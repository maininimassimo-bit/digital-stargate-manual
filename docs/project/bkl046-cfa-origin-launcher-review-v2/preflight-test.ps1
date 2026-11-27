param([string]$Package,[string]$Python,[string]$Report)
$ErrorActionPreference='Stop'
$subject=Join-Path $Package 'launcher-subject.json'
$raw=Get-Content -LiteralPath $subject -Raw
$config=$raw|ConvertFrom-Json -AsHashtable
$boot=[IO.File]::ReadAllText((Join-Path $Package 'bootstrap.py'))
$good=& $Python -I -B -S -c $boot $Package ($config|ConvertTo-Json -Depth 12 -Compress) check-storage
if($LASTEXITCODE){throw 'Identita storage non confermate'}
$bad=$raw|ConvertFrom-Json -AsHashtable
$bad.storageIdentity.archive.identity[1]='0'
$msg=& $Python -I -B -S -c $boot $Package ($bad|ConvertTo-Json -Depth 12 -Compress) check-storage 2>&1
if($LASTEXITCODE -eq 0 -or -not ($msg -match 'ORIGIN_STORAGE_ROOT_DIFFERS:archive')){throw 'Identita alterata non respinta'}
$pre=& $Python -I -B -S -c $boot $Package ($config|ConvertTo-Json -Depth 12 -Compress) preflight
if($LASTEXITCODE){throw 'Preflight fallito'}
$r=[ordered]@{schema='BKL046_CFA_ORIGIN_STORAGE_BOUND_PREFLIGHT_V2';subjectSha256=(Get-FileHash -LiteralPath $subject).Hash.ToLowerInvariant();
 storage=$good|ConvertFrom-Json;changedArchiveRejected=$true;preflight=$pre|ConvertFrom-Json;
 admissionRequested=$false;nativeExecutions=0}
[IO.File]::WriteAllText($Report,($r|ConvertTo-Json -Depth 7),[Text.UTF8Encoding]::new($false))
