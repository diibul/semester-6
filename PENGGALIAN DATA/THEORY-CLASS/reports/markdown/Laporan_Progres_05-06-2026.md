# Laporan Progres — 5 Juni 2026

## Ringkasan Sesi
Sesi ini berfokus pada **audit menyeluruh**, **perbaikan gap**, **konversi ke notebook**, dan **pembersihan struktur folder** agar project siap 100% untuk dikumpulkan sebagai tugas akademik.

---

## Fase 1: Audit Project (7 Gap Ditemukan)

Dilakukan pemeriksaan detail seluruh project. Ditemukan **7 gap** yang dikategorikan berdasarkan tingkat keparahan:

| # | Gap | Severity | Status |
|---|-----|----------|--------|
| 1 | PDF laporan GMM belum dibuat | 🔴 Kritis | ✅ Selesai |
| 2 | PPTX presentasi belum diupdate (masih versi 19 Mei) | 🔴 Kritis | ✅ Selesai |
| 3 | `outputs/figures/models/` tidak ada — `baseline_roc.png` salah folder | 🟡 Sedang | ✅ Selesai |
| 4 | `STRUCTURE.md` tidak sinkron — masih versi 19 Mei | 🟡 Sedang | ✅ Selesai |
| 5 | `04_baseline_train.py` sangat minimal — tidak ada CV, feature importance | 🟡 Sedang | ✅ Selesai |
| 6 | `README.md` tidak menyebut script ke-7 (GMM) | 🟢 Rendah | ✅ Selesai |
| 7 | `03_feature_selection_methods.ipynb` 473 KB & tidak terdokumentasi | 🟢 Rendah | ✅ Selesai |

---

## Fase 2: Perbaikan Gap (Priority Low → High)

### Gap 6 & 7 (🟢 Rendah)
- **README.md**: Ditambahkan Quick Start pipeline lengkap (7 script), fixed link yang rusak (`DataProsecing.ipynb` → `00_data_processing.ipynb`), dan ditambahkan deskripsi GMM sebagai highlight.
- **Notebook 03**: Output di-clear → ukuran file turun dari **473 KB → 30 KB** (15x lebih kecil).

### Gap 5 & 3 (🟡 Sedang)
- **`04_baseline_train.py`** di-rewrite total:
  - 5 features (sebelumnya 3): DistinctProducts, Frequency, Recency, Monetary, AvgOrderValue
  - Ditambahkan: **5-Fold Stratified Cross-Validation**
  - Ditambahkan: **Feature Importance** visualization (Gini)
  - Ditambahkan: **Confusion Matrix** heatmap
  - Ditambahkan: **Cross-Validation Scores** bar chart
  - Hasil: ROC AUC = 1.0000, CV Accuracy = 0.9996 ± 0.0005
- Folder `outputs/figures/models/` otomatis terbuat dengan **4 file PNG** baru.

### Gap 4 (🟡 Sedang)
- **STRUCTURE.md** ditulis ulang total agar sinkron dengan kondisi aktual project.

### Gap 2 & 1 (🔴 Kritis)
- **PPTX Presentation** di-regenerate:
  - `presentation_progres_01-06-2026.pptx` — **30 slide**, 6 section
  - Format widescreen 16:9 dengan section dividers
  - Mencakup: EDA, RFM, Advanced Analytics, Baseline ML, Feature Selection, GMM
- **PDF Report** di-regenerate:
  - `Laporan_Progres_01-06-2026.pdf` — **3.3 MB**, 21 visualisasi embedded
  - Source: `Laporan_Progres_24-05-2026.md` + semua gambar dari 5 section

---

## Fase 3: Konversi Script ke Notebook

Karena tugas akademik harus dalam format **.ipynb**, seluruh script analisis `.py` dikonversi menjadi Jupyter Notebook:

| Script (.py) | Notebook (.ipynb) | Cells |
|---|---|---|
| `01_eda_run.py` | `01_eda_run.ipynb` | 14 cells (8 code, 6 markdown) |
| `02_advanced_analysis.py` | `02_advanced_analysis.ipynb` | 10 cells (9 code, 1 markdown) |
| `03_model_prep.py` | `03_model_prep.ipynb` | 3 cells (2 code, 1 markdown) |
| `04_baseline_train.py` | `05_baseline_train.ipynb` | 28 cells (14 code, 14 markdown) |
| `07_gmm_clustering.py` | `06_gmm_clustering.ipynb` | 32 cells (17 code, 15 markdown) |

Konversi dilakukan secara cerdas:
- Docstring → Markdown cell (Overview section)
- Section separator (`═══`, `───`) → Markdown header cells
- Path fix: `os.path.dirname(__file__)` → `os.path.abspath('..')`
- Hapus `matplotlib.use('Agg')`, tambah `%matplotlib inline`
- Hapus `if __name__ == '__main__'` guard
- Multi-line statement (misal `plt.rcParams.update({...})`) tetap utuh

