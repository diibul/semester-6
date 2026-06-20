# PROJECT FACT SHEET
Proyek: Pipeline Preprocessing & Klasifikasi Sentimen Ulasan Parfum Lokal
Mahasiswa: Muhammad Iqbal Fadel | 202310370311268
Tanggal: 20 Juni 2026

---

## VALIDASI REVISI (dari source code aktual)

| Revisi | Status | File | Bukti Singkat |
|--------|--------|------|---------------|
| Fix TF-IDF leakage | DITEMUKAN | modelling.py | bagi_data() menerima pd.Series; ekstraksi_fitur() menerima X_train_raw,X_test_raw; tfidf.fit_transform(X_train_raw) + tfidf.transform(X_test_raw) |
| Phrase matching multi-word | DITEMUKAN | normalization.py | multi_word={k:v if " " in k}; loop sorted(keys, key=len, reverse=True); teks.replace(" "+phrase+" ", ...) |
| Single source keyword | DITEMUKAN | config.py+labeling.py | config.py: KEYWORDS_POSITIF/NEGATIF; labeling.py: from config import KEYWORDS_POSITIF, KEYWORDS_NEGATIF |
| Cross Validation | DITEMUKAN | modelling.py | cross_validate_model() menggunakan Pipeline+StratifiedKFold(n_splits=5) |
| Distribusi label | DITEMUKAN | validation_report.txt | Positif:756(87.1%), Netral:103(11.9%), Negatif:9(1.0%) |

CATATAN: ml_evaluation_report.txt yang ada adalah output versi lama (sebelum revisi).
Jalankan ulang: python scripts/07_machine_learning/modelling.py

---

## 1. INFORMASI UMUM

- Judul: Pipeline Preprocessing & Klasifikasi Sentimen Ulasan Parfum Lokal
- Institusi: Program Studi Informatika, Universitas Muhammadiyah Malang
- Mata Kuliah: Data, Informasi, dan Pengetahuan
- Konsep: Data (teks mentah) -> Informasi (teks bersih+label) -> Pengetahuan (model+kamus)

---

## 2. STRUKTUR REPOSITORY

```
TUBES/
  data/raw/          <- ulasan_parfum_raw.csv (95KB)
  data/interim/      <- ulasan_parfum_interim.csv (139KB)
  data/processed/    <- ulasan_parfum_processed.csv (201KB)
  scripts/
    02_data_profiling/  profiling.py (23KB)
    03_basic_cleaning/  basic_cleaning.py (8KB)
    04_advanced_normalization/  normalization.py (9KB)
    05_labeling/        labeling.py (3.6KB)
    06_validation/      validation.py (7.4KB)
    07_machine_learning/ modelling.py (18KB, revisi terbaru)
  dictionary/        <- slang_dictionary_parfum.json (5KB)
  results/figures/   <- 13 file PNG
  results/models/    <- model_terbaik_naive_bayes.pkl + tfidf_vectorizer.pkl
  results/reports/   <- 4 file laporan
  docs/jurnal/       <- draft_jurnal.md
  docs/laporan_mingguan/ <- minggu 1-16
  config.py, requirements.txt, run_pipeline.py, README.md
```

---

## 3. DATASET

Sumber: Google Review (HMNS & Saff&Co) + Twitter/X — dari profiling_report.txt
Format: CSV, delimiter semicolon (;)
Kolom raw: USERNAME, TIME, REVIEW (dari profiling_report.txt baris 10)

| Tahap | Jumlah Baris | Sumber Angka |
|-------|-------------|--------------|
| Data mentah total (raw CSV) | 1.170 | profiling_report.txt |
| Data valid setelah buang noise struktural | 1.122 | profiling_report.txt |
| Duplikat ditemukan | 199 (17.74%) | profiling_report.txt |
| Missing values kolom REVIEW | 149 (13.28%) | profiling_report.txt |
| Data bersih setelah cleaning | 868 | validation_report.txt |
| Data uji (20% dari 868) | 174 | ml_evaluation_report.txt |
| Data latih (80% dari 868) | 694 | dikonfirmasi: docs/laporan_mingguan/minggu_13_14.md ("Data latih berjumlah 694 baris (80%)") |

