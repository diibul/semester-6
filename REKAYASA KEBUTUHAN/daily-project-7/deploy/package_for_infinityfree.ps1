# ============================================================
# StudioBook – Deploy to InfinityFree (Fresh)
# Run from: daily-project-7 folder (project root)
# ============================================================

$ErrorActionPreference = 'Stop'

$projectRoot = $PSScriptRoot | Split-Path  # Go up from deploy/ to project root
$backendDir  = Join-Path $projectRoot 'backend'
$outputDir   = Join-Path $projectRoot '_deploy_output'

Write-Host "=== StudioBook InfinityFree Deploy Packager ===" -ForegroundColor Cyan
Write-Host "Project root: $projectRoot"
Write-Host "Backend dir:  $backendDir"
Write-Host ""

# ---------- 1. Clean previous output ----------
if (Test-Path $outputDir) {
    Remove-Item $outputDir -Recurse -Force
}
New-Item -ItemType Directory -Path $outputDir | Out-Null

# ---------- 2. Check vendor exists ----------
$vendorDir = Join-Path $backendDir 'vendor'
if (-not (Test-Path $vendorDir)) {
    Write-Host "[ERROR] vendor/ not found! Run 'composer install' in backend/ first." -ForegroundColor Red
    exit 1
}

# ---------- 3. Check build assets exist ----------
$buildDir = Join-Path $backendDir 'public\build'
if (-not (Test-Path $buildDir)) {
    Write-Host "[ERROR] public/build/ not found! Run 'npm run build' in frontend/ first." -ForegroundColor Red
    exit 1
}

Write-Host "[OK] vendor/ found" -ForegroundColor Green
Write-Host "[OK] public/build/ found" -ForegroundColor Green
Write-Host ""

# ---------- 4. Create htdocs root .htaccess ----------
# This redirects all traffic to the public/ subdirectory
# so we don't need to modify index.php at all!
$rootHtaccess = @"
<IfModule mod_rewrite.c>
    RewriteEngine On

    # Redirect all requests to public/ subfolder
    RewriteCond %{REQUEST_URI} !^/public/
    RewriteRule ^(.*)$ public/`$1 [L]
</IfModule>
"@

$rootHtaccessPath = Join-Path $outputDir '.htaccess_root'
$rootHtaccess | Out-File -FilePath $rootHtaccessPath -Encoding utf8

# ---------- 5. Package per-folder ZIPs ----------
# InfinityFree File Manager has upload size limits (~10MB).
# We create separate ZIPs per folder so each stays small.

Write-Host "Creating per-folder ZIP packages..." -ForegroundColor Yellow

$folders = @('app', 'bootstrap', 'config', 'database', 'resources', 'routes', 'storage')
$rootFiles = @('artisan', 'composer.json', 'composer.lock', 'phpunit.xml')

foreach ($folder in $folders) {
    $srcPath = Join-Path $backendDir $folder
    if (Test-Path $srcPath) {
        $zipPath = Join-Path $outputDir "$folder.zip"
        Write-Host "  Packaging $folder -> $folder.zip"
        Compress-Archive -Path $srcPath -DestinationPath $zipPath -Force
    }
}

# vendor/ is big, might need to split
$vendorZip = Join-Path $outputDir 'vendor.zip'
Write-Host "  Packaging vendor -> vendor.zip (this may take a moment...)"
Compress-Archive -Path $vendorDir -DestinationPath $vendorZip -Force

# public/ folder (includes build assets)
$publicDir = Join-Path $backendDir 'public'
$publicZip = Join-Path $outputDir 'public.zip'
Write-Host "  Packaging public -> public.zip"
Compress-Archive -Path $publicDir -DestinationPath $publicZip -Force

# Root files
$rootFilePaths = @()
foreach ($file in $rootFiles) {
    $filePath = Join-Path $backendDir $file
    if (Test-Path $filePath) {
        $rootFilePaths += $filePath
    }
}
if ($rootFilePaths.Count -gt 0) {
    $rootFilesZip = Join-Path $outputDir 'root_files.zip'
    Write-Host "  Packaging root files -> root_files.zip"
    Compress-Archive -Path $rootFilePaths -DestinationPath $rootFilesZip -Force
}

# ---------- 6. Copy SQL dump and .env template ----------
$sqlSrc = Join-Path $projectRoot 'deploy\studiobookmusic_infinityfree.sql'
$envSrc = Join-Path $projectRoot 'deploy\.env.infinityfree.example'

Copy-Item $sqlSrc (Join-Path $outputDir 'database.sql')
Copy-Item $envSrc (Join-Path $outputDir '.env.example')

# ---------- 7. Summary ----------
Write-Host ""
Write-Host "=== Packaging Complete! ===" -ForegroundColor Green
Write-Host "Output folder: $outputDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files created:" -ForegroundColor Yellow

Get-ChildItem $outputDir | ForEach-Object {
    $sizeMB = [math]::Round($_.Length / 1MB, 2)
    Write-Host ("  {0,-25} {1,8} MB" -f $_.Name, $sizeMB)
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Login ke InfinityFree -> buka File Manager"
Write-Host "2. Di htdocs/, upload .htaccess_root dan rename jadi .htaccess"
Write-Host "3. Upload & extract setiap ZIP ke htdocs/ (buat folder matching)"
Write-Host "4. Upload .env.example ke htdocs/.env dan isi database credentials"
Write-Host "5. Di phpMyAdmin, import database.sql"
Write-Host "6. Buka website kamu!"
