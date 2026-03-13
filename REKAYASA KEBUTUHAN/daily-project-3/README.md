# Sistem Pelacakan Alumni Berbasis Banyak Sumber Publik

Implementasi full-stack modern untuk tugas mata kuliah Rekayasa Kebutuhan.

Sistem ini mempertahankan konsep asli: membantu admin melacak data alumni dari berbagai sumber publik, memverifikasi status terkini, dan menyimpan riwayat pelacakan.

## Link Proyek

- Repository GitHub: https://github.com/diibul/semester-6
- Web aplikasi (published): https://semester-6-two.vercel.app/login
- API backend (Railway): https://alumni-tracker.up.railway.app

## Identitas Mahasiswa

- Nama: Muhammad Iqbal Fadel
- NIM: 202310370311268
- Kelas: Rekayasa Kebutuhan / A

## Deskripsi Proyek

Aplikasi mendukung alur utama berikut:

- Autentikasi admin menggunakan token API Laravel Sanctum.
- Manajemen data alumni (tambah, lihat, ubah, hapus).
- Simulasi pelacakan alumni dari banyak kategori sumber publik.
- Proses verifikasi kandidat hasil pelacakan oleh admin.
- Penyimpanan riwayat pelacakan dan statistik dashboard.

## Arsitektur Sistem

Struktur implementasi saat ini:

```text
daily-project-3
├── backend            # Laravel 12 REST API
└── frontend           # Dashboard React + Vite
```

Arsitektur logis:

- Backend: Laravel 12, REST API, Sanctum, MVC + Service Layer.
- Frontend: React (Vite), TailwindCSS, React Router, Axios.
- Database: MySQL.

## Teknologi yang Digunakan

### Backend

- Laravel 12
- PHP 8.2+
- Laravel Sanctum
- MySQL

### Frontend

- React 19 + Vite
- TailwindCSS
- React Router
- Axios

## Fitur Utama

- Ringkasan dashboard: total alumni, alumni terlacak, perlu verifikasi, belum ditemukan.
- Tabel manajemen alumni dengan badge status dan aksi (Lihat, Ubah, Hapus, Lacak).
- Endpoint simulasi pelacakan untuk membuat query dan kandidat hasil.
- Endpoint verifikasi hasil dengan aksi:
  - confirm -> Teridentifikasi
  - uncertain -> Perlu Verifikasi
  - invalid -> Belum Ditemukan
- Halaman riwayat hasil pelacakan dengan pembaruan status verifikasi.

## Instruksi Instalasi

## 1) Setup Backend

```bash
cd backend
cp .env.example .env
composer install
php artisan key:generate
```

Atur kredensial MySQL pada file `.env`, lalu jalankan:

```bash
php artisan migrate
php artisan db:seed
php artisan serve
```

Admin default hasil seeder:

- Email: `admin@alumni-tracker.test`
- Password: `password`

URL backend default: `http://127.0.0.1:8000`

## 2) Setup Frontend

```bash
cd frontend
npm install
```

Buat file `.env` di frontend (opsional jika pakai default):

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

Jalankan server development:

```bash
npm run dev
```

URL frontend default: `http://localhost:5173`

## Variabel Lingkungan

### Backend (`backend/.env`)

- `APP_NAME`
- `APP_ENV`
- `APP_KEY`
- `APP_URL`
- `FRONTEND_URL`
- `DB_CONNECTION`
- `DB_HOST`
- `DB_PORT`
- `DB_DATABASE`
- `DB_USERNAME`
- `DB_PASSWORD`

### Frontend (`frontend/.env`)

- `VITE_API_URL`

## Dokumentasi API

Base URL: `http://127.0.0.1:8000/api`

### Autentikasi

- `POST /login`
- `POST /logout` (butuh autentikasi)
- `GET /me` (butuh autentikasi)

### Alumni

- `GET /alumni` (mendukung `page`, `search`)
- `POST /alumni`
- `GET /alumni/{id}`
- `PUT /alumni/{id}`
- `DELETE /alumni/{id}`

### Tracking

- `POST /tracking/{alumni_id}`

Proses yang diimplementasikan:

1. Memuat data alumni.
2. Membuat query pencarian.
3. Menjalankan simulasi hasil dari sumber publik.
4. Menghasilkan kandidat hasil dengan confidence score.
5. Menyimpan kandidat ke riwayat pelacakan.
6. Mengubah status alumni menjadi `Perlu Verifikasi`.

### Verifikasi Hasil

- `GET /results`
- `GET /results/{id}`
- `PUT /results/{id}/verify`

Contoh body request:

```json
{
  "action": "confirm"
}
```

Aksi yang diperbolehkan:

- `confirm`
- `uncertain`
- `invalid`

### Dashboard

- `GET /dashboard`

Respons berisi:

- `total_alumni`
- `tracked_alumni`
- `teridentifikasi`
- `perlu_verifikasi`
- `belum_ditemukan`

## Skema Database

### users

- id
- name
- email
- password
- role
- created_at
- updated_at

### alumni

