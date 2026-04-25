# StudioBook

Platform web untuk booking studio musik yang terintegrasi dengan forum komunitas musik.

## Dokumen Roadmap

- Phase 1 (System Design): lihat `PHASE_1_SYSTEM_DESIGN.md`
- Phase 2 (Architecture & Setup): lihat `PHASE_2_ARCHITECTURE_SETUP.md`
- Phase 3 (Backend Engineering): lihat `PHASE_3_BACKEND_ENGINEERING.md`
- Phase 4 (Frontend Engineering): lihat `PHASE_4_FRONTEND_ENGINEERING.md`
- Phase 5 (Testing & QA): lihat `PHASE_5_TESTING_QA.md`
- Phase 6 (Deployment Engineering): lihat `PHASE_6_DEPLOYMENT_ENGINEERING.md`
- Phase 7 (Final Polish): lihat `PHASE_7_FINAL_POLISH.md`

## Deskripsi

Aplikasi ini dibangun dengan Laravel + React (Inertia.js) dan menggunakan MySQL sebagai database. Fokusnya adalah fitur MVP yang saling terhubung end-to-end: autentikasi, manajemen studio, booking jadwal dengan anti double booking, dan forum komunitas.

## Fitur

- Register, login, dan logout
- Menampilkan daftar studio dan detail studio
- Booking jadwal studio dengan validasi backend
- Anti double booking untuk jadwal yang sama
- Dummy payment dengan status booking `pending`, `paid`, dan `confirmed`
- Forum komunitas untuk membuat postingan dan komentar
- Seeder untuk data studio dan jadwal

## Teknologi

- Backend: Laravel
- Frontend: React + Inertia.js
- Database: MySQL (development), SQLite (default deployment Render)
- Styling: Tailwind CSS
- Authentication: Laravel Breeze (React)

## Instalasi

1. Install dependency PHP dan JavaScript.

```bash
cd backend
composer install

cd ../frontend
npm install
```

2. Salin file environment dan atur koneksi database MySQL.

```bash
cd ../backend
copy .env.example .env
php artisan key:generate
```

3. Jalankan migrasi dan seeder.

```bash
cd backend
php artisan migrate --seed
```

4. Jalankan aplikasi.

```bash
cd backend
php artisan serve

cd ../frontend
npm run dev
```

## Akun Demo

- Email: `test@example.com`
- Password: `password`

## Alur Fitur

### Authentication

- Register, login, logout menggunakan Breeze React.

### Studio Management

- Halaman studio menampilkan daftar studio dan detail jadwal.

### Booking System

- User memilih studio dan jadwal.
- Backend menolak booking jika jadwal sudah dipakai.
- Booking dibuat dengan status `pending`.
- Dummy payment mengubah status ke `paid`.
- Konfirmasi mengubah status ke `confirmed`.

### Forum Komunitas

- User dapat membuat postingan.
- User dapat membaca postingan dan memberi komentar.
- Input forum disanitasi di backend.

## Tabel Pengujian

| Fitur | Skenario | Hasil yang Diharapkan | Status |
| --- | --- | --- | --- |
| Login | Kredensial valid | User berhasil login dan masuk dashboard | OK |
| Login | Kredensial invalid | Login ditolak dan muncul error | OK |
| Booking | Jadwal tersedia | Booking tersimpan dengan status `pending` | OK |
| Booking | Double booking | Request ditolak oleh validasi backend | OK |
| Booking | Dummy payment | Status menjadi `paid` | OK |
| Booking | Konfirmasi booking | Status menjadi `confirmed` | OK |
| Forum | Buat postingan | Postingan tersimpan dan tampil di forum | OK |
| Forum | Buat komentar | Komentar tersimpan dan tampil pada post | OK |

## Catatan

- Jalankan `php artisan migrate --seed` setelah setup database.
- Pastikan MySQL aktif sebelum menjalankan aplikasi.

## Deployment

Artefak deployment yang sudah disiapkan:

- `render.yaml` di root project untuk deploy ke Render.
- `backend/Procfile` untuk platform yang mendukung Procfile (mis. Railway).
- `backend/.env.production.example` sebagai template env production.

### Deploy ke Render (recommended, fastest)

1. Push project ke GitHub.
2. Buat Web Service baru di Render dan pilih repository ini.
3. Render akan membaca `render.yaml` otomatis.
4. Lengkapi `APP_URL` setelah URL service Render terbentuk (opsional saat awal deploy).
5. Deploy dan verifikasi endpoint utama.

Catatan Render default:

- Konfigurasi saat ini menggunakan SQLite (`DB_CONNECTION=sqlite`) agar deploy cepat tanpa setup database eksternal.
- File database dibuat otomatis saat build di `backend/database/database.sqlite`.

### Deploy ke Railway (alternative)

1. Import project dari GitHub ke Railway.
2. Set start command berbasis `backend/Procfile` atau command setara.
3. Isi environment variables production mengacu ke `backend/.env.production.example`.
4. Jalankan migration production dengan `php artisan migrate --force`.

### Production checklist

- `APP_DEBUG=false`.
- `APP_KEY` aman (jangan hardcode di repository).
- Error page user-friendly tersedia (`backend/resources/views/errors/404.blade.php`, `backend/resources/views/errors/500.blade.php`).

## Final Polish

Pada phase terakhir ini dilakukan perapian UX dan consistency pass:

- Alur aksi booking dibuat lebih jelas dan mencegah aksi yang tidak valid dari sisi UI.
- Halaman error 404/500 dipoles agar konsisten dan lebih informatif.
- Final quality gate dijalankan ulang: build frontend sukses dan seluruh test backend lulus.
