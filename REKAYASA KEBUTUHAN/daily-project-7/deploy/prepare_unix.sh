#!/usr/bin/env bash
set -euo pipefail

echo "Creating laravel_app.zip and public.zip..."

# run from backend folder
zip -r ../laravel_app.zip . -x .env
(cd public && zip -r ../../public.zip .)

echo "Done. Files: ../laravel_app.zip and ../public.zip"
