[CmdletBinding()]
param(
    [string]$EvidenceRoot = 'C:\DigitalStarGate\TelemetryEvidence'
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$timestamp = [datetime]::UtcNow.ToString('yyyyMMdd-HHmmss')
$bundle = Join-Path $EvidenceRoot ("power-network-source-inventory-{0}" -f $timestamp)
New-Item -ItemType Directory -Path $bundle -Force | Out-Null

Write-Output 'Digital StarGate Power/Network telemetry source inspector - READ ONLY'
Write-Output ('Computer: {0}' -f $env:COMPUTERNAME)
Write-Output ('Evidence bundle: {0}' -f $bundle)

function Safe-Cim {
    param([string]$ClassName)
    try { return @(Get-CimInstance -ClassName $ClassName -ErrorAction Stop) } catch { return @() }
}

$networkAdapters = @(Get-NetAdapter -ErrorAction SilentlyContinue |
    Select-Object Name, InterfaceDescription, Status, LinkSpeed, MacAddress, ifIndex)

$ipConfig = @(Get-NetIPConfiguration -ErrorAction SilentlyContinue | ForEach-Object {
    $ipv4Addresses = @()
    if ($null -ne $_.IPv4Address) {
        $ipv4Addresses = @($_.IPv4Address | Where-Object { $null -ne $_ } | ForEach-Object { $_.IPAddress })
    }

    $ipv4Gateways = @()
    if ($null -ne $_.IPv4DefaultGateway) {
        $ipv4Gateways = @($_.IPv4DefaultGateway | Where-Object { $null -ne $_ } | ForEach-Object { $_.NextHop })
    }

    $dnsServers = @()
    if ($null -ne $_.DNSServer -and $null -ne $_.DNSServer.ServerAddresses) {
        $dnsServers = @($_.DNSServer.ServerAddresses | Where-Object { -not [string]::IsNullOrWhiteSpace([string]$_) })
    }

    [pscustomobject]@{
        interface_alias = $_.InterfaceAlias
        interface_index = $_.InterfaceIndex
        ipv4_address = $ipv4Addresses
        ipv4_gateway = $ipv4Gateways
        dns_server = $dnsServers
    }
})

$routes = @(Get-NetRoute -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.DestinationPrefix -eq '0.0.0.0/0' } |
    Select-Object InterfaceAlias, InterfaceIndex, NextHop, RouteMetric, State)

$vpnAdapters = @($networkAdapters | Where-Object {
    $_.Name -match '(?i)vpn|openvpn|wireguard|tap|tun' -or $_.InterfaceDescription -match '(?i)vpn|openvpn|wireguard|tap|tun'
})

$relevantProcesses = @(Get-Process -ErrorAction SilentlyContinue |
    Where-Object { $_.ProcessName -match '(?i)eagle|ups|power|openvpn|wireguard|rut|teltonika' } |
    Select-Object ProcessName, Id, Path)

$relevantServices = @(Get-Service -ErrorAction SilentlyContinue |
    Where-Object { $_.Name -match '(?i)eagle|ups|power|openvpn|wireguard|rut|teltonika' -or $_.DisplayName -match '(?i)eagle|ups|power|openvpn|wireguard|rut|teltonika' } |
    Select-Object Name, DisplayName, Status, StartType)

$batteries = @(Safe-Cim -ClassName 'Win32_Battery' | Select-Object Name, DeviceID, BatteryStatus, EstimatedChargeRemaining, EstimatedRunTime, Status)

$pnpPower = @(Safe-Cim -ClassName 'Win32_PnPEntity' |
    Where-Object { $_.Name -match '(?i)ups|battery|power|eagle' -or $_.Description -match '(?i)ups|battery|power|eagle' } |
    Select-Object Name, Description, PNPDeviceID, Status)

$candidateRoots = @(
    'C:\Program Files\PrimaLuceLab',
    'C:\Program Files (x86)\PrimaLuceLab',
    'C:\ProgramData\PrimaLuceLab',
    (Join-Path $env:LOCALAPPDATA 'PrimaLuceLab'),
    (Join-Path $env:APPDATA 'PrimaLuceLab'),
    'C:\DigitalStarGate'
)

