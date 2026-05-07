Deployment helper for InfinityFree (step-by-step)

Overview
--------
This folder contains scripts and instructions to prepare ZIP files for deployment to InfinityFree.

If your File Manager flattens folders during extraction, use the per-folder package script instead of a single ZIP.

Workflow (summary)
1. Run the `split_package_windows.ps1` script to create one ZIP per folder (`app.zip`, `bootstrap.zip`, `config.zip`, `database.zip`, `public.zip`, `resources.zip`, `routes.zip`, `storage.zip`, `vendor.zip`).
2. In InfinityFree File Manager: upload and extract each ZIP into a matching folder under `htdocs/infinityfree`.
3. Create `index.php` in `htdocs` (or edit the existing one) to point to `htdocs/infinityfree`.
4. Upload `.env` to `htdocs/infinityfree/.env` with your InfinityFree DB credentials and `APP_KEY`.
5. Ensure `storage` and `bootstrap/cache` are writable.
6. Use phpMyAdmin to import the SQL.

Detailed steps
--------------
1) Prepare ZIP files (Windows PowerShell)

   Open PowerShell in the `backend` folder (where `artisan` lives) and run:

   ```powershell
   # create one ZIP per folder in the parent directory
   ..\deploy\split_package_windows.ps1
   ```

   Notes:
   - Upload each ZIP into a matching folder name.
   - If a folder already exists on InfinityFree, extract the ZIP into that folder.

2) Upload to InfinityFree

   - Go to File Manager → open `htdocs/infinityfree` → upload and extract `app.zip` into `app`, `bootstrap.zip` into `bootstrap`, `config.zip` into `config`, `database.zip` into `database`, `public.zip` into `public_html`, `resources.zip` into `resources`, `routes.zip` into `routes`, `storage.zip` into `storage`, and `vendor.zip` into `vendor`.

3) Edit `public_html/index.php`

   InfinityFree needs `index.php` to load the application files from the sibling folder. Replace the autoload & bootstrap lines with the contents in `index_php_patch.txt`.

4) Create `.env` in `laravel_app`

   Use `deploy/.env.infinityfree.example` as a template. Fill `DB_DATABASE`, `DB_USERNAME`, `DB_PASSWORD`, and `APP_KEY` (copy the APP_KEY you generated earlier).

5) File permissions

   Set `storage` and `bootstrap/cache` writable via File Manager (right click → Change Permissions) if available. On InfinityFree you may not need to change file permissions manually.

6) Database

   - Open InfinityFree Control Panel → MySQL Databases → click `phpMyAdmin` for the database you created.
   - If you have SQL dump, import it. Otherwise your app can run without data and you can use migrations locally to generate schema and export the DB, then import.

If anything fails, copy the error message or screenshot and send it here and I'll help troubleshoot.
