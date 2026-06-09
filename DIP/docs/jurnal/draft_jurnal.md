# Pembangunan Pipeline Preprocessing Otomatis untuk Normalisasi Teks Bahasa Gaul pada Dataset Ulasan Parfum Lokal di Media Digital

**Muhammad Iqbal Fadel**  
Program Studi Informatika, Universitas Muhammadiyah Malang  
202310370311268  
Email: [email institusi]

---

## Abstrak

Dataset ulasan konsumen berbahasa Indonesia untuk produk parfum lokal masih sangat terbatas, terutama yang sudah melalui proses pembersihan dan pemberian label secara terstruktur. Penelitian ini menyajikan pipeline preprocessing otomatis end-to-end yang dibangun untuk menangani karakteristik khusus teks ulasan parfum dari platform digital, yaitu penggunaan bahasa gaul, singkatan, dan istilah campuran Bahasa Indonesia-Inggris. Dataset mentah berjumlah 1.122 baris dikumpulkan dari Google Review dan platform Twitter/X, kemudian diproses melalui enam tahap: data profiling, basic cleaning, advanced normalization menggunakan kamus slang domain spesifik, keyword-based labeling, validasi integritas, dan klasifikasi machine learning. Hasil akhir berupa 868 baris data bersih berlabel sentimen (Positif/Negatif/Netral) beserta kamus normalisasi 120 entri yang dapat digunakan kembali oleh peneliti lain. Model Multinomial Naive Bayes yang dilatih pada dataset ini mencapai akurasi 92,53% dengan F1-Weighted 0,9227. Dataset, kamus slang, dan seluruh skrip preprocessing dipublikasikan secara terbuka untuk mendukung penelitian di bidang Natural Language Processing (NLP) berbahasa Indonesia.

**Kata kunci:** preprocessing teks, bahasa gaul, ulasan parfum, slang dictionary, sentiment analysis, NLP bahasa Indonesia

---

## 1. Pendahuluan

Pertumbuhan industri parfum lokal Indonesia dalam beberapa tahun terakhir mendorong meningkatnya volume ulasan konsumen di berbagai platform digital. Ulasan-ulasan tersebut mengandung informasi yang sangat berharga bagi produsen dan peneliti, namun karakteristik penulisannya sangat jauh dari teks formal. Pengguna cenderung menulis dengan singkatan ("bgt", "sis", "rekomen"), istilah campuran bahasa Inggris ("worth it", "long lasting", "packaging"), dan ekspresi informal lainnya yang menyulitkan pemrosesan otomatis.

Masalah utama yang dihadapi penelitian NLP berbahasa Indonesia adalah keterbatasan sumber daya yang bersih dan berlabel. Sebagian besar penelitian yang ada hanya memanfaatkan kamus slang generik yang tidak mencakup istilah domain spesifik, sehingga proses normalisasi menjadi kurang akurat ketika diterapkan pada teks bertemakan produk tertentu.

Penelitian ini bertujuan untuk: (1) membangun pipeline preprocessing yang dapat direproduksi untuk domain ulasan parfum lokal, (2) menyusun kamus normalisasi slang yang bersifat domain-specific, dan (3) menghasilkan dataset bersih berlabel sentimen yang siap digunakan untuk pelatihan model machine learning.

---

## 2. Metodologi

### 2.1 Sumber dan Pengumpulan Data

Data dikumpulkan dari dua sumber utama: Google Review pada toko parfum lokal HMNS dan Saff&Co, serta platform Twitter/X dengan kata kunci terkait parfum lokal Indonesia. Pengumpulan dilakukan secara manual dan semi-otomatis menggunakan teknik web scraping. Dataset mentah awal terdiri dari 1.170 baris, termasuk baris kosong dan noise struktural. Setelah pembersihan awal, diperoleh 1.122 baris data valid dengan kolom USERNAME, TIME, dan REVIEW.

### 2.2 Tahap 1 — Data Profiling (Minggu 3-4)

Data profiling dilakukan untuk memahami kondisi awal dataset sebelum preprocessing dimulai. Hasil profiling menunjukkan:

