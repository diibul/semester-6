# Laporan Progres — 24 Mei 2026

**Mata Kuliah:** Penggalian Data (Data Mining) — Kelas Teori  
**Semester:** 6 (Genap)  
**Tanggal:** 24 Mei 2026  
**Topik Utama:** Implementasi Gaussian Mixture Model (GMM) untuk Customer Segmentation

---

## 1. Pendahuluan

Laporan ini mendokumentasikan progres pengerjaan project Data Mining pada tanggal 24 Mei 2026. Fokus utama pada sesi ini adalah **implementasi algoritma Gaussian Mixture Model (GMM)** sebagai metode clustering utama (highlight) untuk segmentasi pelanggan e-commerce. GMM dipilih karena kemampuannya dalam melakukan *soft clustering* (probabilistik), di mana setiap pelanggan memiliki derajat keanggotaan di setiap cluster, berbeda dengan metode RFM manual yang sudah ada sebelumnya yang bersifat *hard clustering* (rule-based).

### 1.1 Latar Belakang

Pada progres sebelumnya (19 Mei 2026), project telah menyelesaikan:
- Data cleaning (522,601 transaksi bersih)
- Exploratory Data Analysis (12 visualisasi)
- Customer Segmentation dengan metode RFM manual (5 segmen)
- Advanced Analytics (basket analysis, cohort analysis, forecasting)
- Baseline Machine Learning dengan RandomForest (ROC-AUC: 0.92)
- Deliverables (PDF report + PPTX presentation)
- Project restructuring ke folder profesional

Namun, project **belum memiliki algoritma clustering yang menjadi highlight utama**. Oleh karena itu, GMM diimplementasikan sebagai algoritma inti project ini.

### 1.2 Tujuan

1. Mengimplementasikan GMM sebagai algoritma clustering utama project
2. Menentukan jumlah cluster optimal secara otomatis menggunakan BIC/AIC
3. Membandingkan hasil GMM dengan segmentasi RFM yang sudah ada
4. Menghasilkan visualisasi profesional untuk keperluan presentasi
5. Menyusun rekomendasi bisnis berdasarkan profil cluster GMM

---

## 2. Metodologi

### 2.1 Dataset

Dataset yang digunakan adalah data customer-level yang telah disiapkan pada fase sebelumnya:

| Parameter | Nilai |
|-----------|-------|
| File sumber | `data/processed/model_data_customers.csv` |
| Jumlah pelanggan | 4,718 |
| Fitur yang digunakan | 5 |
| Periode data | Desember 2018 — Desember 2019 |

### 2.2 Fitur yang Digunakan

| No | Fitur | Deskripsi | Tipe |
|----|-------|-----------|------|
| 1 | **Recency** | Jumlah hari sejak transaksi terakhir | Numerik (days) |
| 2 | **Frequency** | Jumlah transaksi unik | Numerik (count) |
| 3 | **Monetary** | Total belanja kumulatif (GBP) | Numerik (GBP) |
| 4 | **AvgOrderValue** | Rata-rata nilai per transaksi | Numerik (GBP) |
| 5 | **DistinctProducts** | Jumlah produk unik yang dibeli | Numerik (count) |

### 2.3 Pipeline GMM (7 Tahap)

Pipeline GMM diimplementasikan dalam script `scripts/07_gmm_clustering.py` dengan 7 tahap berurutan:

**Tahap 1 — Data Preparation**
- Load data customer dari `model_data_customers.csv`
- Penanganan nilai infinity dan NaN
- Clipping outlier menggunakan metode IQR (Interquartile Range): nilai di luar 1.5×IQR dari Q1/Q3 di-clip
- Normalisasi menggunakan `StandardScaler` (mean=0, std=1) — krusial karena GMM sensitif terhadap perbedaan skala antar fitur

