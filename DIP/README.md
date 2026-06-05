# 🌸 Pipeline Preprocessing & Klasifikasi Sentimen Ulasan Parfum Lokal

> **Tugas Besar — Mata Kuliah Data, Informasi, dan Pengetahuan**  
> Program Studi Informatika | Universitas Muhammadiyah Malang  

---

## 👤 Identitas Mahasiswa

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Kelas** | Data, Informasi dan Pengetahuan / C |
| **Dosen** | - |

---

## 📋 Deskripsi Proyek

Proyek ini membangun sebuah **pipeline end-to-end** untuk preprocessing dan klasifikasi sentimen teks berbahasa gaul Indonesia pada dataset ulasan parfum lokal yang dikumpulkan dari platform Google Review dan Twitter/X.

### Rantai Transformasi

```
DATA (Teks Mentah)  →  INFORMASI (Teks Bersih + Label)  →  PENGETAHUAN (Model ML + Slang Dictionary)
```

- **Data**: Teks mentah ulasan parfum dari Google Review / Twitter/X yang mengandung singkatan, typo, dan bahasa gaul.
- **Informasi**: Teks yang sudah dibersihkan, dibakukan, dan diberi label sentimen (Positif / Negatif / Netral).
- **Pengetahuan**: Model Machine Learning (Naive Bayes & SVM) yang mampu mengklasifikasikan sentimen secara otomatis, serta Kamus Normalisasi (Slang Dictionary) khusus domain parfum.

---

## 🗂️ Struktur Folder

```
TUBES/
│
├── 📁 data/
│   ├── raw/            ← Dataset mentah (.csv)
│   ├── interim/        ← Data setengah jadi (setelah cleaning dasar)
│   └── processed/      ← Dataset final berlabel sentimen (.csv)
│
├── 📁 scripts/
│   ├── 02_data_profiling/          ← Analisis kualitas data
│   ├── 03_basic_cleaning/          ← Case folding, regex, filtering
│   ├── 04_advanced_normalization/  ← Normalisasi slang ke bahasa baku
│   ├── 05_labeling/                ← Pelabelan sentimen berbasis keyword
│   ├── 06_validation/              ← Validasi integritas data
│   ├── 07_machine_learning/        ← Klasifikasi sentimen (SVM & Naive Bayes)
│   └── utils/                      ← Fungsi-fungsi helper & logger
│
├── 📁 dictionary/      ← Slang Dictionary (168 entri, 10 kategori)
│
├── 📁 docs/
│   ├── jurnal/               ← Draft & final artikel jurnal SINTA
│   ├── presentasi/           ← Slide UAS
│   └── laporan_mingguan/     ← Log progress tiap minggu
│
├── 📁 results/
│   ├── figures/        ← Grafik, Word Cloud, Confusion Matrix
│   ├── reports/        ← Laporan evaluasi otomatis
│   └── models/         ← Model ML (.pkl) & TF-IDF Vectorizer (.pkl)
│
├── 📁 logs/            ← Log eksekusi skrip
│
├── 📄 README.md        ← File ini
├── 📄 requirements.txt ← Daftar library Python
├── 📄 .gitignore       ← File yang diabaikan Git
├── 📄 config.py        ← Konfigurasi path & parameter global
└── 📄 run_pipeline.py  ← Master script pipeline preprocessing
```

---

## 🚀 Cara Menjalankan

### 1. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 2. Jalankan Pipeline Preprocessing (Langkah 1–5)
```bash
# Jalankan seluruh pipeline sekaligus:
python run_pipeline.py

# Atau jalankan per langkah:
python scripts/02_data_profiling/profiling.py
python scripts/03_basic_cleaning/basic_cleaning.py
python scripts/04_advanced_normalization/normalization.py
python scripts/05_labeling/labeling.py
python scripts/06_validation/validation.py
```

### 3. Jalankan Pipeline Machine Learning (Langkah 6)
```bash
python scripts/07_machine_learning/modelling.py
```

---

## 📊 Hasil Machine Learning

### Perbandingan Model

| Model | Akurasi | F1 Macro | F1 Weighted | Penanganan Imbalance |
|---|---|---|---|---|
| **Naive Bayes** 🏆 | **92,53%** | **0,7102** | **0,9227** | SMOTE pada data latih |
| SVM (LinearSVC) | 89,66% | 0,6163 | 0,8776 | class_weight='balanced' |

> Model terbaik: **Multinomial Naive Bayes** dengan akurasi **92,53%** dan F1-Weighted **0,9227**.

### Word Cloud: Sebelum vs Sesudah Preprocessing

| Sebelum | Sesudah |
|---|---|
| ![Before](results/figures/wordcloud_before.png) | ![After](results/figures/wordcloud_after.png) |

---

## 📅 Timeline Pengerjaan

| Minggu | Fase | Status |
|---|---|---|
| 1-2 | Inisiasi & Akuisisi Data (1.122 baris) | ✅ Selesai |
| 3-4 | Data Profiling (17,74% duplikat, 6 visualisasi) | ✅ Selesai |
| 5-6 | Basic Cleaning (868 baris bersih, 77,4% tersisa) | ✅ Selesai |
| 7-8 | Advanced Normalization — 168 entri kamus (UTS) | ✅ Selesai |
| 9-10 | Labeling — Positif 87,1% / Netral 11,9% / Negatif 1,0% | ✅ Selesai |
| 11-12 | Validasi — 0 noise tersisa, integrity check PASS | ✅ Selesai |
| 13 | Machine Learning — SVM & Naive Bayes (Akurasi 92,53%) | ✅ Selesai |
| 14 | Drafting Jurnal | 🔄 Selanjutnya |
| 15-16 | Final Submission (UAS) | ⏳ Pending |

---

## 📚 Referensi

- Jurnal Utama: [Springer - E-Commerce Review NLP](https://link.springer.com/article/10.1007/s10660-022-09582-4)

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademik. Dataset dan kamus normalisasi bebas digunakan untuk penelitian dengan mencantumkan sumber.
