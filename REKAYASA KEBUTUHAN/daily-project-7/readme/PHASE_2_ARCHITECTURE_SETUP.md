# Phase 2 - Architecture and Tech Setup Validation

Dokumen ini memvalidasi seluruh poin Phase 2 roadmap setelah struktur project dipisah menjadi frontend, backend, dan readme.

## 1) Arsitektur

Arsitektur yang digunakan:

Client (Browser)
-> React (Inertia)
-> Laravel Controller
-> Model (Eloquent)
-> Database

Implementasi saat ini:
- Backend Laravel berada di folder `backend`.
- Frontend React + Vite berada di folder `frontend`.
- Inertia sebagai bridge antara backend dan frontend tetap aktif.

## 2) Status output wajib Phase 2

### Repo Git siap
- Valid: project terdeteksi sebagai git working tree.

### Laravel + Inertia + React + Breeze jalan
- Valid: dependency backend mencakup `inertiajs/inertia-laravel` dan `laravel/breeze`.
- Valid: frontend mencakup `@inertiajs/react`, `react`, dan `vite`.
- Valid: route auth dan route aplikasi utama tersedia.

### Database terkoneksi
- Valid: migrasi berjalan sukses.
- Valid: konfigurasi database tersedia untuk sqlite dan mysql.

### Vite + hot reload stabil
- Valid: build frontend sukses dan output assets ke `backend/public/build`.
- Valid: script dev backend sudah disesuaikan untuk menjalankan Vite dari folder frontend.

## 3) Checklist setup

- Install PHP + Composer: terpenuhi (project Laravel berjalan).
- Install Node.js: terpenuhi (frontend build berhasil).
- Install MySQL: siap konfigurasi melalui env (opsional aktif di lokal).
- Setup Git: terpenuhi.
- Install Laravel: terpenuhi.
- Setup .env: terpenuhi.
- Setup database: terpenuhi.
- Install Inertia: terpenuhi.
- Install React: terpenuhi.
- Install Breeze auth: terpenuhi.
- Vite running + hot reload: terpenuhi.
- Error handling terlihat jelas (dev): terpenuhi melalui `APP_DEBUG=true` pada konfigurasi development.

## 4) Penyesuaian teknis penting setelah split folder

Perubahan agar workflow tetap stabil:
- `backend/composer.json` script `setup` kini menjalankan npm install dan build pada `../frontend`.
- `backend/composer.json` script `dev` kini menjalankan Vite dev server pada `../frontend`.
- `frontend/vite.config.js` mengarah ke output publik backend (`../backend/public`).
- `frontend/tailwind.config.js` membaca blade templates dari folder backend.

## 5) Cara menjalankan

Backend:
- `cd backend`
- `composer install`
- `php artisan key:generate`
- `php artisan migrate --seed`
- `php artisan serve`

Frontend:
- `cd frontend`
- `npm install`
- `npm run dev`

Alternatif satu command dari backend:
- `cd backend`
- `composer run dev`

## 6) Kesimpulan

Status Phase 2: Completed.

Seluruh output wajib dan checklist utama pada Phase 2 telah tervalidasi dan sudah disesuaikan dengan struktur project terbaru.
