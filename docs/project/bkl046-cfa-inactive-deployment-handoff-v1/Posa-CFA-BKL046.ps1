param(
    [Parameter(Mandatory)][ValidateSet('Validate','InstallInactive','VerifyInstalled')][string]$Mode,
    [Parameter(Mandatory)][string]$ReceiptDirectory
)
$ErrorActionPreference = 'Stop'
if ($env:COMPUTERNAME -ine 'DSG-SHARED') { throw 'Usare la VM DSG-Shared.' }
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()
$isAdmin = [Security.Principal.WindowsPrincipal]::new($identity).IsInRole(
    [Security.Principal.WindowsBuiltInRole]::Administrator)
if (($Mode -eq 'InstallInactive') -ne $isAdmin) {
    throw 'InstallInactive richiede PowerShell amministrativo. Le altre modalita richiedono PowerShell ordinario.'
}
$receiptRoot = Get-Item -LiteralPath $ReceiptDirectory
if (!$receiptRoot.PSIsContainer -or ($receiptRoot.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
    throw 'Attesa directory ordinaria per le ricevute.'
}
$receiptId = [guid]::NewGuid().ToString('N')
$runtime = Get-AppxPackage '*CodexPrimaryRuntime*' | Sort-Object Version -Descending |
    Select-Object -First 1 -ExpandProperty InstallLocation
if (!$runtime -or !$runtime.StartsWith('C:\Program Files\WindowsApps\', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Runtime protetto assente.'
}
$python = Join-Path $runtime 'dependencies\python\python.exe'
if ((Get-FileHash -LiteralPath $python).Hash -ine '11d41654aaae8f8de156cd3a6b04326713d28419a267bb84581d8f7166e1b4c1') {
    throw 'Runtime Python diverso da quello collaudato.'
}
$installer = Join-Path $PSScriptRoot 'installa-inattivo.py'
$verifier = Join-Path $PSScriptRoot 'verifica-accesso.py'
$archive = Join-Path $PSScriptRoot 'BKL046-CFA-XDRZ-posa-protetta-candidata-v1.zip'
$installerPin = 'c662f709b2596b0738647ad9c584348872824a0c3bfa53bb486855bd75ce81db'
$verifierPin = 'bd188e7ac1fe753c9f4ba29840e985a1add366dca550c995c39c7ef1803aacf5'
$archivePin = '08a107e2a748de3911bb1b7e3badb03340bb92a5d954c7bb1e55f3f24566de7a'
$subjectPin = '94db7ebe9d92af0fa16f67da4a45636bea24918b782dcd415f1b8dd5a8bfa423'
$bootstrap = @'
import hashlib
from pathlib import Path
import sys
source, digest, *args = sys.argv[1:]
code = Path(source).read_bytes()
if hashlib.sha256(code).hexdigest() != digest:
    raise SystemExit("Pinned program changed")
sys.argv = [source, *args]
exec(compile(code, source, "exec"), {"__name__":"__main__","__file__":source})
'@
function Invoke-PinnedCfa([string]$File,[string]$Pin,[string[]]$Arguments,[string]$Result) {
    & $python -I -B -S -c $bootstrap $File $Pin @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Esecutore terminato con codice $LASTEXITCODE." }
    $data = Get-Content -LiteralPath $Result -Raw | ConvertFrom-Json
    if ($data.subjectSha256 -cne $subjectPin -or $data.archiveSha256 -cne $archivePin -or
        $data.activationConfigured -ne $false -or $data.admissionRequested -ne $false -or
        $data.nativeExecutions -ne 0) { throw 'Ricevuta inattesa.' }
    $data
}
$readback = Join-Path $receiptRoot.FullName "$receiptId-readback.json"
switch ($Mode) {
    'Validate' {
        $lab = Join-Path $receiptRoot.FullName "$receiptId-self-test.json"
        $prepare = Invoke-PinnedCfa $installer $installerPin @('self-test',$archive,$lab) $lab
        $observe = Invoke-PinnedCfa $verifier $verifierPin @('probe',$installer,$archive,$readback) $readback
        if ($prepare.evidence -cne 'ISOLATED_COPY' -or $prepare.filesVerified -ne 3858 -or
            $observe.stagedRosterFiles -ne 3858 -or $observe.verifiedInstalled -ne $false) {
            throw 'Riscontro di collaudo inatteso.'
        }
        [pscustomobject]@{Mode=$Mode; InstallerReceipt=$lab; AccessReceipt=$readback; Files=3858}
    }
    'InstallInactive' {
        $pose = Invoke-PinnedCfa $installer $installerPin @('install-inactive',$archive,$readback) $readback
        if ($pose.evidence -cne 'INACTIVE_INSTALLATION' -or $pose.filesVerified -ne 3858) {throw 'Riscontro di posa inatteso.'}
        [pscustomobject]@{Mode=$Mode; InstallerReceipt=$readback; Files=3858}
    }
    'VerifyInstalled' {
        $observe = Invoke-PinnedCfa $verifier $verifierPin @('verify-installed',$installer,$archive,$readback) $readback
        if ($observe.verifiedInstalled -ne $true -or $observe.ordinaryInstalledFilesVerified -ne 3858) {
            throw 'Riscontro installato inatteso.'
        }
        [pscustomobject]@{Mode=$Mode; AccessReceipt=$readback; Files=3858}
    }
}
