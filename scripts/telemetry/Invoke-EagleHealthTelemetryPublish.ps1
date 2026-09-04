[CmdletBinding()]
param(
    [string]$RepositoryRoot = 'C:\DigitalStarGate\digital-stargate-manual-ap14-runtime',
    [string]$SecretPath = 'C:\DigitalStarGate\TelemetryRuntime\secrets\ingest-token.dpapi',
    [string]$CollectorProjection = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\eagle-health.json",
    [string]$PublicProjection = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\eagle-health-public.json",
    [string]$PublishEndpoint = 'https://dsg-observatory-status-relay-cfjug35c6q-ew.a.run.app/v1/eagle-health',
    [switch]$ValidateOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

if ($env:COMPUTERNAME -ne 'EAGLE30154') {
    throw "EAGLE Health publication is authorized only from EAGLE30154; current host=$env:COMPUTERNAME"
}

$collector = Join-Path $RepositoryRoot 'scripts\telemetry\Export-EagleHostHealth.ps1'
$projector = Join-Path $RepositoryRoot 'scripts\telemetry\Export-EagleHealthPortalProjection.ps1'
$publisher = Join-Path $RepositoryRoot 'scripts\telemetry\Publish-EagleHealthTelemetry.ps1'

foreach ($path in @($collector, $projector, $publisher, $SecretPath)) {
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Required runtime file not found: $path"
    }
}

$uri = [Uri]$PublishEndpoint
if ($uri.Scheme -ne 'https') { throw 'PublishEndpoint must use HTTPS.' }

# Collector is read-only and performs no remediation. Refresh immediately before
# publication so the public projection cannot inherit an already-stale sample.
& $collector -OutputPath $CollectorProjection -CadenceClass all | Out-Null
& $projector -InputPath $CollectorProjection -OutputPath $PublicProjection | Out-Null

Add-Type -AssemblyName System.Security
$protected = [System.IO.File]::ReadAllBytes($SecretPath)
$plainBytes = [System.Security.Cryptography.ProtectedData]::Unprotect(
    $protected,
    $null,
    [System.Security.Cryptography.DataProtectionScope]::LocalMachine)

try {
    $token = [System.Text.Encoding]::UTF8.GetString($plainBytes)
    if ([string]::IsNullOrWhiteSpace($token)) { throw 'Decrypted ingest token is empty.' }

    $arguments = @{
        ProjectionPath = $PublicProjection
        Endpoint = $PublishEndpoint
        BearerToken = $token
    }
    if ($ValidateOnly) { $arguments.ValidateOnly = $true }

    & $publisher @arguments
}
finally {
    if ($plainBytes) { [Array]::Clear($plainBytes, 0, $plainBytes.Length) }
    $token = $null
}