$candidatePaths = foreach ($root in $candidateRoots) {
    [pscustomobject]@{ path = $root; exists = [bool](Test-Path -LiteralPath $root) }
}

$report = [ordered]@{
    schema_version = '1.0'
    component = 'DSG.PowerNetworkTelemetrySourceInspector'
    computer = $env:COMPUTERNAME
    observed_at_utc = [datetime]::UtcNow.ToString('o')
    mode = 'READ_ONLY_NO_CONFIGURATION_CHANGES_NO_DEVICE_COMMANDS'
    network = [ordered]@{
        adapters = $networkAdapters
        ip_configuration = $ipConfig
        default_routes = $routes
        vpn_candidates = $vpnAdapters
    }
    power = [ordered]@{
        batteries = $batteries
        pnp_candidates = $pnpPower
        relevant_processes = $relevantProcesses
        relevant_services = $relevantServices
        candidate_paths = @($candidatePaths)
    }
    conclusions = [ordered]@{
        network_operational_interface_verified = $false
        power_operational_interface_verified = $false
        router_configuration_changed = $false
        power_command_sent = $false
        device_connections_opened = $false
        note = 'Inventory only. Do not enable Power/Network runtime adapters until source identity, read-only access, semantics and freshness are validated.'
    }
}

$jsonPath = Join-Path $bundle 'power-network-source-inventory.json'
$txtPath = Join-Path $bundle 'power-network-source-inventory.txt'
$report | ConvertTo-Json -Depth 10 | Set-Content -LiteralPath $jsonPath -Encoding UTF8

@(
    '=== NETWORK ADAPTERS ===',
    ($networkAdapters | Format-Table -AutoSize | Out-String),
    '=== IP CONFIGURATION ===',
    ($ipConfig | Format-List | Out-String),
    '=== DEFAULT ROUTES ===',
    ($routes | Format-Table -AutoSize | Out-String),
    '=== VPN CANDIDATES ===',
    ($vpnAdapters | Format-Table -AutoSize | Out-String),
    '=== POWER/EAGLE PROCESSES ===',
    ($relevantProcesses | Format-Table -AutoSize | Out-String),
    '=== POWER/EAGLE SERVICES ===',
    ($relevantServices | Format-Table -AutoSize | Out-String),
    '=== WINDOWS BATTERY ===',
    ($batteries | Format-Table -AutoSize | Out-String),
    '=== POWER PNP CANDIDATES ===',
    ($pnpPower | Format-Table -AutoSize | Out-String),
    '=== CANDIDATE PATHS ===',
    ($candidatePaths | Format-Table -AutoSize | Out-String)
) | Set-Content -LiteralPath $txtPath -Encoding UTF8

Write-Output ''
Write-Output '=== DEFAULT ROUTES ==='
$routes | Format-Table -AutoSize | Out-String | Write-Output
Write-Output '=== VPN CANDIDATES ==='
if ($vpnAdapters.Count -gt 0) { $vpnAdapters | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== POWER/EAGLE PROCESSES ==='
if ($relevantProcesses.Count -gt 0) { $relevantProcesses | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== POWER/EAGLE SERVICES ==='
if ($relevantServices.Count -gt 0) { $relevantServices | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output '=== WINDOWS BATTERY / UPS CANDIDATES ==='
if ($batteries.Count -gt 0) { $batteries | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found via Win32_Battery)' }
Write-Output '=== POWER PNP CANDIDATES ==='
if ($pnpPower.Count -gt 0) { $pnpPower | Format-Table -AutoSize | Out-String | Write-Output } else { Write-Output '(none found)' }
Write-Output ('Evidence JSON: {0}' -f $jsonPath)
Write-Output ('Evidence TXT : {0}' -f $txtPath)
Write-Output 'POWER/NETWORK SOURCE INVENTORY RESULT: PASS (inventory only)'