**Tahap 2 — Seleksi Jumlah Cluster Optimal**
- Fit GMM untuk k=2 hingga k=10
- Hitung BIC (Bayesian Information Criterion) dan AIC (Akaike Information Criterion) untuk setiap k
- Pilih k optimal berdasarkan nilai BIC minimum
- Setiap k di-fit dengan 5 inisialisasi (`n_init=5`) untuk stabilitas

**Tahap 3 — Training GMM**
- Train model final dengan k optimal
- Parameter: `covariance_type='full'`, `n_init=10`, `max_iter=500`, `tol=1e-4`
- Assign hard labels (cluster dominan) dan soft probabilities (probabilitas keanggotaan per cluster)
- Simpan model sebagai file `.pkl`

**Tahap 4 — Cluster Profiling & Auto-Labeling**
- Hitung rata-rata fitur per cluster
- Assign label deskriptif otomatis berdasarkan karakteristik relatif (monetary rank, frequency rank, recency rank)
- Penanganan label duplikat dengan penomoran otomatis

**Tahap 5 — Visualisasi (7 Plot)**
- BIC/AIC selection curve
- PCA 2D scatter plot
- PCA 3D scatter plot
- Radar/spider chart profil cluster
- Cluster distribution bar chart
- Membership probability heatmap
- GMM vs RFM comparison heatmap

**Tahap 6 — Perbandingan GMM vs RFM**
- Rebuild segmen RFM dari data transaksi asli
- Cross-tabulation antara label GMM dan segmen RFM
- Analisis kecocokan dan perbedaan kedua metode

**Tahap 7 — Rekomendasi Bisnis**
- Generate strategi bisnis per cluster berdasarkan profil
- Assign prioritas (Tinggi/Sedang)
- Simpan sebagai CSV

---

## 3. Hasil dan Temuan

### 3.1 Seleksi Jumlah Cluster Optimal

Hasil fitting GMM untuk k=2 hingga k=10:

| k | BIC | AIC |
|---|-----|-----|
| 2 | 54,966.1 | 54,617.3 |
| 3 | 52,671.5 | 52,115.1 |
| 4 | 51,371.7 | 50,607.6 |
| 5 | 50,581.1 | 49,609.5 |
| 6 | 50,116.2 | 48,937.0 |
| 7 | 49,646.3 | 48,259.5 |
| 8 | 49,499.2 | 47,904.8 |
| **9** | **49,234.3** | **47,432.3** |
| 10 | 49,260.1 | 47,250.4 |

**Optimal k = 9** (nilai BIC minimum). BIC dipilih sebagai kriteria utama karena memberikan penalti lebih besar untuk model kompleks, sehingga menghasilkan jumlah cluster yang lebih parsimonious dibandingkan AIC.

### 3.2 Profil Cluster GMM

| Cluster | Label | Jumlah | % | Avg Recency | Avg Frequency | Avg Monetary (GBP) |
|---------|-------|--------|---|-------------|---------------|---------------------|
| 0 | Mid-Value Regular 1 | 277 | 5.9% | 69.2 hari | 4.9 | 16,103.48 |
| 1 | Mid-Value Regular 2 | 343 | 7.3% | 93.8 hari | 5.2 | 13,567.19 |
| 2 | **High-Value Loyal** | 355 | 7.5% | 15.6 hari | 17.8 | **87,728.49** |
| 3 | Emerging / Potential 1 | 473 | 10.0% | 59.7 hari | 3.5 | 5,245.69 |
| 4 | At-Risk / Dormant 1 | 720 | 15.3% | 95.5 hari | 2.0 | 3,524.50 |
| 5 | At-Risk / Dormant 2 | 1,303 | 27.6% | 166.6 hari | 1.0 | 1,781.20 |
| 6 | Mid-Value Regular 3 | 590 | 12.5% | 20.6 hari | 7.0 | 13,849.36 |
| 7 | At-Risk / Dormant 3 | 316 | 6.7% | 121.9 hari | 2.6 | 16,566.41 |
| 8 | Emerging / Potential 2 | 341 | 7.2% | 91.8 hari | 2.9 | 5,212.95 |

