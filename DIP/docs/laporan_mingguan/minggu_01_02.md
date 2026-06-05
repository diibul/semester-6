# Laporan Mingguan — Minggu 1 & 2
## Inisiasi & Akuisisi Data

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Periode** | Minggu 1–2 (Bulan 1) |
| **Tanggal** | Mei 2026 |

---

## ✅ Capaian Minggu Ini

### 1. Penentuan Niche & Topik
- **Topik**: Pembangunan Pipeline Preprocessing untuk Normalisasi Teks Bahasa Gaul pada Dataset Ulasan Parfum Lokal
- **Sumber Data**: Ulasan dari platform Google Review dan Twitter/X bertema parfum lokal Indonesia
- **Domain Khusus**: Parfum lokal — kata gaul seperti "bgt", "wanginya", "rekomen", "worth it", "longlasting", dll.

### 2. Akuisisi Dataset
- ✅ Dataset awal diperoleh: `review_parfum_clean.csv`
- ✅ Jumlah baris: lebih dari 1.000 baris (memenuhi syarat minimal)
- ✅ Dipindahkan ke folder `data/raw/` sesuai struktur proyek

### 3. Pembangunan Struktur Proyek
- ✅ Seluruh folder proyek dibuat (data, scripts, dictionary, docs, results)
- ✅ File konfigurasi global (`config.py`) dibuat
- ✅ Requirements library Python (`requirements.txt`) dibuat
- ✅ README.md profesional dibuat
- ✅ Slang Dictionary awal domain parfum dibuat (120+ entri)

---

## 📁 Dataset Mentah

| Atribut | Detail |
|---|---|
| Nama file | `review_parfum_clean.csv` |
| Lokasi | `data/raw/` |
| Sumber | Google Review / Twitter/X |
| Format | CSV (UTF-8) |
| Estimasi baris | >1.000 |

---

## 🔍 Observasi Awal Dataset

Setelah melihat sekilas dataset:
- Terdapat teks dengan bahasa gaul seperti: "wanginya bgt", "rekomen bgt", "ga worth"
- Terdapat emoji dalam beberapa baris
- Ada potensi duplikat dan teks yang sangat pendek
- Bahasa campuran (Indonesia + Inggris): "long lasting", "worth it", "packaging"

---

## 📅 Rencana Minggu 3–4

- [ ] Jalankan `scripts/02_data_profiling/profiling.py`
- [ ] Hitung persentase duplikat
- [ ] Identifikasi kata gaul paling sering muncul (Top 30)
- [ ] Identifikasi noise: emoji, URL, mention, angka
- [ ] Buat laporan profiling lengkap

---

## 📚 Referensi Jurnal

- Utama: [Springer — E-Commerce Review NLP](https://link.springer.com/article/10.1007/s10660-022-09582-4)