- Jumlah duplikat: 199 baris (17,74%)
- Missing values pada kolom REVIEW: 149 baris (13,28%)
- Rata-rata panjang teks: 58,6 karakter atau 10,1 kata per ulasan
- Panjang minimum: 2 karakter; maksimum: 336 karakter
- Noise yang terdeteksi: 46 baris mengandung angka (4,1%) dan 46 baris terlalu pendek (<10 karakter)
- Kata gaul yang ditemukan antara lain: "worth" (13 kemunculan), "sis" (13), "bgt" (3), "btw" (1)

Profiling ini menjadi dasar keputusan teknis di tahap-tahap berikutnya, termasuk ambang batas panjang teks minimum yang digunakan saat filtering.

### 2.3 Tahap 2 — Basic Cleaning (Minggu 5-6)

Basic cleaning mencakup tiga proses utama:

**Case folding** — Seluruh teks diubah menjadi huruf kecil untuk menghindari duplikasi token akibat perbedaan kapitalisasi (misalnya "Wangi" dan "wangi" diperlakukan sebagai satu token).

**Regex cleaning** — Karakter-karakter yang tidak membawa makna dihapus menggunakan ekspresi reguler, meliputi URL, simbol khusus, angka berdiri sendiri, dan karakter non-alfanumerik berlebih.

**Filtering** — Ulasan yang terlalu pendek (di bawah 10 karakter setelah dibersihkan) dan duplikat dihapus. Tahap ini mengurangi jumlah data dari 1.122 menjadi 868 baris (77,4% tersisa), yang dianggap wajar karena masih jauh di bawah ambang 50%.

### 2.4 Tahap 3 — Advanced Normalization (Minggu 7-8)

Tahap ini merupakan inti dari pipeline, yaitu konversi kata-kata informal menjadi bentuk baku menggunakan kamus slang yang dibangun secara domain-specific.

**Pembangunan Slang Dictionary**

Kamus slang dikembangkan secara manual berdasarkan observasi pada dataset dan referensi kamus gaul yang sudah ada. Kamus disimpan dalam format JSON terstruktur dengan 10 kategori: kata ganti, kata kerja, kata sifat, negasi, deskripsi aroma, ketahanan parfum, proyeksi, harga, kemasan, dan rekomendasi. Total entri yang dihasilkan adalah 120 pasang kata gaul-formal.

Alasan pemilihan kamus domain-specific dibandingkan kamus generik adalah: (1) istilah teknis parfum seperti "sillage", "longlasting", dan "edt" tidak ada di kamus generik, dan (2) kata yang sama bisa bermakna berbeda tergantung konteks domain.

**Mengapa tidak menggunakan Stemming?**

Keputusan untuk tidak menerapkan stemming didasarkan pada dua pertimbangan. Pertama, dataset ini bersifat multi-bahasa (Indonesia + Inggris), dan stemmer bahasa Indonesia seperti PySastrawi akan salah menangani token berbahasa Inggris. Kedua, tujuan pipeline ini adalah normalisasi (dari gaul ke formal), bukan reduksi morfologi. Stemming berisiko mengubah makna kata yang justru penting untuk klasifikasi sentimen, misalnya "tahan lama" yang menjadi bentuk lain setelah di-stem.

**Proses Normalisasi**

Normalisasi dilakukan token per token dengan mekanisme lookup O(1) pada kamus. Sebelum lookup, huruf-huruf yang berulang lebih dari dua kali dinormalisasi terlebih dahulu (misalnya "wangiiiii" menjadi "wangi"). Coverage kamus sebelum normalisasi adalah 0,56% dari total token, mencerminkan bahwa dataset didominasi Bahasa Inggris.

Contoh transformasi yang dihasilkan:

| Teks Mentah | Teks Bersih | Teks Ternormalisasi |
|---|---|---|
| `Ok bgt` | `ok bgt` | `ok sangat` |
| `rekomen bgt wanginya` | `rekomen bgt wanginya` | `rekomendasikan sangat aromanya` |
| `ga worth sih harganya` | `ga worth sih harganya` | `tidak sepadan sih harganya` |

### 2.5 Tahap 4 — Keyword-based Labeling (Minggu 9-10)

Pelabelan sentimen dilakukan menggunakan pendekatan berbasis kata kunci (keyword matching), yaitu dengan mendefinisikan daftar kata positif, negatif, dan netral yang relevan dengan domain parfum. Pendekatan ini dipilih karena dataset tidak memiliki label awal yang bisa digunakan untuk supervised learning.

