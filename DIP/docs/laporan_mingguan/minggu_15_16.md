# Laporan Mingguan — Minggu 15 & 16
## Final Submission (UAS — Evaluasi II)

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Periode** | Minggu 15–16 (Bulan 4) |
| **Tanggal** | Juni 2026 |
| **Status** | SELESAI |

---

## Capaian Minggu Ini

- [x] Audit akhir seluruh struktur folder dan kelengkapan file
- [x] Verifikasi semua skrip dapat dijalankan dari awal tanpa error
- [x] Finalisasi `README.md` — deskripsi, cara menjalankan, word cloud, timeline
- [x] Finalisasi `docs/jurnal/draft_jurnal.md`
- [x] Menyiapkan laporan mingguan lengkap (Minggu 1–16)
- [x] Push seluruh file ke repositori GitHub
- [x] Verifikasi GitHub: README terbaca, struktur folder rapi

---

## Checklist Final Submission

### Struktur Folder

| Folder/File | Ada? |
|---|---|
| `data/raw/ulasan_parfum_raw.csv` | Ya |
| `data/interim/ulasan_parfum_interim.csv` | Ya |
| `data/processed/ulasan_parfum_processed.csv` | Ya |
| `scripts/02_data_profiling/profiling.py` | Ya |
| `scripts/03_basic_cleaning/basic_cleaning.py` | Ya |
| `scripts/04_advanced_normalization/normalization.py` | Ya |
| `scripts/05_labeling/labeling.py` | Ya |
| `scripts/06_validation/validation.py` | Ya |
| `scripts/07_machine_learning/modelling.py` | Ya |
| `dictionary/slang_dictionary_parfum.json` | Ya |
| `results/figures/wordcloud_before.png` | Ya |
| `results/figures/wordcloud_after.png` | Ya |
| `results/figures/comparison_before_after.png` | Ya |
| `results/models/model_terbaik_naive_bayes.pkl` | Ya |
| `results/reports/sampel_validasi_manual.csv` | Ya |
| `docs/jurnal/draft_jurnal.md` | Ya |
| `docs/laporan_mingguan/minggu_01_02.md` | Ya |
| `docs/laporan_mingguan/minggu_03_04.md` | Ya |
| `docs/laporan_mingguan/minggu_05_06.md` | Ya |
| `docs/laporan_mingguan/minggu_07_08.md` | Ya |
| `docs/laporan_mingguan/minggu_09_10.md` | Ya |
| `docs/laporan_mingguan/minggu_11_12.md` | Ya |
| `docs/laporan_mingguan/minggu_13_14.md` | Ya |
| `docs/laporan_mingguan/minggu_15_16.md` | Ya (file ini) |
| `README.md` | Ya |
| `requirements.txt` | Ya |
| `config.py` | Ya |
| `run_pipeline.py` | Ya |

---

## Ringkasan Akhir Proyek

### Data

| Metrik | Nilai |
|---|---|
| Data mentah awal | 1.170 baris |
| Data valid setelah profiling | 1.122 baris |
| Data bersih setelah cleaning | 868 baris |
| Persentase data tersisa | 77,4% |
| Distribusi label (Positif / Netral / Negatif) | 87,1% / 11,9% / 1,0% |

### Pipeline

| Tahap | Skrip | Status |
|---|---|---|
| Data Profiling | `02_data_profiling/profiling.py` | Selesai |
| Basic Cleaning | `03_basic_cleaning/basic_cleaning.py` | Selesai |
| Advanced Normalization | `04_advanced_normalization/normalization.py` | Selesai |
| Labeling | `05_labeling/labeling.py` | Selesai |
| Validasi | `06_validation/validation.py` | Selesai |
| Machine Learning | `07_machine_learning/modelling.py` | Selesai |

### Hasil Model Terbaik

| Metrik | Nilai |
|---|---|
| Model | Multinomial Naive Bayes |
| Akurasi | 92,53% |
| F1-Macro | 0,7102 |
| F1-Weighted | 0,9227 |

---

## Bukti Pengumpulan

| Item | Keterangan |
|---|---|
| Link GitHub | https://github.com/diibul/semester-6/tree/main/DIP |
| Draft Jurnal | `docs/jurnal/draft_jurnal.md` |
| Dataset Final | `data/processed/ulasan_parfum_processed.csv` |
