# Laporan Mingguan — Minggu 3 & 4
## Data Profiling

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Periode** | Minggu 3–4 (Bulan 1) |
| **Tanggal** | 19 Mei 2026 |
| **Status** | ✅ SELESAI |

---

## ✅ Capaian Minggu Ini

- [x] Menjalankan skrip `scripts/02_data_profiling/profiling.py`
- [x] Menghitung persentase data duplikat
- [x] Mengidentifikasi kata gaul paling sering muncul
- [x] Mengidentifikasi berbagai jenis noise dalam data
- [x] Membuat 6 visualisasi otomatis (grafik & word cloud)
- [x] Menyimpan laporan ke `results/reports/profiling_report.txt`

---

## 📊 Hasil Data Profiling

### Ringkasan Dataset

| Metrik | Nilai |
|---|---|
| **Total baris raw** | 1.170 baris |
| **Baris noise struktural dibuang** | 48 baris (baris kosong, header palsu, dll.) |
| **Data valid tersisa** | **1.122 baris** ✅ (memenuhi syarat >1.000) |
| **Kolom** | USERNAME, TIME, REVIEW |
| **Delimiter CSV** | Semicolon (`;`) |

### 1. Duplikat

| Metrik | Nilai |
|---|---|
| Jumlah duplikat | **199 baris** |
| Persentase | **17,74%** dari data valid |
| → Perlu dihapus pada tahap Basic Cleaning |

### 2. Missing Values

| Kolom | Missing | Persen |
|---|---|---|
| USERNAME | 8 | 0,71% |
| TIME | 11 | 0,98% |
| REVIEW | 149 | 13,28% |

### 3. Statistik Panjang Teks

| Metrik | Karakter | Kata |
|---|---|---|
| Rata-rata | 58,6 | 10,1 |
| Minimum | 2 | 1 |
| Maximum | 336 | 66 |
| Median | 45,0 | 8,0 |

### 4. Noise Detection

| Jenis Noise | Jumlah | Persen |
|---|---|---|
| Mengandung URL | 1 | 0,1% |
| Mengandung Hashtag (#) | 0 | 0,0% |
| Mengandung Mention (@) | 0 | 0,0% |
| Mengandung Emoji | 0 | 0,0% |
| Mengandung Angka | 46 | 4,1% |
| Teks Sangat Pendek (<10 char) | 46 | 4,1% |
| Teks Sangat Panjang (>500) | 0 | 0,0% |

### 5. Top 10 Kata Paling Sering Muncul

| Rank | Kata | Frekuensi |
|---|---|---|
| 1 | best | 95 |
| 2 | helpful | 83 |
| 3 | smells | 80 |
| 4 | long | 77 |
| 5 | here | 63 |
| 6 | love | 44 |
| 7 | lasting | 43 |
| 8 | fragrance | 43 |
| 9 | buy | 41 |
| 10 | like | 41 |

### 6. Kata Gaul / Informal yang Ditemukan

| Kata | Frekuensi | Catatan |
|---|---|---|
| worth | 13 | "worth it" → domain parfum |
| sis | 13 | sapaan informal |
| mba | 5 | sapaan informal |
| bro | 4 | sapaan informal |
| kak | 4 | sapaan informal |
| bgt | 3 | "banget" → intensifier |
| mbak | 3 | sapaan informal |
| mantap | 1 | ekspresi positif |
| viral | 1 | tren sosmed |
| fomo | 1 | fear of missing out |

---

## 🔍 Observasi & Insight

> **Dataset dominan Bahasa Inggris** karena bersumber dari Google Review HMNS dan Saff&Co outlet. Banyak reviewer internasional (Malaysia, dll.) memberikan ulasan dalam Bahasa Inggris.

> **Kata gaul relatif sedikit** dibanding yang diharapkan, namun kata-kata domain parfum seperti "worth", "long lasting", "smells", "fragrance" sangat relevan untuk Slang Dictionary.

> **17,74% duplikat** adalah angka yang cukup signifikan — berasal dari reviewer yang memberikan ulasan sama di beberapa outlet berbeda.

---

## 📁 Output yang Dihasilkan

| File | Lokasi |
|---|---|
| `profiling_report.txt` | `results/reports/` |
| `top_kata_raw.png` | `results/figures/` |
| `top_kata_gaul.png` | `results/figures/` |
| `noise_overview.png` | `results/figures/` |
| `distribusi_panjang_teks.png` | `results/figures/` |
| `distribusi_waktu.png` | `results/figures/` |
| `wordcloud_before.png` | `results/figures/` |

---

## 📅 Rencana Minggu 5–6 (Basic Cleaning)

- [ ] Jalankan `scripts/03_basic_cleaning/basic_cleaning.py`
- [ ] Case folding (lowercase semua)
- [ ] Hapus URL, angka, karakter khusus
- [ ] Hapus duplikat (199 baris)
- [ ] Filter teks terlalu pendek (<10 karakter) — 46 baris
- [ ] Simpan hasil ke `data/interim/ulasan_parfum_interim.csv`
