# PowerShell helper to create deploy zips for InfinityFree
# Run this from the backend folder (where artisan lives)

param()

Write-Host "Creating laravel_app.zip and public.zip..."

# create laravel_app.zip in the parent folder
Compress-Archive -Path * -DestinationPath ..\laravel_app.zip -Force

# create public.zip from public/ contents
Compress-Archive -Path public\* -DestinationPath ..\public.zip -Force

Write-Host "Done. Files created: ../laravel_app.zip and ../public.zip"