Logika pelabelan: jika ulasan mengandung kata kunci positif lebih banyak dari negatif, label "Positif" diberikan; sebaliknya untuk "Negatif"; dan jika jumlahnya seimbang atau tidak ada kata kunci yang cocok, diberi label "Netral".

Distribusi label akhir:

| Label | Jumlah | Persentase |
|---|---|---|
| Positif | 756 | 87,1% |
| Netral | 103 | 11,9% |
| Negatif | 9 | 1,0% |

Ketidakseimbangan kelas (class imbalance) ini wajar mengingat sebagian besar ulasan di Google Review cenderung positif karena konsumen yang tidak puas jarang memberikan ulasan tertulis.

### 2.6 Tahap 5 — Validasi (Minggu 11-12)

Validasi dilakukan dua cara: otomatis dan manual.

**Validasi otomatis** mengecek empat kriteria integritas data: (1) tidak ada URL tersisa, (2) tidak ada teks kosong, (3) reduksi panjang teks di bawah 50%, dan (4) semua baris berlabel. Semua kriteria terpenuhi dengan reduksi rata-rata panjang teks hanya 4,9% (dari 64,2 karakter menjadi 61,1 karakter), membuktikan bahwa proses cleaning tidak merusak makna asli teks.

**Validasi manual** dilakukan dengan mengambil 100 sampel acak dan memeriksanya satu per satu untuk memastikan kesesuaian label dengan isi ulasan. Hasil validasi manual tersimpan dalam file `results/reports/sampel_validasi_manual.csv`.

---

## 3. Deskripsi Data

### 3.1 Statistik Ringkas Dataset Akhir

| Atribut | Nilai |
|---|---|
| Total baris dataset bersih | 868 |
| Kolom utama | text_normalized, label |
| Kolom tambahan | USERNAME, TIME, text_clean |
| Bahasa | Indonesia + Inggris (campuran) |
| Format file | CSV (UTF-8) |
| Ukuran file | 201 KB |

### 3.2 Distribusi Label

| Label | Jumlah | Persentase |
|---|---|---|
| Positif | 756 | 87,1% |
| Netral | 103 | 11,9% |
| Negatif | 9 | 1,0% |

### 3.3 Statistik Teks

| Metrik | Sebelum Cleaning | Sesudah Cleaning |
|---|---|---|
| Rata-rata panjang (karakter) | 64,2 | 61,1 |
| Panjang minimum (karakter) | 10 | 9 |
| Panjang maksimum (karakter) | 336 | 322 |
| Reduksi rata-rata | — | 4,9% |

### 3.4 Kamus Normalisasi (Slang Dictionary)

| Kategori | Jumlah Entri |
|---|---|
| Kata Ganti & Sapaan | 13 |
| Kata Kerja & Partikel | 20 |
| Kata Sifat & Intensifier | 15 |
| Kata Negasi | 11 |
| Deskripsi Aroma | 15 |
| Ketahanan Parfum | 12 |
| Proyeksi & Sillage | 7 |
| Harga & Nilai | 10 |
| Kemasan & Produk | 12 |
| Noise/Filler | 15 |
| **Total** | **120** |

---

## 4. Hasil Klasifikasi Machine Learning

Untuk membuktikan kualitas dan kegunaan dataset yang dihasilkan, dilakukan eksperimen klasifikasi sentimen menggunakan dua algoritma: Support Vector Machine (SVM/LinearSVC) dan Multinomial Naive Bayes.

Pembagian data: 80% data latih dan 20% data uji. Untuk menangani ketidakseimbangan kelas, diterapkan teknik SMOTE (Synthetic Minority Oversampling Technique) pada data latih untuk Naive Bayes, dan parameter `class_weight='balanced'` untuk SVM. Representasi teks menggunakan TF-IDF dengan n-gram (1,2).

| Model | Akurasi | F1-Macro | F1-Weighted |
|---|---|---|---|
| Multinomial Naive Bayes | **92,53%** | **0,7102** | **0,9227** |
| SVM (LinearSVC) | 89,66% | 0,6163 | 0,8776 |

