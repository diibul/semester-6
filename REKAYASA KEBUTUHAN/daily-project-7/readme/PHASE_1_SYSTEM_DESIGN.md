# Phase 1 - System Design Validation

Dokumen ini menutup seluruh kebutuhan pada Phase 1 roadmap: use case, flow, schema, enum, relasi, dan boundary MVP.

## 1) Use Case Refinement

### Aktor
- Musisi atau User
- Owner Studio
- Sistem

### Use case per aktor
- Musisi atau User
  - Register akun
  - Login dan logout
  - Browse daftar studio
  - Lihat detail studio dan jadwal
  - Buat booking
  - Lakukan dummy payment
  - Konfirmasi status booking milik sendiri
  - Buat post forum
  - Buat komentar forum
- Owner Studio (MVP saat ini masih satu peran user, tanpa panel owner terpisah)
  - Melihat data studio (public)
  - Konfirmasi booking (diimplementasikan pada booking milik user terkait)
- Sistem
  - Validasi input
  - Cegah double booking
  - Kelola transisi status booking
  - Proteksi route berbasis auth middleware

### Boundary MVP (yang tidak dikerjakan)
- Review studio
- Upload gambar studio atau post
- Moderasi forum tingkat lanjut
- Role management owner terpisah
- Payment gateway real

## 2) Flow System

### Auth flow
1. User register.
2. User login.
3. Session dipertahankan oleh Laravel auth.
4. Route protected hanya bisa diakses user login.

### Booking flow
1. User browse studio.
2. User buka detail studio.
3. User pilih schedule.
4. User submit booking.
5. Sistem lock schedule pada transaksi DB.
6. Sistem menolak jika schedule sudah dipakai atau tidak available.
7. Booking tersimpan status pending dan payment unpaid.
8. User jalankan dummy payment, status menjadi paid.
9. User konfirmasi booking, status menjadi confirmed.

### Forum flow
1. User membuat post.
2. User melihat daftar post.
3. User membuat komentar.
4. Edit atau delete masih opsional dan belum diaktifkan.

## 3) Database Schema (ERD tekstual)

### Tabel wajib
- users
- studios
- schedules
- bookings
- forum_posts
- comments

### Foreign key
- schedules.studio_id -> studios.id
- bookings.user_id -> users.id
- bookings.studio_id -> studios.id
- bookings.schedule_id -> schedules.id
- forum_posts.user_id -> users.id
- comments.forum_post_id -> forum_posts.id
- comments.user_id -> users.id

### Constraint penting
- schedules: unique studio_id + schedule_date + start_time + end_time
- bookings: unique schedule_id (anti double booking tingkat database)

### Index
- studio_id: tercakup pada foreign key relasi
- schedule_date: ditambahkan index khusus
- booking_status: ditambahkan index khusus
- payment_status: ditambahkan index tambahan untuk filter status pembayaran

## 4) Enum dan aturan transisi

### booking_status
- pending -> paid -> confirmed

### payment_status
- unpaid -> paid

### Aturan transisi
- Booking baru selalu pending dan unpaid.
- Aksi dummy payment mengubah payment_status ke paid dan booking_status ke paid.
- Aksi confirm hanya valid jika payment_status sudah paid.

## 5) Relationship validation

- 1 user -> banyak booking: terpenuhi
- 1 studio -> banyak jadwal: terpenuhi
- 1 post -> banyak komentar: terpenuhi

## 6) Hasil validasi Phase 1

Status: Completed

Semua poin wajib pada Phase 1 sudah terpenuhi setelah:
- verifikasi flow dan boundary MVP,
- dokumentasi system design formal,
- penambahan index yang diminta roadmap untuk kebutuhan query.
