# Laporan Mingguan — Minggu 9 & 10
## Domain-Specific Labeling

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Periode** | Minggu 9–10 (Bulan 3) |
| **Tanggal** | 19 Mei 2026 |
| **Status** | ✅ SELESAI |

---

## ✅ Capaian Minggu Ini

- [x] Membuat keyword list Positif (50 kata) dan Negatif (38 kata)
- [x] Menerapkan keyword-based labeling pada 868 baris
- [x] Membuat visualisasi distribusi label (pie chart + bar chart)
- [x] Menyimpan dataset berlabel ke `data/processed/`

---

## 📊 Hasil Labeling

| Label | Jumlah | Persentase |
|---|---|---|
| **Positif** | 756 | 87,1% |
| **Netral** | 103 | 11,9% |
| **Negatif** | 9 | 1,0% |
| **Total** | **868** | **100%** |

### Analisis Distribusi

> Label **Positif dominan (87,1%)** karena dataset berasal dari Google Review toko parfum yang umumnya dikunjungi pelanggan puas. Ini konsisten dengan karakteristik ulasan Google yang cenderung positif.

> **9 ulasan Negatif** mengandung keluhan seperti: parfum tidak tahan lama, kemasan bocor, dan harga tidak sepadan.

> **103 ulasan Netral** tidak mengandung keyword positif maupun negatif yang signifikan (misal: "Good morning", "Okay").

---

## 📁 Output

| File | Lokasi |
|---|---|
| `ulasan_parfum_processed.csv` (+ kolom label) | `data/processed/` |
| `distribusi_label.png` | `results/figures/` |