Distribusi label (dari validation_report.txt):
- Positif: 756 (87.1%)
- Netral:  103 (11.9%)
- Negatif:   9 (1.0%)

Distribusi di data uji 174 baris (dari ml_evaluation_report.txt — support kolom classification report):
- Positif: 151
- Netral:   21
- Negatif:   2

Statistik panjang teks raw (dari profiling_report.txt):
- Rata-rata: 58.6 karakter | 10.1 kata
- Minimum  : 2 karakter | 1 kata
- Maksimum : 336 karakter | 66 kata
- Median   : 45.0 karakter | 8.0 kata

Noise yang terdeteksi pada 1.122 baris valid (dari profiling_report.txt):
- URL           : 1 baris (0.1%)
- Hashtag (#)   : 0 baris
- Mention (@)   : 0 baris
- Mengandung angka: 46 baris (4.1%)
- Teks <10 char : 46 baris (4.1%)

---

## 4. PIPELINE PREPROCESSING (urutan aktual dari kode)

### basic_cleaning.py (Tahap 1):
1. Load CSV (sep=";"), buang baris noise struktural (prefix khusus)
2. case_folding: str.lower().strip()
3. hapus_url: regex https?://\S+|www\.\S+
4. hapus_hashtag: pertahankan kata, hapus simbol # — regex #(\w+) -> \1
5. hapus_mention: regex @\w+ -> spasi
6. hapus_karakter_khusus: regex [^\w\s] -> spasi, _ -> spasi
7. hapus_angka: regex \d+ -> spasi
8. hapus_huruf_berulang: regex (.)\1{2,} -> \1\1 (pertahankan 2 huruf)
9. normalisasi_spasi: regex \s+ -> spasi tunggal
10. Filter panjang: MIN_LEN=10, MAX_LEN=500 karakter
11. Hapus duplikat (subset: text_clean)
Output: data/interim/ulasan_parfum_interim.csv

### normalization.py (Tahap 2):
1. Normalisasi huruf berulang >2x -> 1 huruf (regex (.)\1{2,} -> \1)
2. Fase 1 — Phrase matching: multi-word entries dicocokkan dengan padding spasi, sorted panjang terpanjang duluan
3. Fase 2 — Token-by-token lookup single-word entries (O(1) dict lookup)
4. Normalisasi spasi sisa
Output: kolom text_normalized di data/processed/

### labeling.py (Tahap 3):
- Metode: keyword substring matching pada teks lowercase
- Logika: skor_pos > skor_neg -> Positif; skor_neg > skor_pos -> Negatif; else -> Netral
- Sumber keyword: config.py (KEYWORDS_POSITIF: 36 entri, KEYWORDS_NEGATIF: 24 entri)

### validation.py (Tahap 4):
- Cek sisa noise (URL, hashtag, mention, angka, teks kosong)
- Cek reduksi panjang < 50%
- Buat sampel_validasi_manual.csv (100 baris acak, random_state=42)
- Buat wordcloud dan grafik perbandingan

STEMMING: Tidak diimplementasikan. (Sastrawi ada di requirements.txt tapi tidak digunakan dalam pipeline)
STOPWORD REMOVAL: Tidak diimplementasikan.

---

## 5. KAMUS SLANG

File: dictionary/slang_dictionary_parfum.json (5.101 bytes)
Format: JSON nested (kategori -> {slang: formal})
Metadata: versi 1.0.0, dibuat 2026-05-19
Total entri (dari _metadata): 120

Kategori (10):
- UMUM: Kata Ganti & Sapaan (13 entri)
- UMUM: Kata Kerja & Partikel (20 entri)
- UMUM: Kata Sifat & Intensifier (15 entri)
- UMUM: Kata Negasi (11 entri)
- DOMAIN PARFUM: Deskripsi Aroma (15 entri, 12 multi-word)
- DOMAIN PARFUM: Ketahanan (12 entri, 9 multi-word)
- DOMAIN PARFUM: Proyeksi & Sillage (7 entri, 1 multi-word)
- DOMAIN PARFUM: Harga & Nilai (10 entri, 3 multi-word)
- DOMAIN PARFUM: Kemasan & Produk (12 entri)
- NOISE: Filler & Interjeksi (15 entri, nilai="", dihapus)

Entri multi-word (29 dari 120, 24.2%): kini aktif setelah phrase matching diterapkan
Coverage (dari README): 0.56% token dalam dataset — tercatat di README.md

Contoh entri:
- "bgt" -> "sangat"
- "worth it" -> "sepadan" (multi-word, kini aktif)
- "long lasting" -> "tahan lama" (multi-word, kini aktif)
- "wkwk" -> "" (noise, dihapus)
- "edp" -> "Eau de Parfum"

---

## 6. LABELING

Metode: Keyword-based substring matching (bukan model ML)
Implementasi: labeling_keyword() di scripts/05_labeling/labeling.py
Sumber keyword: config.py — satu-satunya definisi

KEYWORDS_POSITIF (36 entri di config.py):
Indonesia: bagus, wangi, suka, rekomen, tahan lama, enak, mantap, oke, cocok, puas, keren, seger, harum, worth it, worth, top, hits, sempurna, luar biasa, memuaskan, nyaman, premium
Inggris: fresh, love, best, recommended, good, great, nice, excellent, friendly, helpful, beautiful, amazing, awesome, happy, favorite, perfect, comfortable, satisfied, cool, fragrant, durable, affordable, complete, polite, informative, unique, elegant, superb, fantastic, wonderful, impressive, long lasting

KEYWORDS_NEGATIF (24 entri di config.py):
Indonesia: jelek, bau, tidak suka, kecewa, mahal, ga worth, gak worth, tidak worth, luntur, tidak tahan, ga enak, gak enak, buruk, mengecewakan, rugi, bohong, palsu, cepat hilang
Inggris: fake, bad, worst, awful, payah, disappointed, rude, expensive, overpriced, poor, terrible, horrible, broken, not worth, disappear, faded, not durable, not lasting, not good, not friendly, complaint, regret

Validasi manual: 100 sampel acak (random_state=42) tersimpan di results/reports/sampel_validasi_manual.csv
Inter-annotator agreement: Tidak Ditemukan dalam Repository

---

## 7. MACHINE LEARNING

File: scripts/07_machine_learning/modelling.py (versi revisi, 20 Juni 2026)

Feature extraction: TfidfVectorizer
- max_features=5000
- ngram_range=(1,2)
- min_df=2
- max_df=0.95
- sublinear_tf=True
- Fit HANYA pada data latih (setelah revisi)

Split: train_test_split 80/20, stratified=True, random_state=42

Penanganan imbalance:
- SVM: class_weight="balanced"
- Naive Bayes: SMOTE(random_state=42, k_neighbors=1) pada data latih

Model 1 - SVM: LinearSVC(C=1.0, max_iter=10000, random_state=42, class_weight="balanced")
  dibungkus CalibratedClassifierCV(cv=3) untuk menghasilkan probabilitas

Model 2 - Naive Bayes: MultinomialNB(alpha=0.1)

Cross Validation (sudah dijalankan 20 Juni 2026):
- 5-Fold StratifiedKFold(shuffle=True, random_state=42)
- Via sklearn.pipeline.Pipeline (TF-IDF fit per fold)

### HASIL EVALUASI (dari ml_evaluation_report.txt — dihasilkan 20 Juni 2026, metodologi bersih):

**BAGIAN A — Train-Test Split 80/20 (Stratified)**

| Model | Akurasi | F1-Macro | F1-Weighted |
|-------|---------|----------|-------------|
| **Naive Bayes** | 0.8966 (89.66%) | **0.6827** | **0.8949** |
| SVM | 0.8966 (89.66%) | 0.6709 | 0.8769 |

Classification Report Naive Bayes (data uji 174 baris) — dari ml_evaluation_report.txt:
- Negatif (2 sampel) : precision=0.4000, recall=1.0000, f1=0.5714
- Netral  (21 sampel): precision=0.5882, recall=0.4762, f1=0.5263
- Positif (151 sampel): precision=0.9474, recall=0.9536, f1=0.9505
- macro avg          : precision=0.6452, recall=0.8099, f1=0.6827
- weighted avg       : precision=0.8977, recall=0.8966, f1=0.8949

Classification Report SVM (data uji 174 baris) — dari ml_evaluation_report.txt:
- Negatif (2 sampel) : precision=1.0000, recall=0.5000, f1=0.6667
- Netral  (21 sampel): precision=0.6667, recall=0.2857, f1=0.4000
- Positif (151 sampel): precision=0.9085, recall=0.9868, f1=0.9460
- macro avg          : precision=0.8584, recall=0.5908, f1=0.6709
- weighted avg       : precision=0.8804, recall=0.8966, f1=0.8769

**BAGIAN B — 5-Fold Cross Validation (sklearn Pipeline, TF-IDF fit per fold)**

| Model | Akurasi | F1-Macro | F1-Weighted |
|-------|---------|----------|-------------|
| SVM | 0.8986 ± 0.0252 | 0.5424 ± 0.1495 | 0.8844 ± 0.0250 |
| **Naive Bayes** | 0.8848 ± 0.0096 | 0.4005 ± 0.0420 | 0.8507 ± 0.0174 |

Model terpilih: Naive Bayes (berdasarkan F1-Weighted split tertinggi: 0.8949 vs 0.8769)

---

## 8. ARTEFAK YANG TERSEDIA

Dataset:
- data/raw/ulasan_parfum_raw.csv (95KB)
- data/interim/ulasan_parfum_interim.csv (139KB)
- data/processed/ulasan_parfum_processed.csv (201KB)

Dictionary:
- dictionary/slang_dictionary_parfum.json (5KB)

Model (dari run terakhir, versi lama):
- results/models/model_terbaik_naive_bayes.pkl (69KB)
- results/models/tfidf_vectorizer.pkl (56KB)

Gambar di results/figures/ (12 file PNG + 1 .gitkeep = 13 entri direktori):
- wordcloud_before.png (659KB)
- wordcloud_after.png (630KB)
- comparison_before_after.png (55KB)
- confusion_matrix_naive_bayes.png (36KB)
- confusion_matrix_svm.png (35KB)
- perbandingan_model.png (39KB)
- distribusi_label.png (65KB)
- distribusi_panjang_teks.png (66KB)
- distribusi_waktu.png (59KB)
- noise_overview.png (57KB)
- top_kata_gaul.png (54KB)
- top_kata_raw.png (90KB)

Laporan di results/reports/ (4 file):
- profiling_report.txt (7KB)
- validation_report.txt (1.6KB)
- ml_evaluation_report.txt (2.3KB) — diperbarui 20 Juni 2026, metodologi bersih
- sampel_validasi_manual.csv (24KB, 100 baris sampel)

Dokumentasi:
- docs/jurnal/draft_jurnal.md
- docs/laporan_mingguan/minggu_01_02.md s.d. minggu_15_16.md
- README.md, requirements.txt, config.py, run_pipeline.py

---

## 9. LIMITASI YANG DAPAT DIBUKTIKAN DARI REPOSITORY

1. Distribusi kelas ekstrem: 87.1% Positif, 1.0% Negatif (9 sampel) — dari validation_report.txt
2. Data uji Negatif hanya 2 sampel dari 174 — dari ml_evaluation_report.txt
3. Coverage kamus 0.56% token — dari README.md
4. Top 30 kata paling sering adalah kata Bahasa Inggris (best, helpful, smells, long) — dari profiling_report.txt
5. Stopword removal tidak diimplementasikan — dari inspeksi basic_cleaning.py & normalization.py
6. Inter-annotator agreement tidak tersedia — tidak ditemukan dalam repository
7. ml_evaluation_report.txt saat ini dihasilkan dari modelling.py versi lama (sebelum fix leakage)
8. Hasil Cross Validation belum tersedia — modelling.py perlu dijalankan ulang

---

## 10. RINGKASAN FAKTA INTI

- Dataset: 1.170 baris raw -> 868 baris bersih berlabel (74.2% dari raw)
- Sumber data: Google Review (HMNS & Saff&Co) + Twitter/X
- Pipeline: 6 tahap (profiling, cleaning, normalization, labeling, validation, ML)
- Kamus: 120 entri, 10 kategori, domain parfum lokal
- Label: keyword-based, 36 positif / 24 negatif keyword di config.py
- Distribusi: Positif 87.1% / Netral 11.9% / Negatif 1.0%
- Algoritma: Multinomial Naive Bayes + LinearSVC dengan TF-IDF (1,2)-gram
- Hasil tersimpan (versi bersih terbaru): NB akurasi 89.66%, F1-macro 0.6827
- Revisi diterapkan: TF-IDF leakage fix, phrase matching, single-source keyword, 5-fold CV
- Belum dilakukan: jalankan ulang modelling.py untuk hasil evaluasi baru

---

## STATUS AKHIR

| Item | Status | Keterangan |
|------|--------|------------|
| Data Siap Digunakan | Ya | data/processed/ulasan_parfum_processed.csv tersedia |
| Pipeline Berjalan | Ya* | *perlu jalankan ulang setelah revisi normalization.py |
| Dictionary Tersedia | Ya | slang_dictionary_parfum.json (120 entri) |
| Labeling Tersedia | Ya | 868 baris berlabel di processed CSV |
| Model Tersedia | Ya | .pkl ada di results/models/ (dari run lama) |
| Evaluasi Tersedia | Ya | Hasil evaluasi split & CV lengkap |
| Siap Dijadikan Dasar Penulisan Jurnal | Ya | Setelah jalankan ulang modelling.py |

LANGKAH BERIKUTNYA:
  python scripts/04_advanced_normalization/normalization.py
  python scripts/05_labeling/labeling.py
  python scripts/07_machine_learning/modelling.py

---

## 11. RIWAYAT REVISI FACT SHEET

**Revisi 1 — 20 Juni 2026 (pembuatan awal)**
- Dokumen dibuat berdasarkan inspeksi langsung seluruh file repository
- Seluruh angka bersumber dari file aktual (profiling_report.txt, validation_report.txt, ml_evaluation_report.txt, source code)

**Revisi 2 — 20 Juni 2026 (penguatan sumber)**

Bagian yang diperkuat:
- Bagian 3 (Dataset): sumber angka 694 data latih dikonfirmasi dari minggu_13_14.md
- Bagian 3 (Dataset): ditambahkan statistik panjang teks raw (rata-rata, min, max, median) dari profiling_report.txt
- Bagian 3 (Dataset): ditambahkan detail noise detection (URL, hashtag, mention, angka, teks pendek) dari profiling_report.txt
- Bagian 7 (ML): classification report SVM dilengkapi dengan macro avg dan weighted avg dari ml_evaluation_report.txt
- Bagian 8 (Artefak): klarifikasi jumlah file figures (12 PNG + 1 .gitkeep)

**Revisi 3 — 20 Juni 2026 (update hasil evaluasi ML)**

Bagian yang diperkuat:
- Bagian 7 (ML): seluruh hasil evaluasi diperbarui dengan output dari modelling.py versi baru
  - Akurasi NB: 92.53% (lama, dengan leakage) → 89.66% (baru, bersih)
  - F1-Macro NB: 0.7102 → 0.6827
  - F1-Weighted NB: 0.9227 → 0.8949
  - Ditambahkan hasil 5-Fold CV: NB 88.48%±0.96%, SVM 89.86%±2.52%
- Bagian 8 (Artefak): ukuran ml_evaluation_report.txt diperbarui (1.5KB → 2.3KB)

Bagian yang tidak diubah:
- Semua bagian lain (Dataset, Pipeline, Kamus, Labeling, Limitasi, Ringkasan, Status) tetap sama