#### Interpretasi Cluster:

1. **High-Value Loyal (Cluster 2)**: 355 pelanggan (7.5%) — Pelanggan terbaik dengan recency rendah (15.6 hari), frekuensi tertinggi (17.8 transaksi), dan monetary sangat tinggi (£87,728). Ini adalah pelanggan paling berharga yang harus dipertahankan.

2. **Mid-Value Regular (Cluster 0, 1, 6)**: Total 1,210 pelanggan (25.7%) — Pelanggan menengah dengan frekuensi moderat (4.9–7.0) dan monetary antara £13,500–£16,100. Kelompok ini memiliki potensi untuk di-upgrade menjadi High-Value.

3. **At-Risk / Dormant (Cluster 4, 5, 7)**: Total 2,339 pelanggan (49.6%) — Kelompok terbesar. Recency tinggi (95–167 hari), frekuensi rendah (1–2.6), monetary bervariasi. Cluster 5 (27.6%) paling mengkhawatirkan dengan rata-rata hanya 1 transaksi.

4. **Emerging / Potential (Cluster 3, 8)**: Total 814 pelanggan (17.2%) — Pelanggan baru atau berkembang dengan monetary rendah namun recency cukup baik. Perlu didorong untuk meningkatkan frekuensi.

### 3.3 Perbandingan GMM vs RFM

Cross-tabulation antara cluster GMM dan segmen RFM:

| GMM Cluster | At Risk | Champions | Hibernating | Loyal | Potential | Total |
|-------------|---------|-----------|-------------|-------|-----------|-------|
| At-Risk / Dormant 1 | 63 | 11 | 336 | 310 | 0 | 720 |
| At-Risk / Dormant 2 | 0 | 0 | 997 | 79 | 227 | 1,303 |
| At-Risk / Dormant 3 | 70 | 46 | 144 | 37 | 19 | 316 |
| Emerging / Potential 1 | 203 | 134 | 0 | 136 | 0 | 473 |
| Emerging / Potential 2 | 91 | 53 | 83 | 104 | 10 | 341 |
| High-Value Loyal | 14 | **334** | 4 | 0 | 3 | 355 |
| Mid-Value Regular 1 | 49 | 143 | 58 | 19 | 8 | 277 |
| Mid-Value Regular 2 | 180 | 109 | 33 | 19 | 2 | 343 |
| Mid-Value Regular 3 | 32 | **531** | 2 | 23 | 2 | 590 |
| **Total** | **702** | **1,361** | **1,657** | **727** | **271** | **4,718** |

#### Temuan Kunci Perbandingan:

1. **High-Value Loyal GMM ≈ Champions RFM**: 334 dari 355 pelanggan High-Value Loyal GMM (94.1%) terklasifikasi sebagai Champions di RFM. Ini menunjukkan konsistensi tinggi antara kedua metode untuk mengidentifikasi pelanggan terbaik.

2. **At-Risk/Dormant GMM ≈ Hibernating RFM**: Cluster At-Risk/Dormant 2 (1,303 pelanggan) sebagian besar terdiri dari Hibernating RFM (997 pelanggan, 76.5%). GMM berhasil menangkap pola inaktivitas.

3. **GMM lebih granular**: RFM hanya memiliki 5 segmen rigid, sedangkan GMM mengidentifikasi 9 cluster dengan nuansa berbeda. Misalnya, At-Risk/Dormant dibagi menjadi 3 sub-cluster berdasarkan tingkat keparahan.

4. **Kelebihan GMM**: Setiap pelanggan memiliki probabilitas keanggotaan di setiap cluster (soft clustering), memungkinkan identifikasi pelanggan yang berada di "perbatasan" antar segmen.

### 3.4 Rekomendasi Bisnis per Cluster

