# Laporan Mingguan — Minggu 7 & 8
## Advanced Normalization (UTS — Evaluasi I)

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Periode** | Minggu 7–8 (Bulan 2) |
| **Tanggal** | 19 Mei 2026 |
| **Status** | ✅ SELESAI |

---

## ✅ Capaian Minggu Ini

- [x] Membangun fungsi `slang_to_formal()` untuk normalisasi kata gaul
- [x] Flatten nested JSON dictionary menjadi lookup table
- [x] Menerapkan normalisasi huruf berulang (`wangiiii` → `wangi`)
- [x] Menghitung dictionary coverage sebelum & sesudah
- [x] Membuat demo perbandingan data mentah vs data bersih (untuk UTS)
- [x] Simpan hasil ke `data/processed/ulasan_parfum_processed.csv`

---

## 📊 Hasil Advanced Normalization

| Metrik | Nilai |
|---|---|
| Data input (dari interim) | 868 baris |
| Entri kamus slang | 168 entri |
| Coverage sebelum normalisasi | 0,56% (55/9.889 token) |
| Coverage sesudah normalisasi | 0,23% (token slang sudah diganti) |
| Data output | 868 baris (tidak ada penghapusan di tahap ini) |

### Catatan Coverage

> Coverage yang rendah (0,56%) menunjukkan bahwa dataset ini **dominan Bahasa Inggris** karena bersumber dari Google Review. Kata gaul Bahasa Indonesia seperti "bgt", "sis", "kak" tetap berhasil dinormalisasi.

### Contoh Transformasi

| Raw | Clean | Normalized |
|---|---|---|
| `Good long lasting smell. Staff were friendly!` | `good long lasting smell staff were friendly` | `good long lasting smell staff were friendly` |
| `Saff & co parfum ter the best 🫶🏻` | `saff co parfum ter the best` | `saff co parfum ter the best` |
| `Ok bgt` | `ok bgt` | `ok sangat` |

---

## 📁 Output

| File | Lokasi |
|---|---|
| `ulasan_parfum_processed.csv` | `data/processed/` |

---

## 📅 Rencana Minggu 9–10

- [ ] Keyword-based labeling (Positif / Negatif / Netral)
- [ ] Visualisasi distribusi label
