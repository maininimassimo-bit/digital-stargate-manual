[CmdletBinding()]
param(
  [string]$ProjectionPath = "$env:LOCALAPPDATA\DigitalStarGate\telemetry\eagle-health-pilot.json",
  [string]$ConfigPath,
  [switch]$AllowCommissionedProjection
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Fail([string]$Message) { throw "BKL-030 OAT FAIL: $Message" }

if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
  $ConfigPath = Join-Path $PSScriptRoot 'eagle-health-commissioning.config.json'
}

if (-not (Test-Path -LiteralPath $ConfigPath -PathType Leaf)) { Fail "config not found: $ConfigPath" }
$config = Get-Content -LiteralPath $ConfigPath -Raw | ConvertFrom-Json

if ($config.commissioning.enabled -ne $false) { Fail 'precommissioning config must remain disabled' }
if ($config.commissioning.state -ne 'BLOCKED_BY_BKL_029') { Fail 'commissioning dependency guard is not BKL-029' }
if ($config.policy.enabled -ne $false) { Fail 'health classification policy must remain disabled' }
if ($config.safety.authority -ne 'OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS') { Fail 'Safety Authority boundary changed' }
if ($config.safety.may_authorize_equipment_actions -ne $false -or $config.safety.may_authorize_safety_actions -ne $false) { Fail 'collector must not authorize equipment or Safety actions' }

$expandedCommissioned = [Environment]::ExpandEnvironmentVariables([string]$config.projection.commissioned_path)
$expandedPilot = [Environment]::ExpandEnvironmentVariables([string]$config.projection.pilot_path)
$resolvedRequested = [Environment]::ExpandEnvironmentVariables($ProjectionPath)

if (-not $AllowCommissionedProjection -and [string]::Equals($resolvedRequested, $expandedCommissioned, [StringComparison]::OrdinalIgnoreCase)) {
  Fail 'commissioned projection is blocked in precommissioning OAT; use pilot projection'
}
if (-not (Test-Path -LiteralPath $resolvedRequested -PathType Leaf)) { Fail "projection not found: $resolvedRequested" }

$p = Get-Content -LiteralPath $resolvedRequested -Raw | ConvertFrom-Json
if ($p.schema_version -ne '1.0') { Fail "unexpected schema_version: $($p.schema_version)" }
if ($p.component -ne 'DSG.EagleHostHealthCollector') { Fail "unexpected component: $($p.component)" }
if ([string]::IsNullOrWhiteSpace([string]$p.computer)) { Fail 'computer is empty' }
if ($p.summary.state -ne 'UNKNOWN') { Fail "summary must remain UNKNOWN precommissioning; got $($p.summary.state)" }
if (@($p.summary.reasons | Where-Object { $_.code -eq 'POLICY_NOT_ACTIVATED' }).Count -lt 1) { Fail 'POLICY_NOT_ACTIVATED reason missing' }
if ($p.diagnostics.policy_enabled -ne $false) { Fail 'projection policy_enabled must be false' }
if ($p.diagnostics.safety_authority -ne 'OUTSIDE_SCOPE_LOCAL_PHYSICAL_INTERLOCKS') { Fail 'projection Safety Authority boundary changed' }

$required = @($config.oat.required_signals)
$actual = @($p.signals.PSObject.Properties.Name)
$missing = @($required | Where-Object { $_ -notin $actual })
if ($missing.Count -gt 0) { Fail ('missing signals: ' + ($missing -join ',')) }

foreach ($name in $required) {
  $s = $p.signals.$name
  if ($null -eq $s) { Fail "signal is null: $name" }
  if ($s.state -notin @('OBSERVED','UNAVAILABLE','NOT_SUPPORTED','UNKNOWN')) { Fail "invalid state for ${name}: $($s.state)" }
  if ($s.quality -notin @('CURRENT','STALE','UNKNOWN')) { Fail "invalid quality for ${name}: $($s.quality)" }
}

$observed = [DateTimeOffset]::Parse([string]$p.observed_at_utc)
$freshUntil = [DateTimeOffset]::Parse([string]$p.fresh_until_utc)
if ($freshUntil -le $observed) { Fail 'fresh_until_utc must be later than observed_at_utc' }

Write-Host 'Digital StarGate BKL-030 EAGLE Health OAT - PRECOMMISSIONING'
Write-Host "Computer: $($p.computer)"
Write-Host "Projection: $resolvedRequested"
Write-Host "Pilot boundary: $expandedPilot"
Write-Host "Signals: $($actual.Count); required=$($required.Count); missing=0"
Write-Host "Summary: $($p.summary.state); policy_enabled=$($p.diagnostics.policy_enabled)"
Write-Host "Safety authority: $($p.diagnostics.safety_authority)"
Write-Host 'BKL-030 OAT RESULT: PASS - PRECOMMISSIONING ONLY; NOT COMMISSIONING OR ACCEPTANCE'
