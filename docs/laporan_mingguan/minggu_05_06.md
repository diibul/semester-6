# Laporan Mingguan — Minggu 5 & 6
## Basic Cleaning Pipeline

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Periode** | Minggu 5–6 (Bulan 2) |
| **Tanggal** | 19 Mei 2026 |
| **Status** | ✅ SELESAI |

---

## ✅ Capaian Minggu Ini

- [x] Case folding (lowercase semua teks)
- [x] Hapus URL, hashtag, mention
- [x] Hapus karakter khusus & tanda baca
- [x] Hapus angka
- [x] Normalisasi huruf berulang (waaangi → waangi)
- [x] Filter teks terlalu pendek (<10 char)
- [x] Hapus duplikat
- [x] Simpan hasil ke `data/interim/ulasan_parfum_interim.csv`

---

## 📊 Hasil Basic Cleaning

| Metrik | Nilai |
|---|---|
| Data awal (valid) | 1.122 baris |
| Difilter (panjang <10 char) | -204 baris |
| Difilter (kosong) | -0 baris |
| Duplikat dihapus | -50 baris |
| **Data akhir** | **868 baris (77,4% tersisa)** |
| Rata-rata panjang | 61,1 karakter |
| Rata-rata kata | 11,4 kata per ulasan |

### Contoh Transformasi

| Sebelum (Raw) | Sesudah (Clean) |
|---|---|
| `Good long lasting smell. Staff were friendly!` | `good long lasting smell staff were friendly` |
| `Saff & co parfum ter the best 🫶🏻 …` | `saff co parfum ter the best` |
| `Good products!` | `good products` |

---

## 📁 Output

| File | Lokasi |
|---|---|
| `ulasan_parfum_interim.csv` | `data/interim/` |

---

## 📅 Rencana Minggu 7–8 (Advanced Normalization + UTS)

- [ ] Jalankan `scripts/04_advanced_normalization/normalization.py`
- [ ] Slang-to-Formal menggunakan dictionary
- [ ] Demo perbandingan data mentah vs data bersih (untuk UTS)
- [ ] Hitung dictionary coverage