Model Naive Bayes menghasilkan performa lebih baik pada dataset ini, kemungkinan karena distribusi fitur TF-IDF pada ulasan singkat lebih sesuai dengan asumsi distribusi multinomial dibandingkan margin-based SVM.

Perlu dicatat bahwa F1-Macro yang relatif lebih rendah dibandingkan F1-Weighted disebabkan oleh kelas "Negatif" yang sangat sedikit (hanya 9 sampel / 1,0%), sehingga performa model pada kelas minoritas ini memengaruhi nilai makro secara signifikan.

---

## 5. Nilai Guna Dataset

Dataset dan pipeline yang dihasilkan dari penelitian ini dapat dimanfaatkan untuk beberapa keperluan:

1. **Sentiment Analysis** — Dataset berlabel ini siap digunakan langsung untuk melatih model klasifikasi sentimen ulasan produk berbahasa Indonesia, terutama untuk domain produk konsumen (FMCG).

2. **Pengembangan Kamus Slang** — Kamus normalisasi domain parfum yang dihasilkan dapat diperluas atau diadaptasi untuk domain lain seperti kosmetik dan perawatan kulit.

3. **Benchmarking** — Dataset dapat menjadi salah satu acuan evaluasi performa model NLP berbahasa Indonesia yang menangani teks informal/campuran.

4. **Penelitian Lanjutan** — Pipeline yang modular memungkinkan peneliti untuk mengganti atau menambahkan tahap tertentu, misalnya menambahkan aspect-based sentiment analysis atau topic modeling.

---

## 6. Keterbatasan

Beberapa keterbatasan perlu diakui dalam penelitian ini:

- Pelabelan berbasis kata kunci rentan terhadap kesalahan pada ulasan yang mengandung ironi atau sarkasme, di mana sentimen sesungguhnya berlawanan dengan kata yang digunakan.
- Coverage kamus slang yang rendah (0,56%) menunjukkan bahwa dataset ini didominasi Bahasa Inggris, sehingga manfaat kamus normalisasi Bahasa Indonesia menjadi terbatas pada subset tertentu.
- Distribusi kelas yang sangat tidak seimbang (87% Positif) membatasi kemampuan model dalam mendeteksi ulasan negatif.
- Pengumpulan data dilakukan pada periode tertentu, sehingga tidak merepresentasikan tren bahasa yang berkembang.

---

## 7. Kesimpulan

Penelitian ini berhasil membangun pipeline preprocessing end-to-end yang mencakup enam tahap untuk mengolah teks ulasan parfum lokal berbahasa Indonesia informal menjadi dataset bersih berlabel yang siap digunakan untuk machine learning. Kamus normalisasi domain spesifik dengan 120 entri merupakan kontribusi utama penelitian ini karena belum tersedia kamus sejenis untuk domain parfum lokal Indonesia.

Dataset akhir sebanyak 868 baris, kamus slang, dan seluruh skrip Python dipublikasikan secara terbuka untuk mendukung reproduktibilitas penelitian dan pengembangan sumber daya NLP berbahasa Indonesia.

---

## Referensi

1. Haddi, E., Liu, X., & Shi, Y. (2013). The role of text pre-processing in sentiment analysis. *Procedia Computer Science*, 17, 26–32.
2. Medhat, W., Hassan, A., & Korashy, H. (2014). Sentiment analysis algorithms and applications: A survey. *Ain Shams Engineering Journal*, 5(4), 1093–1113.
3. Rahardi, R., et al. (2022). E-Commerce Review NLP with Domain Adaptation. *Springer – Electronic Commerce Research*, 22. https://link.springer.com/article/10.1007/s10660-022-09582-4
4. Saputra, A., & Wahyudi, M. (2021). Normalisasi Teks Bahasa Gaul Indonesia Menggunakan Pendekatan Kamus. *Jurnal Nasional Teknik Elektro dan Teknologi Informasi*, 10(2), 112–119.
5. Chawla, N. V., et al. (2002). SMOTE: Synthetic Minority Over-sampling Technique. *Journal of Artificial Intelligence Research*, 16, 321–357.

---

*Draft ini disusun sebagai bagian dari Tugas Besar Mata Kuliah Data, Informasi, dan Pengetahuan.*  
*Versi: 1.0 | Tanggal: Juni 2026*
