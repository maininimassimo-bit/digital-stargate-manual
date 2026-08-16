[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$CloudWatcherCsv,

    [Parameter(Mandatory = $true)]
    [string]$OutputPath,

    [ValidateRange(1, 3600)]
    [int]$FreshnessSeconds = 60,

    [ValidateRange(4096, 1048576)]
    [int