| Cluster | Prioritas | Rekomendasi |
|---------|-----------|-------------|
| **High-Value Loyal** | Tinggi | Pertahankan dengan loyalty program eksklusif, early access produk baru, dan personalized offers. Prioritaskan customer service premium. |
| **Mid-Value Regular (1, 2, 3)** | Tinggi | Tingkatkan engagement dengan cross-selling dan bundling. Berikan insentif untuk meningkatkan frekuensi pembelian. |
| **At-Risk / Dormant (1, 2, 3)** | Sedang | Jalankan win-back campaign dengan diskon terbatas dan reminder produk favorit. Kirim survey untuk memahami alasan penurunan aktivitas. |
| **Emerging / Potential (1, 2)** | Sedang | Berikan pengalaman belanja terbaik untuk konversi. Tawarkan bundling starter, free shipping, dan highlight produk best-seller. |

---

## 4. Visualisasi yang Dihasilkan

Seluruh visualisasi tersimpan di `outputs/figures/gmm/`:

| No | File | Deskripsi |
|----|------|-----------|
| 1 | `gmm_bic_aic_selection.png` | Kurva BIC dan AIC untuk seleksi jumlah cluster optimal (k=2 s/d k=10). Garis vertikal menunjukkan k optimal (k=9). |
| 2 | `gmm_cluster_scatter_2d.png` | Scatter plot PCA 2D (2 komponen utama) menunjukkan separasi visual antar 9 cluster. Setiap titik mewakili 1 pelanggan. |
| 3 | `gmm_cluster_scatter_3d.png` | Scatter plot PCA 3D (3 komponen utama) memberikan perspektif tambahan pada struktur cluster. |
| 4 | `gmm_cluster_profiles_radar.png` | Radar chart menampilkan profil normalized (0–1) setiap cluster pada 5 fitur: Recency, Frequency, Monetary, AvgOrderValue, DistinctProducts. |
| 5 | `gmm_cluster_distribution.png` | Bar chart menunjukkan jumlah dan persentase pelanggan per cluster. Cluster At-Risk/Dormant 2 terbesar (27.6%). |
| 6 | `gmm_probability_heatmap.png` | Heatmap rata-rata probabilitas keanggotaan per cluster. Diagonal kuat menunjukkan cluster yang well-separated. |
| 7 | `gmm_vs_rfm_comparison.png` | Heatmap cross-tabulation antara cluster GMM dan segmen RFM. Menunjukkan pemetaan dan koherensi kedua metode. |

---

## 5. Data Output yang Dihasilkan

Seluruh data output tersimpan di `outputs/data/gmm/`:

| No | File | Deskripsi | Ukuran |
|----|------|-----------|--------|
| 1 | `gmm_cluster_assignments.csv` | Daftar CustomerNo beserta cluster assignment dan label | 147 KB |
| 2 | `gmm_cluster_profiles.csv` | Profil statistik setiap cluster (mean fitur, label, persentase) | 1.2 KB |
| 3 | `gmm_strategy_recommendations.csv` | Rekomendasi bisnis per cluster (aksi, prioritas) | 1.6 KB |
| 4 | `gmm_model.pkl` | Model GMM yang sudah di-train (serialized dengan joblib) | 8.1 KB |

---

## 6. Parameter Teknis GMM

| Parameter | Nilai | Keterangan |
|-----------|-------|------------|
| `n_components` | 9 | Jumlah cluster optimal (via BIC) |
| `covariance_type` | `full` | Setiap cluster memiliki matriks kovarians sendiri |
| `n_init` | 10 | Jumlah inisialisasi (cegah local optima) |
| `max_iter` | 500 | Iterasi maksimum per inisialisasi |
| `tol` | 1e-4 | Toleransi konvergensi |
| `random_state` | 42 | Reproducibility |
| Scaling | StandardScaler | Normalisasi z-score |
| Outlier handling | IQR clipping (1.5×IQR) | Mencegah cluster bias oleh outlier |

