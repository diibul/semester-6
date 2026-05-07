# 🎵 StudioBook

**Platform booking studio musik dengan forum komunitas terintegrasi.**

---

**Muhammad Iqbal Fadel** — 202310370311268

## 🔗 Links

| | URL |
|---|---|
| **GitHub** | [github.com/diibul/semester-6](https://github.com/diibul/semester-6/tree/main/REKAYASA%20KEBUTUHAN/daily-project-7) |
| **Live Website** | [studiobook.infinityfreeapp.com](http://studiobook.infinityfreeapp.com) |

---

## Tentang Project

StudioBook adalah aplikasi web untuk memudahkan proses booking studio musik secara online. Dilengkapi dengan sistem anti double-booking, payment flow, dan forum komunitas untuk interaksi antar musisi.

## Fitur Utama

- **Authentication** — Register, login, logout (Laravel Breeze)
- **Studio Management** — Daftar studio, detail, dan jadwal ketersediaan
- **Booking System** — Booking jadwal dengan anti double-booking dan payment flow (`pending` → `paid` → `confirmed`)
- **Forum Komunitas** — Buat postingan dan komentar antar pengguna

## Tech Stack

| Layer | Teknologi |
|-------|-----------|
| Backend | Laravel 12 (PHP 8.2+) |
| Frontend | React + Inertia.js |
| Styling | Tailwind CSS |
| Database | MySQL |
| Auth | Laravel Breeze |

## Struktur Project

```
daily-project-7/
├── backend/          # Laravel API + Inertia server
├── frontend/         # React components + pages
├── deploy/           # Deployment scripts & config
└── readme/           # Dokumentasi project
```

## Quick Start

```bash
# 1. Install dependencies
cd backend && composer install
cd ../frontend && npm install

# 2. Setup environment
cd ../backend
cp .env.example .env
php artisan key:generate

# 3. Database
php artisan migrate --seed

# 4. Jalankan
php artisan serve          # Terminal 1
cd ../frontend && npm run dev   # Terminal 2
```

**Akun Demo:** `test@example.com` / `password`
