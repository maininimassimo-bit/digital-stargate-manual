$ErrorActionPreference='Stop'
$script=Join-Path $PSScriptRoot '..\..\scripts\telemetry\Export-EagleHostHealth.ps1'
if(-not (Test-Path $script)){ throw 'Exporter missing' }
$text=Get-Content -Raw $script
$required=@('DSG.EagleHostHealthCollector','eagle-health.json','POLICY_NOT_ACTIVATED','free_bytes','free_pct','health_status','operational_status','automatic_remediation=$false','Move-Item -LiteralPath $tmp -Destination $OutputPath -Force')
foreach($token in $required){ if($text -notlike ('*'+$token+'*')){ throw "Missing contract token: $token" } }
$forbidden=@('Restart-Computer','Stop-Process','Restart-Service','Start-Service','Set-Service','Disable-PnpDevice','Enable-PnpDevice','Set-ItemProperty','Remove-ItemProperty','Register-ScheduledTask','Set-NetAdapter','shutdown.exe')
foreach($token in $forbidden){ if($text -match [regex]::Escape($token)){ throw "Forbidden remediation/control command found: $token" } }
$tokens=$null;$errors=$null
[void][System.Management.Automation.Language.Parser]::ParseFile($script,[ref]$tokens,[ref]$errors)
if($errors.Count -gt 0){ throw ('PowerShell parse errors: '+(($errors | ForEach-Object {$_.Message}) -join '; ')) }
Write-Host 'EAGLE host health collector contract checks: PASS'