---

## Fase 4: Pembersihan Struktur Folder

### File yang Dihapus (11 file)

| File | Alasan Hapus |
|------|-------------|
| `scripts/01_eda_run.py` | Sudah dikonversi ke .ipynb |
| `scripts/02_advanced_analysis.py` | Sudah dikonversi ke .ipynb |
| `scripts/03_model_prep.py` | Sudah dikonversi ke .ipynb |
| `scripts/04_baseline_train.py` | Sudah dikonversi ke .ipynb |
| `scripts/07_gmm_clustering.py` | Sudah dikonversi ke .ipynb |
| `notebooks/01_eda_exploration.ipynb` | Duplikat dengan `01_eda_run.ipynb` |
| `notebooks/02_feature_selection_and_baseline.ipynb` | Duplikat dengan `03` + `05` |
| `reports/Laporan_progres_19-05-2026.pdf` | Usang, diganti versi 01-06 |
| `reports/presentation_progres_19-05-2026.pptx` | Usang, diganti versi 01-06 |
| `reports/markdown/progres 19-05-2026.md` | Usang, path masih pakai `Dokumentasi/` |
| `reports/markdown/Laporan - progres (...).md` | Usang, sudah di-supersede |

### Notebooks di-Renumber (Sequential)
- `03_feature_selection_methods.ipynb` → `04_feature_selection_methods.ipynb`
- `04_baseline_train.ipynb` → `05_baseline_train.ipynb`
- `07_gmm_clustering.ipynb` → `06_gmm_clustering.ipynb`

### File duplikat dihapus
- `outputs/data/models/baseline_roc.png` (duplikat dari `outputs/figures/models/`)
- `scripts/convert_py_to_ipynb.py` (utility sementara, sudah tidak diperlukan)

---

## Fase 5: Update Dokumentasi

Semua file dokumentasi diperbarui agar reflect kondisi aktual:

1. **README.md** — Quick Start sekarang pakai notebook, bukan script .py
2. **STRUCTURE.md** — Rewrite total, notebook-centric, folder tree akurat
3. **PROGRESS.md** — Phase 9 (audit) + Phase 10 (cleanup) ditambahkan

---

## Struktur Project Final

```
project-root/
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/Sales Transaction v.4a.csv           (41.3 MB)
│   └── processed/
│       ├── Sales_Transaction_v4a_cleaned.csv     (49.2 MB)
│       ├── model_data_customers.csv              (264 KB)
│       └── selected_feature_scores.csv           (0.2 KB)
│
├── notebooks/                                     (7 notebooks)
│   ├── 00_data_processing.ipynb
│   ├── 01_eda_run.ipynb
│   ├── 02_advanced_analysis.ipynb
│   ├── 03_model_prep.ipynb
│   ├── 04_feature_selection_methods.ipynb
│   ├── 05_baseline_train.ipynb
│   └── 06_gmm_clustering.ipynb                   ← HIGHLIGHT
│
├── scripts/                                       (2 utility scripts)
│   ├── 05_generate_pdf_report.py
│   └── 06_make_presentation.py
│
├── outputs/
│   ├── figures/
│   │   ├── eda/          (12 PNG)
│   │   ├── analysis/     (6 PNG)
│   │   ├── models/       (4 PNG)
│   │   └── gmm/          (7 PNG)
│   └── data/
│       ├── analysis/     (10 CSV)
│       ├── models/       (1 PKL + 1 JSON)
│       └── gmm/          (3 CSV + 1 PKL)
│
├── reports/
│   ├── Laporan_Progres_01-06-2026.pdf             (3.3 MB, 21 gambar)
│   ├── presentation_progres_01-06-2026.pptx       (2.9 MB, 30 slides)
│   └── markdown/
│       ├── Laporan_Progres_24-05-2026.md
│       └── Laporan_Progres_05-06-2026.md           ← FILE INI
│
└── docs/
    ├── STRUCTURE.md
    └── PROGRESS.md
```

**Total: 67 file** — bersih, terorganisir, zero duplikat.

---

## Statistik Model

### Baseline RandomForest
- Features: DistinctProducts, Frequency, Recency, Monetary, AvgOrderValue
- ROC AUC: **1.0000**
- CV Accuracy: **0.9996 ± 0.0005** (5-fold stratified)
- CV ROC AUC: **1.0000 ± 0.0000**

### GMM Clustering
- Optimal clusters: **9** (via BIC/AIC)
- Algorithm: Gaussian Mixture Model (full covariance)
- High-Value Loyal: 355 customers (7.5%)
- Mid-Value Regular: 1,210 customers (25.6%)
- At-Risk / Dormant: 2,339 customers (49.6%)
- Emerging / Potential: 814 customers (17.3%)

---

**Status:** ✅ Project 100% selesai dan siap dikumpulkan.  
**Author:** Muhammad Iqbal Fadel  
**Tanggal:** 5 Juni 2026