- id
- name
- nim
- study_program
- graduation_year
- email
- tracking_status
- created_at
- updated_at

### tracking_results

- id
- alumni_id
- source
- title
- description
- url
- confidence_score
- status
- tracked_at
- created_at

Relasi:

- Alumni hasMany TrackingResults
- TrackingResult belongsTo Alumni

## Screenshots

Tambahkan screenshot setelah aplikasi dijalankan:

- Halaman Login
- Halaman Dashboard
- Halaman Daftar Alumni
- Halaman Simulasi Tracking
- Halaman Hasil Tracking

## Pengujian

Jalankan test backend:

```bash
cd backend
php artisan test
```

Jalankan pengecekan build frontend:

```bash
cd frontend
npm run build
```

### Tabel Pengujian Aspek Kualitas

Pengujian dilakukan secara manual terhadap aplikasi yang berjalan di lingkungan lokal (`http://127.0.0.1:8000` untuk backend dan `http://localhost:5174` untuk frontend).

#### 1. Fungsionalitas (Functionality)

| No | Skenario Uji | Langkah Uji | Hasil yang Diharapkan | Hasil Aktual | Status |
|---|---|---|---|---|---|
| F-01 | Login dengan kredensial valid | Masukkan email `admin@alumni-tracker.test` dan password `password`, klik Login | Berhasil masuk, token tersimpan, diarahkan ke Dashboard | Berhasil masuk dan diarahkan ke Dashboard | ✅ Lulus |
| F-02 | Login dengan kredensial tidak valid | Masukkan email/password yang salah, klik Login | Muncul pesan error "Invalid credentials" | Muncul pesan error dengan status 401 | ✅ Lulus |
| F-03 | Tambah data alumni baru | Isi form tambah alumni (nama, NIM, prodi, tahun lulus, email), klik Simpan | Data tersimpan, muncul di daftar alumni | Data berhasil tersimpan di database | ✅ Lulus |
| F-04 | Tambah alumni dengan NIM duplikat | Isi form dengan NIM yang sudah ada, klik Simpan | Muncul pesan error validasi NIM sudah digunakan | Muncul error validasi dari server | ✅ Lulus |
| F-05 | Lihat daftar alumni | Buka halaman Daftar Alumni | Menampilkan tabel berisi semua data alumni dengan pagination | Tabel alumni tampil dengan data dan pagination | ✅ Lulus |
| F-06 | Cari alumni berdasarkan nama | Ketik nama di kolom pencarian | Tabel hanya menampilkan alumni yang nama/NIM-nya mengandung kata kunci | Hasil pencarian sesuai kata kunci | ✅ Lulus |
| F-07 | Edit data alumni | Klik tombol Edit pada salah satu alumni, ubah data, klik Simpan | Data alumni terupdate, perubahan tersimpan | Data berhasil diperbarui | ✅ Lulus |
| F-08 | Hapus data alumni | Klik tombol Hapus pada salah satu alumni | Data alumni terhapus dari daftar dan database | Data berhasil dihapus | ✅ Lulus |
| F-09 | Jalankan tracking alumni | Klik tombol Lacak pada salah satu alumni | Sistem menghasilkan kandidat hasil tracking, status alumni berubah menjadi "Perlu Verifikasi" | Hasil tracking tersimpan, status alumni berubah | ✅ Lulus |
| F-10 | Verifikasi hasil tracking — Konfirmasi | Pada halaman Hasil Tracking, klik tombol Konfirmasi | Status hasil tracking berubah menjadi "Teridentifikasi" | Status berhasil diubah menjadi Teridentifikasi | ✅ Lulus |
| F-11 | Verifikasi hasil tracking — Tidak Pasti | Klik tombol Tidak Pasti pada hasil tracking | Status berubah menjadi "Perlu Verifikasi" | Status berhasil diubah | ✅ Lulus |
| F-12 | Verifikasi hasil tracking — Tidak Valid | Klik tombol Tidak Valid pada hasil tracking | Status berubah menjadi "Belum Ditemukan" | Status berhasil diubah | ✅ Lulus |
| F-13 | Lihat statistik dashboard | Buka halaman Dashboard | Menampilkan total alumni, alumni terlacak, perlu verifikasi, dan belum ditemukan | Semua statistik tampil dengan benar | ✅ Lulus |
| F-14 | Logout | Klik tombol Logout | Token dihapus, pengguna diarahkan ke halaman Login | Berhasil logout dan diarahkan ke Login | ✅ Lulus |
| F-15 | Akses halaman tanpa login | Akses langsung URL `/dashboard` tanpa login | Diarahkan kembali ke halaman Login | Diarahkan ke halaman Login | ✅ Lulus |

#### 2. Kegunaan (Usability)

