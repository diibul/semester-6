# Laporan Mingguan — Minggu 11 & 12
## Validasi & Dokumentasi

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Periode** | Minggu 11–12 (Bulan 3) |
| **Tanggal** | 19 Mei 2026 |
| **Status** | ✅ SELESAI |

---

## ✅ Capaian Minggu Ini

- [x] Cek sisa noise pada data bersih (URL, hashtag, mention, angka)
- [x] Data Integrity Check (reduksi panjang, teks kosong, label)
- [x] Ambil 100 sampel untuk validasi manual
- [x] Buat Word Cloud setelah preprocessing
- [x] Buat grafik perbandingan panjang teks sebelum vs sesudah
- [x] Simpan laporan validasi lengkap

---

## 📊 Hasil Validasi

### Data Integrity Check

| Kriteria | Status |
|---|---|
| Reduksi panjang wajar (<50%) | ✅ YA (4,9%) |
| Tidak ada URL tersisa | ✅ YA (0) |
| Tidak ada hashtag tersisa | ✅ YA (0) |
| Tidak ada mention tersisa | ✅ YA (0) |
| Tidak ada angka tersisa | ✅ YA (0) |
| Tidak ada teks kosong | ✅ YA (0) |
| Semua baris berlabel | ✅ YA |

### Statistik Panjang Teks

| Metrik | Sebelum (Raw) | Sesudah (Bersih) |
|---|---|---|
| Rata-rata (char) | 64,2 | 61,1 |
| Min (char) | 10 | 9 |
| Max (char) | 336 | 322 |
| Reduksi | — | 4,9% |

> Reduksi yang rendah (4,9%) menunjukkan **proses cleaning TIDAK mengubah makna asli teks** — hanya menghapus simbol, angka, dan karakter khusus.

---

## 📁 Output

| File | Lokasi |
|---|---|
| `validation_report.txt` | `results/reports/` |
| `sampel_validasi_manual.csv` | `results/reports/` |
| `wordcloud_after.png` | `results/figures/` |
| `comparison_before_after.png` | `results/figures/` |
