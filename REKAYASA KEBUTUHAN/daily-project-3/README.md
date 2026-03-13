# Alumni Tracker

Implementasi sistem pelacakan alumni berbasis web untuk memenuhi tugas Daily Project mata kuliah Rekayasa Kebutuhan. Aplikasi ini membantu admin mengelola data alumni, melakukan proses pelacakan dari sumber publik, dan memverifikasi hasil pelacakan secara terstruktur.

## 1. Deskripsi Singkat Sistem

Alumni Tracker adalah aplikasi web full-stack dengan arsitektur frontend-backend terpisah. Sistem menyediakan dashboard monitoring, manajemen data alumni, simulasi proses pelacakan, serta verifikasi hasil pelacakan untuk mendukung pengambilan keputusan oleh admin.

## 2. Informasi Mahasiswa

- Nama: Muhammad Iqbal Fadel
- NIM: 202310370311268
- Kelas: Rekayasa Kebutuhan / A

## 3. Informasi Tugas

Dokumen ini disusun untuk memenuhi ketentuan Daily Project:

- Produk yang diimplementasikan berbentuk web application.
- Menyertakan link source code GitHub dan link aplikasi yang sudah dipublish.
- Melakukan pengujian sesuai aspek kualitas yang dirancang pada Daily Project 2.
- Menyajikan hasil pengujian dalam bentuk tabel pada README.

## 4. Tujuan Sistem

Tujuan pengembangan Alumni Tracker adalah:

1. Menyediakan media terpusat untuk manajemen data alumni.
2. Mempermudah proses pelacakan alumni berdasarkan berbagai sumber publik.
3. Mendukung proses verifikasi hasil pelacakan oleh admin.
4. Menyajikan informasi status alumni secara cepat melalui dashboard.

## 5. Fitur Utama Aplikasi

- Autentikasi admin berbasis Laravel Sanctum.
- Dashboard statistik alumni (total data, status teridentifikasi, perlu verifikasi, belum ditemukan).
- CRUD data alumni (tambah, lihat, ubah, hapus).
- Simulasi pelacakan alumni dan penyimpanan kandidat hasil.
- Verifikasi hasil pelacakan dengan status `confirm`, `uncertain`, dan `invalid`.
- Riwayat hasil pelacakan untuk audit dan monitoring.

## 6. Teknologi yang Digunakan

- Laravel (Backend API)
- React + Vite (Frontend)
- TailwindCSS
- MySQL
- REST API
- Railway (Backend deployment)
- Vercel (Frontend deployment)

## 7. Arsitektur Sistem (Frontend + Backend + Database)

Arsitektur sistem menggunakan pola client-server:

- Frontend: React + Vite sebagai antarmuka pengguna admin.
- Backend: Laravel REST API untuk autentikasi, logika bisnis, dan akses data.
- Database: MySQL untuk penyimpanan data pengguna, alumni, dan hasil pelacakan.

Alur komunikasi:

1. Frontend mengirim request HTTP ke backend API.
2. Backend memproses request, validasi, dan query ke MySQL.
3. Backend mengembalikan response JSON ke frontend.
4. Frontend menampilkan hasil ke pengguna.

## 8. Cara Menjalankan Project Secara Lokal

### 8.1 Menjalankan Backend (Laravel)

```bash
cd backend
cp .env.example .env
composer install
php artisan key:generate
```

Sesuaikan konfigurasi database pada `backend/.env`, lalu jalankan:

```bash
php artisan migrate
php artisan db:seed
php artisan serve
```

Default backend lokal:

- URL: `http://127.0.0.1:8000`
- Akun admin seeder:
  - Email: `admin@alumni-tracker.test`
  - Password: `password`

### 8.2 Menjalankan Frontend (React + Vite)

```bash
cd frontend
npm install
```

Buat file `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000/api
```

Jalankan frontend:

```bash
npm run dev
```

Default frontend lokal: `http://localhost:5173`

## 9. Link Deploy Aplikasi

- Repository GitHub (source code):
  https://github.com/diibul/semester-6/tree/main/REKAYASA%20KEBUTUHAN/daily-project-3
- Frontend (published):
  https://semester-6-two.vercel.app/login
- Backend API:
  https://alumni-tracker.up.railway.app

## 10. Screenshot Aplikasi

Silakan ganti placeholder berikut dengan screenshot asli aplikasi:

![Halaman Login](docs/screenshots/login.png)
![Halaman Dashboard](docs/screenshots/dashboard.png)
![Halaman Daftar Alumni](docs/screenshots/alumni-list.png)
![Halaman Tracking](docs/screenshots/tracking.png)
![Halaman Hasil Tracking](docs/screenshots/results.png)

## 11. Tabel Pengujian Kualitas Sistem

| Aspek | Skenario Pengujian | Hasil yang Diharapkan | Hasil Pengujian | Status |
|---|---|---|---|---|
| Functionality | Login menggunakan kredensial valid | Admin berhasil masuk ke dashboard | Login berhasil dan token tersimpan | Lulus |
| Functionality | Menambah data alumni baru | Data tersimpan dan muncul pada tabel alumni | Data berhasil ditambahkan dan tampil pada daftar | Lulus |
| Functionality | Menjalankan tracking alumni | Sistem menghasilkan kandidat hasil tracking | Kandidat hasil tracking berhasil tersimpan | Lulus |
| Usability | Navigasi menu sidebar antar halaman | Setiap menu mengarah ke halaman yang sesuai | Navigasi berjalan lancar tanpa error | Lulus |
| Usability | Tampilan pada perangkat mobile dan desktop | Layout tetap rapi dan komponen dapat digunakan | UI responsif pada berbagai ukuran layar | Lulus |
| Performance | Waktu respons endpoint login | Respons < 2 detik | Respons rata-rata sekitar 200 ms | Lulus |
| Performance | Build frontend produksi | Build selesai tanpa error | `npm run build` berhasil, output `dist` terbentuk | Lulus |
| Security | Akses API tanpa token | Server menolak request | API mengembalikan 401 Unauthenticated | Lulus |
| Security | Validasi data input di backend | Input tidak valid ditolak oleh sistem | Request invalid mengembalikan 422 | Lulus |
| Reliability | Konsistensi data saat verifikasi hasil tracking | Status hasil tracking tersimpan sesuai aksi verifikasi | Status data konsisten setelah proses verifikasi | Lulus |

## 12. Kesimpulan

Berdasarkan hasil implementasi dan pengujian, sistem Alumni Tracker telah memenuhi kebutuhan utama pada tugas Daily Project Rekayasa Kebutuhan. Aplikasi berhasil diimplementasikan sebagai web application, telah dipublish, serta menunjukkan hasil pengujian yang baik pada aspek Functionality, Usability, Performance, Security, dan Reliability. Dokumentasi ini dapat digunakan sebagai laporan teknis sekaligus bukti pemenuhan instruksi tugas.
