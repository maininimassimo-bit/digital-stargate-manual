[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot '..\..')).Path
$collectorPath = Join-Path $repoRoot 'scripts\telemetry\Start-EagleHealthCollectorPilot.ps1'
if (-not (Test-Path -LiteralPath $collectorPath -PathType Leaf)) {
  throw "Collector script not found: $collectorPath"
}

$tokens = $null
$parseErrors = $null
$ast = [System.Management.Automation.Language.Parser]::ParseFile(
  $collectorPath,
  [ref]$tokens,
  [ref]$parseErrors)

if ($parseErrors.Count -gt 0) {
  $details = ($parseErrors | ForEach-Object { $_.Message }) -join '; '
  throw "PowerShell parser errors: $details"
}

$raw = Get-Content -LiteralPath $collectorPath -Raw

function Assert-Match {
  param([string]$Pattern,[string]$Name)
  if ($raw -notmatch $Pattern) { throw "Missing contract invariant: $Name" }
}

function Assert-NotMatch {
  param([string]$Pattern,[string]$Name)
  if ($raw -match $Pattern) { throw "Forbidden contract pattern present: $Name" }
}

Assert-Match 'eagle-health-pilot\.json' 'pilot output filename'
Assert-Match "ValidateSet\('NONE','FAST','MEDIUM','SLOW'\)" 'failure-injection allowlist'
Assert-Match "FailureInjectionGroup\s*=\s*'NONE'" 'failure injection disabled by default'
Assert-Match 'GetFileName\(\$OutputPath\).*pilot' 'failure injection constrained to pilot output'
Assert-Match "state='UNKNOWN'.*POLICY_NOT_ACTIVATED" 'summary policy disabled'
Assert-Match 'policy_enabled=\$false' 'policy_enabled false'
Assert-Match "safety_authority='OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS'" 'Safety Authority boundary'
Assert-Match 'reboot_required=\$null;policy=''RAW_EVIDENCE_ONLY''' 'pending reboot raw evidence only'
Assert-Match "reason='UNAVAILABLE_NON_ELEVATED'" 'non-elevated reliability behavior'
Assert-Match 'TEST_INJECTED_FAST_SOURCE_FAILURE' 'FAST failure injection'
Assert-Match 'TEST_INJECTED_MEDIUM_SOURCE_FAILURE' 'MEDIUM failure injection'
Assert-Match 'TEST_INJECTED_SLOW_SOURCE_FAILURE' 'SLOW failure injection'
Assert-Match "New-SignalEnvelope 'OBSERVED' 'CURRENT'" 'nominal signal envelope'
Assert-Match "New-SignalEnvelope 'UNAVAILABLE' 'UNKNOWN'" 'failure signal envelope'
Assert-Match '\$tmp="\$OutputPath\.tmp"' 'atomic temporary output'
Assert-Match 'Move-Item -LiteralPath \$tmp -Destination \$OutputPath -Force' 'atomic projection replace'

$expectedSignals = @(
  'cpu','memory','uptime','processes','plugin_heartbeat',
  'storage','scheduled_tasks','log_sources',
  'event_log','usb_com','pending_reboot','time_sync','configuration_drift'
)
foreach ($signal in $expectedSignals) {
  Assert-Match ("'" + [regex]::Escape($signal) + "'") ("signal " + $signal)
}
if ($expectedSignals.Count -ne 13) { throw 'Internal test error: expected signal count is not 13.' }

# The collector may read host state, write only its projection, and sleep. It must not
# contain commands that mutate Windows services, tasks, registry, power, or host state.
$forbiddenCommands = @(
  'Start-Service','Stop-Service','Restart-Service','Set-Service',
  'Register-ScheduledTask','Set-ScheduledTask','Unregister-ScheduledTask','Start-ScheduledTask','Stop-ScheduledTask',
  'Set-ItemProperty','New-ItemProperty','Remove-ItemProperty',
  'Restart-Computer','Stop-Computer','Rename-Computer',
  'Enable-WindowsOptionalFeature','Disable-WindowsOptionalFeature',
  'Install-WindowsUpdate','Get-WindowsUpdate',
  'powercfg','shutdown','netsh'
)

$commandNames = @($ast.FindAll({
  param($node)
  $node -is [System.Management.Automation.Language.CommandAst]
}, $true) | ForEach-Object { $_.GetCommandName() } | Where-Object { $_ })

foreach ($forbidden in $forbiddenCommands) {
  if ($commandNames -contains $forbidden) {
    throw "Forbidden mutating command found in collector AST: $forbidden"
  }
}

# Explicitly prevent the pilot from defaulting to the final commissioned filename.
Assert-NotMatch '\[string\]\$OutputPath\s*=\s*"\$env:LOCALAPPDATA\\DigitalStarGate\\telemetry\\eagle-health\.json"' 'commissioned output as pilot default'

Write-Host ('Collector AST commands inspected: {0}' -f $commandNames.Count)
Write-Host ('Expected projection signals verified: {0}' -f $expectedSignals.Count)
Write-Host 'EAGLE HEALTH COLLECTOR CONTRACT TEST RESULT: PASS'
