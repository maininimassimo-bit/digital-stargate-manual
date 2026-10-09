param([string]$SchemaPath, [string]$Python = 'python')
$ErrorActionPreference = 'Stop'
$workspace = Join-Path ([System.IO.Path]::GetTempPath()) ('dsg-mpc-schema-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $workspace | Out-Null
$schemaUrl = 'https://raw.githubusercontent.com/IAU-ADES/ADES-Master/f4158f96a049b83dfcf848fa33eaac4391db9460/xsd/submit.xsd'
$expectedHash = '2a5d049808e947cffa11a973a2395c1dde09f00207313a496450b0ef1be27026'
if (-not $SchemaPath) {
    $SchemaPath = Join-Path $workspace 'submit.xsd'
    Invoke-WebRequest -Uri $schemaUrl -OutFile $SchemaPath -MaximumRedirection 0 -TimeoutSec 30
}
if ((Get-Item -LiteralPath $SchemaPath).Length -gt 65536 -or
    (Get-FileHash -LiteralPath $SchemaPath -Algorithm SHA256).Hash.ToLowerInvariant() -ne $expectedHash) {
    throw 'MPC_SCHEMA_BYTES_CHANGED'
}
$schemaSettings = [System.Xml.XmlReaderSettings]::new()
$schemaSettings.DtdProcessing = [System.Xml.DtdProcessing]::Prohibit
$schemaSettings.XmlResolver = $null
$schemaReader = [System.Xml.XmlReader]::Create((Resolve-Path -LiteralPath $SchemaPath).Path, $schemaSettings)
try { $schema = [System.Xml.Schema.XmlSchema]::Read($schemaReader, $null) }
finally { $schemaReader.Dispose() }
if ($schema.Includes.Count -ne 0) { throw 'MPC_SCHEMA_EXTERNAL_REFERENCE' }
$schemas = [System.Xml.Schema.XmlSchemaSet]::new()
$schemas.XmlResolver = $null
[void]$schemas.Add($schema)
$schemas.Compile()
$fixtures = Join-Path $workspace 'fixtures'
& $Python -m tools.scientific_transients.test_mpc_export --schema-fixtures $fixtures
if ($LASTEXITCODE -ne 0) { throw 'MPC_FIXTURE_GENERATION_FAILED' }
$results = [System.Collections.Generic.List[object]]::new()
foreach ($file in (Get-ChildItem -LiteralPath $fixtures -Filter '*.xml')) {
    $validationErrors = [System.Collections.Generic.List[string]]::new()
    $settings = [System.Xml.XmlReaderSettings]::new()
    $settings.DtdProcessing = [System.Xml.DtdProcessing]::Prohibit
    $settings.XmlResolver = $null
    $settings.MaxCharactersInDocument = 2097152
    $settings.ValidationType = [System.Xml.ValidationType]::Schema
    $settings.Schemas = $schemas
    $settings.add_ValidationEventHandler([System.Xml.Schema.ValidationEventHandler] {
        param($sender, $event)
        $validationErrors.Add($event.Message)
    })
    $reader = [System.Xml.XmlReader]::Create($file.FullName, $settings)
    try { while ($reader.Read()) {} }
    finally { $reader.Dispose() }
    $valid = $validationErrors.Count -eq 0
    $expectedValid = $file.Name.StartsWith('valid-')
    if ($valid -ne $expectedValid) { throw ('MPC_XSD_UNEXPECTED_RESULT: ' + $file.Name + ' ' + ($validationErrors -join ' ')) }
    $results.Add(@{ file = $file.Name; schemaValid = $valid; errors = $validationErrors.ToArray() })
}
if ($results.Count -ne 5) { throw 'MPC_SCHEMA_FIXTURE_COUNT' }
@{ schemaUrl = $schemaUrl; schemaSHA256 = $expectedHash; validator = 'System.Xml W3C XSD';
   results = $results; scientificValidation = 'NOT_VALIDATED'; externalSubmission = 'NONE' } |
    ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $workspace 'verification.json') -Encoding utf8
Write-Output "MPC_SCHEMA_TWO_POSITIVE_THREE_NEGATIVE_PASS evidence=$workspace"
