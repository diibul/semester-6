# Create per-folder ZIP packages for InfinityFree when archive extraction flattens folders.
# Run this from the backend folder (where artisan lives).

param()

$ErrorActionPreference = 'Stop'

function New-ZipFromFolder {
    param(
        [Parameter(Mandatory=$true)][string]$SourceFolder,
        [Parameter(Mandatory=$true)][string]$DestinationZip
    )

    if (Test-Path $DestinationZip) { Remove-Item $DestinationZip -Force }

    $tempRoot = Join-Path $env:TEMP ('iffree_' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $tempRoot | Out-Null
    $tempPackage = Join-Path $tempRoot (Split-Path $SourceFolder -Leaf)
    Copy-Item -Path $SourceFolder -Destination $tempPackage -Recurse
    Compress-Archive -Path (Join-Path $tempPackage '*') -DestinationPath $DestinationZip -Force
    Remove-Item $tempRoot -Recurse -Force
}

$folders = @('app','bootstrap','config','database','public','resources','routes','storage','vendor')

foreach ($folder in $folders) {
    if (Test-Path $folder) {
        $zipPath = Join-Path .. ($folder + '.zip')
        Write-Host "Packaging $folder -> $zipPath"
        New-ZipFromFolder -SourceFolder $folder -DestinationZip $zipPath
    }
}

Write-Host 'Done. Upload each ZIP and extract it into a matching folder in InfinityFree.'