| No | Skenario Uji | Langkah Uji | Hasil yang Diharapkan | Hasil Aktual | Status |
|---|---|---|---|---|---|
| U-01 | Navigasi antar halaman | Klik setiap item menu di sidebar | Berpindah ke halaman yang sesuai tanpa error | Navigasi berjalan lancar | ✅ Lulus |
| U-02 | Tampilan responsif pada layar lebar (≥1280px) | Buka aplikasi di monitor 1920x1080 | Layout sidebar + konten tampil rapi | Layout tampil sesuai desain | ✅ Lulus |
| U-03 | Feedback status badge alumni | Lihat kolom status pada daftar alumni | Badge berwarna berbeda untuk setiap status (Belum Dilacak, Perlu Verifikasi, Teridentifikasi, Belum Ditemukan) | Badge tampil dengan warna yang sesuai | ✅ Lulus |
| U-04 | Pesan validasi form | Kirim form kosong tanpa mengisi field wajib | Muncul pesan error spesifik untuk setiap field yang kosong | Pesan validasi tampil per field | ✅ Lulus |
| U-05 | Indikator loading saat fetch data | Buka halaman yang memuat data dari API | Tampil indikator loading selama proses fetch | Loading state tampil sebelum data muncul | ✅ Lulus |

#### 3. Keamanan (Security)

| No | Skenario Uji | Langkah Uji | Hasil yang Diharapkan | Hasil Aktual | Status |
|---|---|---|---|---|---|
| S-01 | Akses API tanpa token | Kirim request `GET /api/alumni` tanpa header Authorization | Server menolak dengan status 401 Unauthorized | Mengembalikan 401 Unauthenticated | ✅ Lulus |
| S-02 | Akses API dengan token tidak valid | Kirim request dengan token palsu/expired | Server menolak dengan status 401 Unauthorized | Mengembalikan 401 Unauthenticated | ✅ Lulus |
| S-03 | Token dihapus saat logout | Lakukan logout, lalu coba akses API dengan token lama | Token tidak lagi valid setelah logout | Token direvoke, akses ditolak | ✅ Lulus |
| S-04 | Validasi input server-side | Kirim data alumni dengan graduation_year berupa string teks | Server menolak dengan pesan validasi | Mengembalikan 422 Unprocessable Entity | ✅ Lulus |
| S-05 | Password di-hash di database | Cek kolom password di tabel users setelah seeder | Password tidak tersimpan sebagai plain text | Tersimpan sebagai bcrypt hash | ✅ Lulus |

#### 4. Performa (Performance)

| No | Skenario Uji | Langkah Uji | Hasil yang Diharapkan | Hasil Aktual | Status |
|---|---|---|---|---|---|
| P-01 | Waktu respons endpoint login | Ukur waktu `POST /api/login` | Respons diterima dalam < 2 detik | ~200ms (lokal) | ✅ Lulus |
| P-02 | Waktu respons daftar alumni | Ukur waktu `GET /api/alumni` dengan 10 data | Respons diterima dalam < 1 detik | ~100ms (lokal) | ✅ Lulus |
| P-03 | Waktu eksekusi simulasi tracking | Ukur waktu `POST /api/tracking/{id}` | Proses selesai dalam < 3 detik | ~300ms (simulasi lokal) | ✅ Lulus |
| P-04 | Build frontend berhasil | Jalankan `npm run build` di folder frontend | Build selesai tanpa error, menghasilkan folder `dist` | Build berhasil, 0 error | ✅ Lulus |

#### 5. Keandalan (Reliability)

| No | Skenario Uji | Langkah Uji | Hasil yang Diharapkan | Hasil Aktual | Status |
|---|---|---|---|---|---|
| R-01 | Konsistensi hasil tracking | Tracking alumni yang sama dua kali berturut-turut | Menghasilkan kandidat hasil baru setiap kali, riwayat tersimpan semua | Setiap tracking menghasilkan data baru dan tersimpan | ✅ Lulus |
| R-02 | Integritas data saat hapus alumni | Hapus alumni yang memiliki riwayat tracking | Data alumni dan semua tracking result terkait terhapus | Data terhapus dengan cascade | ✅ Lulus |
| R-03 | Penanganan request tidak valid | Kirim `PUT /api/alumni/9999` (ID tidak ada) | Server mengembalikan 404 Not Found | Mengembalikan 404 | ✅ Lulus |

## Deployment

### Frontend (Vercel)

- Root directory: `frontend`
- Build command: `npm run build`
- Output directory: `dist`
- Environment variable: `VITE_API_URL=https://alumni-tracker.up.railway.app/api`

URL produksi frontend: `https://semester-6-two.vercel.app/login`

### Backend (Render / Railway)

- Root directory: `backend`
- Build command: `composer install --no-dev --optimize-autoloader`
- Start command: `php artisan serve --host 0.0.0.0 --port $PORT`
- Gunakan MySQL terkelola dan isi env database
- Pastikan `APP_ENV=production`, `APP_DEBUG=false`, `APP_KEY` valid

URL produksi backend: `https://alumni-tracker.up.railway.app`

## Checklist Deliverables

- Laravel API backend: selesai
- React dashboard frontend: selesai
- Skema MySQL + migrasi: selesai
- README + dokumentasi API + panduan deployment: selesai
- Siap untuk pengumpulan tugas akademik