**Model converged** dalam iterasi yang ditentukan.

---

## 7. File yang Dimodifikasi

Selain pembuatan script baru, beberapa file dokumentasi juga diperbarui:

| File | Perubahan |
|------|-----------|
| `scripts/07_gmm_clustering.py` | **[BARU]** Script GMM pipeline (597 baris, 7 tahap) |
| `requirements.txt` | Tambah dependency `scipy>=1.11.0` |
| `README.md` | Tambah section "Highlight: GMM Clustering" |
| `docs/PROGRESS.md` | Tambah Phase 8, update key findings, output count, tech stack |
| `docs/STRUCTURE.md` | Tambah GMM ke folder tree, pipeline, dan output listing |

---

## 8. Teknologi yang Digunakan

| Library | Versi | Fungsi dalam GMM |
|---------|-------|------------------|
| `scikit-learn` | 1.8.0 | `GaussianMixture`, `StandardScaler`, `PCA` |
| `numpy` | 2.4.6 | Array operations, numerics |
| `pandas` | 2.0+ | Data manipulation, profiling |
| `matplotlib` | 3.7+ | Visualisasi (scatter, bar, radar, 3D) |
| `seaborn` | 0.12+ | Heatmap, styling |
| `joblib` | 1.3+ | Model serialization (.pkl) |

---

## 9. Kesimpulan

### 9.1 Pencapaian Hari Ini

1. **GMM berhasil diimplementasikan** sebagai algoritma clustering utama project
2. **9 cluster optimal** teridentifikasi melalui analisis BIC/AIC
3. **7 visualisasi profesional** dihasilkan untuk keperluan presentasi
4. **Perbandingan GMM vs RFM** menunjukkan konsistensi tinggi (94% overlap pada High-Value)
5. **Rekomendasi bisnis** tersusun per cluster dengan prioritas yang jelas
6. Seluruh dokumentasi project telah diperbarui

### 9.2 Insight Bisnis Utama

- **7.5% pelanggan** (High-Value Loyal) menghasilkan proporsi revenue terbesar — harus menjadi prioritas retensi
- **49.6% pelanggan** terklasifikasi At-Risk/Dormant — peluang besar untuk reactivation campaign
- GMM memberikan **granularitas lebih tinggi** (9 cluster vs 5 segmen RFM), memungkinkan strategi marketing yang lebih targeted
- **Soft clustering** GMM memungkinkan identifikasi pelanggan di zona transisi antar segmen

### 9.3 Status Project

| Aspek | Status |
|-------|--------|
| Data Preparation | ✅ Selesai |
| EDA | ✅ Selesai (12 visualisasi) |
| RFM Segmentation | ✅ Selesai (5 segmen) |
| Advanced Analytics | ✅ Selesai (basket, cohort, forecast) |
| Baseline ML | ✅ Selesai (ROC-AUC 0.92) |
| **GMM Clustering** | **✅ Selesai (9 cluster, 7 visualisasi)** |
| Deliverables | ✅ Selesai (PDF + PPTX) |
| Dokumentasi | ✅ Selesai (README, PROGRESS, STRUCTURE) |

**Project Status: PRODUCTION READY untuk submission.**

---

## 10. Langkah Selanjutnya (Opsional)

1. Cross-validation dan hyperparameter tuning model RandomForest
2. Implementasi model ML lanjutan (XGBoost, Neural Networks)
3. Customer Lifetime Value (CLV) prediction
4. Update presentasi PPTX dengan visualisasi GMM
5. Interactive dashboard menggunakan Streamlit

---

*Laporan ini dibuat secara otomatis sebagai dokumentasi progres project Data Mining.*  
*Tanggal: 24 Mei 2026*  
*Lokasi file: `reports/markdown/Laporan_Progres_24-05-2026.md`*
