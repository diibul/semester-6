# Phase 6 - Deployment Engineering

Dokumen ini memvalidasi checklist deployment pada roadmap Phase 6.

## 1) Output wajib

- Repo GitHub rapi: completed (struktur dipisah `backend`, `frontend`, `readme`).
- README lengkap: completed (deskripsi, fitur, stack, install, testing table, deployment section).
- Deploy sukses (Railway atau Render): prepared and ready.

Catatan:
Deploy live membutuhkan kredensial cloud dan akses akun user. Artefak deploy sudah disiapkan agar proses bisa langsung dieksekusi.

## 2) Artefak deployment yang ditambahkan

- `render.yaml`
  - Build backend + frontend.
  - Start command untuk serve aplikasi.
  - Default env vars production.
- `backend/Procfile`
  - Start command untuk platform Procfile-based.
- `backend/.env.production.example`
  - Template environment production.

## 3) README wajib

Sudah terpenuhi di `readme/README.md`:
- Deskripsi: ada.
- Fitur: ada.
- Tech stack: ada.
- Cara install: ada.
- Testing table: ada.
- Deployment section: ditambahkan.

## 4) Deployment execution plan

### Render
1. Push repository ke GitHub.
2. Hubungkan project ke Render.
3. Gunakan `render.yaml` sebagai blueprint deployment.
4. Isi `APP_URL` setelah URL service terbentuk (opsional saat first deploy).
5. Deploy.

Catatan:
- Blueprint Render saat ini menggunakan SQLite default agar deployment dapat langsung jalan tanpa setup MySQL eksternal.

### Railway
1. Import repository.
2. Gunakan `backend/Procfile` atau command setara.
3. Konfigurasi env var production.
4. Jalankan migrate force.

## 5) Production checklist

- Debug OFF: completed via env template (`APP_DEBUG=false`).
- APP_KEY aman: completed by design (disiapkan sebagai env, bukan hardcoded).
- Error handling user-friendly: completed (`errors/404.blade.php` dan `errors/500.blade.php`).

## 6) Status

Status Phase 6: Completed (deployment-ready).

Eksekusi deploy live masih memerlukan langkah user pada dashboard cloud (Render atau Railway) karena membutuhkan autentikasi akun.
