[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [string]$GatewayAddress = '192.168.1.254',

    [string]$InternetAddress = '1.1.1.1',

    [ValidateRange(1, 65535)]
    [int]$InternetPort = 443,

    [string]$DnsName = 'github.com',

    [ValidateRange(250, 10000)]
    [int]$TimeoutMilliseconds = 3000,

    [ValidateRange(5, 3600)]
    [int]$FreshnessSeconds = 60,

    [string]$SourceInstance = $env:COMPUTERNAME
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Test-TcpEndpoint {
    param(
        [Parameter(Mandatory = $true)][string]$Address,
        [Parameter(Mandatory = $true)][int]$Port,
        [Parameter(Mandatory = $true)][int]$TimeoutMs
    )

    $client = New-Object System.Net.Sockets.TcpClient
    $started = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        $async = $client.BeginConnect($Address, $Port, $null, $null)
        if (-not $async.AsyncWaitHandle.WaitOne($TimeoutMs, $false)) {
            return [pscustomobject]@{ Success = $false; LatencyMs = $null; Error = 'timeout' }
        }
        $client.EndConnect($async)
        $started.Stop()
        return [pscustomobject]@{ Success = $true; LatencyMs = [int]$started.ElapsedMilliseconds; Error = $null }
    }
    catch {
        $started.Stop()
        return [pscustomobject]@{ Success = $false; LatencyMs = $null; Error = $_.Exception.Message }
    }
    finally {
        $client.Close()
    }
}

function Test-DnsResolution {
    param(
        [Parameter(Mandatory = $true)][string]$Name,
        [Parameter(Mandatory = $true)][int]$TimeoutMs
    )

    $started = [System.Diagnostics.Stopwatch]::StartNew()
    try {
        $task = [System.Net.Dns]::GetHostAddressesAsync($Name)
        if (-not $task.Wait($TimeoutMs)) {
            return [pscustomobject]@{ Success = $false; LatencyMs = $null; Addresses = @(); Error = 'timeout' }
        }
        $addresses = @($task.Result | ForEach-Object { $_.IPAddressToString })
        $started.Stop()
        return [pscustomobject]@{
            Success = ($addresses.Count -gt 0)
            LatencyMs = [int]$started.ElapsedMilliseconds
            Addresses = $addresses
            Error = $null
        }
    }
    catch {
        $started.Stop()
        return [pscustomobject]@{ Success = $false; LatencyMs = $null; Addresses = @(); Error = $_.Exception.Message }
    }
}

function Get-DefaultRouteEvidence {
    $routes = @(Get-NetRoute -AddressFamily IPv4 -ErrorAction Stop |
        Where-Object { $_.DestinationPrefix -eq '0.0.0.0/0' -and $_.State -eq 'Alive' } |
        Sort-Object RouteMetric, InterfaceMetric)

    if ($routes.Count -eq 0) {
        return [pscustomobject]@{
            Present = $false
            InterfaceAlias = $null
            NextHop = $null
            RouteMetric = $null
        }
    }

    $route = $routes[0]
    return [pscustomobject]@{
        Present = $true
        InterfaceAlias = [string]$route.InterfaceAlias
        NextHop = [string]$route.NextHop
        RouteMetric = [int]$route.RouteMetric
    }
}

$observedAt = [datetime]::UtcNow
$freshUntil = $observedAt.AddSeconds($FreshnessSeconds)

$route = Get-DefaultRouteEvidence
$gateway = Test-TcpEndpoint -Address $GatewayAddress -Port 443 -TimeoutMs $TimeoutMilliseconds
if (-not $gateway.Success) {
    $gateway = Test-TcpEndpoint -Address $GatewayAddress -Port 80 -TimeoutMs $TimeoutMilliseconds
}
$internet = Test-TcpEndpoint -Address $InternetAddress -Port $InternetPort -TimeoutMs $TimeoutMilliseconds
$dns = Test-DnsResolution -Name $DnsName -TimeoutMs $TimeoutMilliseconds

$allHealthy = $route.Present -and $gateway.Success -and $internet.Success -and $dns.Success
$externalPartial = $route.Present -and $gateway.Success -and ($internet.Success -or $dns.Success)
$allExternalFailed = (-not $internet.Success) -and (-not $dns.Success)

$state = 'UNKNOWN'
$quality = 'CURRENT'
$reasons = New-Object System.Collections.Generic.List[string]

if ($allHealthy) {
    $state = 'ONLINE'
    $reasons.Add('Default route, local gateway, Internet TCP and DNS resolution are all healthy.')
}
elif ($externalPartial) {
    $state = 'DEGRADED'
    $reasons.Add('Local route/gateway are healthy but at least one external dependency check failed.')
}
elif ((-not $route.Present) -or ((-not $gateway.Success) -and $allExternalFailed)) {
    $state = 'OFFLINE'
    $reasons.Add('No usable default route, or gateway and all external dependency checks failed.')
}
else {
    $state = 'DEGRADED'
    $reasons.Add('Mixed network evidence does not support ONLINE; degraded state selected fail-safe.')
}

if ($route.Present -and $route.NextHop -ne $GatewayAddress) {
    $reasons.Add(('Observed default gateway {0} differs from configured candidate {1}; active link semantics remain unknown.' -f $route.NextHop, $GatewayAddress))
}

$payload = [ordered]@{
    schema_version = '1.0'
    source_component = 'DSG.PassiveNetworkTelemetryAdapter'
    source_instance = $SourceInstance
    observed_at_utc = $observedAt.ToString('o')
    fresh_until_utc = $freshUntil.ToString('o')
    state = $state
    quality = $quality
    active_link = $null
    vpn = $null
    lte_failover = $null
    reasons = @($reasons)
    diagnostics = [ordered]@{
        default_route_present = $route.Present
        interface_alias = $route.InterfaceAlias
        next_hop = $route.NextHop
        route_metric = $route.RouteMetric
        configured_gateway = $GatewayAddress
        gateway_tcp_reachable = $gateway.Success
        gateway_latency_ms = $gateway.LatencyMs
        internet_target = ('{0}:{1}' -f $InternetAddress, $InternetPort)
        internet_tcp_reachable = $internet.Success
        internet_latency_ms = $internet.LatencyMs
        dns_name = $DnsName
        dns_resolved = $dns.Success
        dns_latency_ms = $dns.LatencyMs
        dns_address_count = @($dns.Addresses).Count
    }
}

$parent = Split-Path -Parent $OutputPath
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}

$tempPath = "$OutputPath.tmp"
$payload | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $tempPath -Encoding UTF8
Move-Item -LiteralPath $tempPath -Destination $OutputPath -Force

Write-Output ('Passive network projection written: {0}' -f $OutputPath)
Write-Output ('Observed UTC: {0}' -f $payload.observed_at_utc)
Write-Output ('Network: {0} / {1}' -f $payload.state, $payload.quality)
Write-Output ('Route: present={0} interface={1} nextHop={2}' -f $route.Present, $route.InterfaceAlias, $route.NextHop)
Write-Output ('Checks: gateway={0} internet={1} dns={2}' -f $gateway.Success, $internet.Success, $dns.Success)
Write-Output 'Semantics intentionally unresolved: active_link=null vpn=null lte_failover=null'
