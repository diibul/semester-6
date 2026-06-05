# Simulasi Perilaku Pembelian Pelanggan dengan Agent-Based Modeling

## Deskripsi Project

Project ini mengimplementasikan sistem simulasi berbasis agen untuk memodelkan perilaku pembelian pelanggan dalam lingkungan e-commerce. Dengan menggunakan pendekatan Agent-Based Modeling (ABM), simulasi ini memungkinkan analisis bagaimana berbagai faktor seperti diskon, minat pelanggan, dan suasana hati memengaruhi keputusan pembelian secara agregat.

Project merupakan tugas mata kuliah Pemodelan dan Simulasi Data semester 6 dan dikembangkan secara bertahap melalui tiga fase implementasi, masing-masing menambahkan kompleksitas dan fitur baru ke model simulasi.


## Latar Belakang

Dalam praktik e-commerce, memahami perilaku pembelian pelanggan merupakan hal penting untuk mengoptimalkan strategi penjualan, penetapan harga, dan manajemen inventori. Namun, perilaku konsumen bukan sekadar agregat dari keputusan individual yang sederhana — ada banyak faktor yang saling berinteraksi dan memengaruhi satu sama lain.

Agent-Based Modeling memberikan kerangka kerja yang tepat untuk memahami fenomena ini. Dengan memodelkan setiap pelanggan sebagai agen autonomus dengan karakteristik dan kemampuan pengambilan keputusan sendiri, kita dapat mensimulasikan bagaimana sistem berperilaku secara keseluruhan tanpa perlu menetapkan aturan agregat secara eksplisit. Pola perilaku kolektif muncul dari interaksi antara agen-agen individual dengan lingkungan simulasi.

Project ini mengeksplorasi hubungan antara diskon produk, minat pelanggan, dan suasana hati belanja terhadap total volume transaksi yang terjadi. Hasil simulasi dapat membantu dalam pengambilan keputusan strategis terkait penawaran harga dan promosi.


## Arsitektur Model Simulasi

### Atribut Agen

Setiap agen dalam simulasi mewakili seorang pelanggan dan memiliki atribut berikut:

- **Purchase Probability (P)**: Probabilitas dasar pelanggan untuk melakukan pembelian, berkisar antara 0.1 hingga 0.5. Atribut ini merefleksikan kecenderungan alami pelanggan untuk membeli.

- **Interest Level (I)**: Tingkat ketertarikan pelanggan terhadap produk yang ditawarkan, berkisar antara 0.0 hingga 1.0. Semakin tinggi nilai ini, semakin mudah diskon mempengaruhi keputusan pembelian.

- **Budget (B)**: Anggaran maksimal yang dimiliki pelanggan untuk pembelian, berkisar antara 50 hingga 500 unit mata uang. Pelanggan tidak akan membeli jika harga produk melebihi budget mereka.

- **Shopping Mood (M)**: Suasana hati pelanggan saat berbelanja, berkisar antara 0.0 hingga 1.0. Atribut ini menambah dimensi psikologis ke model dan mencerminkan pengaruh emosi terhadap keputusan pembelian (ditambahkan di fase kedua pengembangan).


### Variabel Lingkungan

- **Product Price**: Harga dasar produk ditetapkan sebesar 50 unit mata uang.

- **Discount Rate**: Persentase potongan harga yang ditawarkan, berkisar antara 0% hingga 50%. Dalam simulasi, diskon direpresentasikan sebagai desimal (misalnya, 30% = 0.3).

- **Iterasi Simulasi**: Jumlah putaran simulasi yang dijalankan untuk mengumpulkan data transaksi. Default adalah 1000 iterasi, dapat disesuaikan hingga 5000.

- **Jumlah Agen**: Jumlah pelanggan yang disimulasikan dalam setiap scenario. Default adalah 100 agen, dapat disesuaikan antara 10 hingga 500.


### Aturan Transisi dan Model Matematis

Keputusan pembelian untuk setiap agen dihitung menggunakan model probabilistik berikut:

**Fase 1 (Minggu 8) — Model Dasar:**

P_final = min(P + (I × discount), 1.0)

**Fase 2 & 3 (Minggu 10-12) — Model dengan Shopping Mood:**

P_final = min(P + (I × discount) + (M × 0.2), 1.0)

Keterangan:
- P adalah purchase probability
- I adalah interest level
- discount adalah tingkat diskon yang diterapkan
- M adalah shopping mood
- Faktor 0.2 mengalikan shopping mood untuk memberikan bobot terhadap probabilitas pembelian

Setelah P_final dihitung, proses keputusan pembelian dilakukan sebagai berikut:

1. Hitung harga akhir: final_price = PRODUCT_PRICE × (1 - discount)
2. Validasi budget: Jika budget pelanggan < final_price, keputusan = tidak membeli
3. Generasi nilai acak: r = random(0, 1)
4. Keputusan pembelian: Jika r < P_final, maka beli; selain itu, tidak beli

Keputusan pembelian dari semua agen diagregasi untuk menghasilkan total transaksi dalam satu iterasi.


## Skenario Simulasi

Project ini mengimplementasikan tiga skenario utama yang dikembangkan secara bertahap:

### Skenario 1: Dampak Diskon Terhadap Penjualan (Minggu 8)

Skenario dasar menguji pengaruh tingkat diskon terhadap total transaksi. Diskon divariasikan pada nilai 0%, 10%, 30%, dan 50%.

- **Kondisi**: Semua agen memiliki atribut yang diinisialisasi secara acak
- **Parameter**: Discount rate (0%, 10%, 30%, 50%), 100 agen, 1000 iterasi
- **Output Diukur**: Rata-rata transaksi, maksimum, minimum, standar deviasi per diskon
- **Analisis**: Membandingkan bagaimana tingkat diskon yang berbeda mempengaruhi volume transaksi total

### Skenario 2: Pengaruh Shopping Mood (Minggu 10)

Skenario ini memperluas model dengan menambahkan dimensi suasana hati belanja. Setiap agen sekarang memiliki shopping mood yang memengaruhi probabilitas pembelian.

- **Kondisi**: Agen memiliki atribut dasar ditambah shopping mood yang diinisialisasi acak (0.0-1.0)
- **Parameter**: Discount rate (0%, 10%, 30%, 50%), shopping mood random, 100 agen, 1000 iterasi
- **Output Diukur**: Statistik transaksi dengan penambahan faktor mood
- **Analisis**: Membandingkan hasil simulasi dengan dan tanpa mood untuk menunjukkan kontribusi emosi terhadap keputusan pembelian

### Skenario 3: Monte Carlo Scenario Testing (Minggu 12)

Skenario ketiga menggunakan metode Monte Carlo untuk menguji tiga kondisi shopping mood yang berbeda dengan diskon tetap.

- **Kondisi A (Normal Mood)**: Shopping mood agen berkisar 0.0-1.0 (distribusi normal)
- **Kondisi B (Low Mood)**: Shopping mood agen berkisar 0.0-0.3 (suasana hati rendah)
- **Kondisi C (High Mood)**: Shopping mood agen berkisar 0.7-1.0 (suasana hati tinggi)

- **Parameter Tetap**: Discount rate 30% (titik tengah optimal), 100 agen, 1000 iterasi
- **Output Diukur**: Statistik transaksi untuk ketiga skenario
- **Analisis**: Mendemonstrasikan dampak signifikan suasana hati kolektif terhadap perilaku pembelian


## Struktur Direktori Project

```
PEMODELAN DAN SIMULASI DATA/
├── Main.ipynb              Notebook Jupyter berisi logika simulasi lengkap
├── app.py                  Dashboard Streamlit interaktif untuk simulasi
├── requirements.txt        File dependencies Python (kosong, perlu diisi)
├── README.md               Dokumentasi project (file ini)
└── Reports/                Folder laporan mingguan
    ├── MINGGU 4.docx       Laporan tahap perencanaan
    ├── MINGGU 6.docx       Laporan tahap awal implementasi
    ├── MINGGU 8.docx       Laporan skenario dasar
    ├── MINGGU 10.docx      Laporan implementasi shopping mood
    └── MINGGU 12.docx      Laporan Monte Carlo testing
```

### Penjelasan File Utama

- **Main.ipynb**: Notebook Python yang berisi implementasi lengkap model simulasi, terbagi dalam beberapa sel yang mencakup: inisialisasi parameter, pembuatan agen, fungsi simulasi, running simulasi, dan visualisasi hasil menggunakan matplotlib.

- **app.py**: Aplikasi Streamlit yang menyediakan antarmuka interaktif untuk menjalankan simulasi tanpa perlu menjalankan notebook. User dapat mengatur parameter melalui sidebar dan melihat hasil simulasi secara real-time.

- **Reports/**: Folder yang menyimpan laporan perkembangan project mingguan dalam format Word, menjelaskan progress dan temuan pada setiap fase pengembangan.


## Cara Instalasi dan Menjalankan Project

### Prasyarat

- Python 3.7 atau lebih tinggi
- pip (Python package manager)

### Langkah-Langkah Instalasi

1. **Clone atau unduh project**

   Pastikan Anda berada di direktori project yang berisi file-file di atas.

2. **Buat virtual environment (opsional tetapi disarankan)**

   ```
   python -m venv venv
   ```

   Untuk Windows:
   ```
   venv\Scripts\activate
   ```

   Untuk macOS/Linux:
   ```
   source venv/bin/activate
   ```

3. **Install dependencies**

   ```
   pip install numpy pandas matplotlib streamlit
   ```

   Atau jika requirements.txt sudah diisi:
   ```
   pip install -r requirements.txt
   ```

### Menjalankan Simulasi

#### Opsi 1: Menggunakan Jupyter Notebook

```
jupyter notebook Main.ipynb
```

Setelah notebook terbuka di browser, jalankan sel-sel secara berurutan dengan menekan Shift+Enter atau gunakan tombol "Run All".

#### Opsi 2: Menggunakan Dashboard Streamlit (Rekomendasi)

```
streamlit run app.py
```

Dashboard akan terbuka di browser secara otomatis pada http://localhost:8501.


## Cara Menggunakan Dashboard

Dashboard Streamlit menyediakan antarmuka interaktif untuk menjalankan simulasi dengan parameter yang dapat dikustomisasi.

### Komponen Dashboard

**Bagian Sidebar (Parameter Simulasi):**

- **Discount Rate (%)**: Slider untuk mengatur tingkat diskon dari 0% hingga 50% (default: 30%). Mengubah nilai ini akan mempengaruhi probabilitas pembelian setiap agen.

- **Shopping Mood**: Slider untuk mengatur suasana hati belanja dari 0.0 hingga 1.0 (default: 0.5). Nilai yang lebih tinggi berarti pelanggan dalam suasana hati yang lebih baik untuk berbelanja.

- **Jumlah Agent**: Input numerik untuk menentukan berapa banyak pelanggan yang disimulasikan (default: 100, range 10-500). Semakin banyak agen, semakin representatif hasil simulasi tetapi membutuhkan waktu komputasi lebih lama.

- **Jumlah Iterasi**: Input numerik untuk menentukan berapa banyak putaran simulasi (default: 1000, range 100-5000). Lebih banyak iterasi menghasilkan statistik yang lebih stabil.

- **Tombol Jalankan Simulasi**: Tombol untuk memulai simulasi dengan parameter yang telah ditetapkan.

**Bagian Utama Dashboard:**

- **Metric Cards**: Menampilkan empat metrik statistik hasil simulasi:
  - Rata-rata Transaksi (Average Transactions)
  - Nilai Maksimum (Maximum)
  - Nilai Minimum (Minimum)
  - Standar Deviasi (Standard Deviation)

- **Grafik Monte Carlo**: Grafik garis interaktif yang menampilkan perubahan jumlah transaksi pada setiap iterasi simulasi. Grafik ini membantu visualisasi volatilitas dan tren dalam simulasi.

- **Ringkasan Hasil**: Tabel yang menampilkan data rinci per iterasi (jika tersedia).

### Cara Menggunakan Dashboard

1. Buka dashboard dengan menjalankan `streamlit run app.py`
2. Atur parameter simulasi sesuai kebutuhan melalui slider dan input di sidebar
3. Klik tombol "Jalankan Simulasi"
4. Tunggu proses simulasi selesai (waktu tergantung jumlah agen dan iterasi)
5. Hasil ditampilkan dalam bentuk metric cards, grafik, dan tabel
6. Untuk menjalankan simulasi lagi dengan parameter berbeda, ulangi langkah 2-4


## Hasil dan Analisis Simulasi

### Output yang Dihasilkan

Simulasi menghasilkan data transaksi untuk setiap iterasi, dari mana statistik dihitung:

- **Rata-rata Transaksi**: Jumlah rata-rata pembelian yang terjadi dalam setiap iterasi, mencerminkan efek berkelanjutan dari parameter simulasi.

- **Maksimum dan Minimum**: Nilai tertinggi dan terendah jumlah transaksi di seluruh iterasi, menunjukkan variabilitas hasil simulasi.

- **Standar Deviasi**: Mengukur sebaran data transaksi, membantu memahami konsistensi perilaku agen terhadap parameter yang diberikan.

### Pola Hasil yang Diharapkan

Dari ketiga skenario simulasi, pola berikut diharapkan muncul:

1. **Skenario 1 (Diskon)**: Peningkatan diskon secara konsisten menghasilkan peningkatan jumlah transaksi. Hubungan ini linear atau mendekati linear karena probabilitas pembelian berbanding lurus dengan diskon dalam model.

2. **Skenario 2 (Shopping Mood)**: Penambahan faktor shopping mood meningkatkan volatilitas hasil dibandingkan skenario dasar, karena ada dimensi acak tambahan (mood) yang memengaruhi keputusan.

3. **Skenario 3 (Monte Carlo)**: Kondisi high mood menghasilkan transaksi lebih banyak dibanding low mood, dengan normal mood berada di antara keduanya. Efek ini menunjukkan bahwa suasana hati kolektif memiliki dampak material pada hasil penjualan.

### Catatan Analisis

Hasil simulasi dapat dipengaruhi oleh seed random yang berbeda-beda. Untuk hasil yang konsisten, pertimbangkan untuk menetapkan seed random secara eksplisit dalam kode jika diperlukan analisis komparatif yang ketat.


## Teknologi yang Digunakan

- **Python 3.7+**: Bahasa pemrograman utama untuk implementasi simulasi
- **NumPy**: Library komputasi numerik untuk perhitungan matematika dan operasi array
- **Pandas**: Library untuk manipulasi data dan pembuatan DataFrame
- **Matplotlib**: Library untuk visualisasi data dan pembuatan grafik
- **Streamlit**: Framework untuk membangun dashboard interaktif tanpa perlu backend web kompleks
- **Jupyter Notebook**: Lingkungan interaktif untuk pengembangan dan dokumentasi kode

Semua library di atas adalah standard tools untuk scientific computing dan data visualization di Python.


## Catatan Pengembangan

### Asumsi Model

1. **Keputusan Pembelian Independen**: Model mengasumsikan keputusan pembelian setiap agen independen satu sama lain. Dalam realitas, ada efek network atau social influence yang tidak dimodelkan.

2. **Atribut Agen Statis**: Atribut agen (purchase probability, interest level, budget, shopping mood) ditetapkan sekali pada inisialisasi dan tidak berubah selama simulasi. Dalam konteks nyata, atribut ini bisa berubah seiring waktu.

3. **Diskon Seragam**: Diskon diterapkan secara seragam kepada semua agen dan tidak berubah selama simulasi. Strategi pricing dinamis tidak dipertimbangkan.

4. **Distribusi Uniform**: Semua parameter agen diinisialisasi dari distribusi uniform dalam range yang ditentukan. Distribusi lain (misalnya normal atau exponential) bisa memberikan hasil berbeda.

5. **Horizon Waktu Terbatas**: Simulasi adalah snapshot statis dari beberapa iterasi. Dinamika jangka panjang (seperti pembelajaran agen atau perubahan preferensi) tidak dimodelkan.

### Batasan Teknis

1. **Skalabilitas**: Dengan 500 agen dan 5000 iterasi, simulasi mungkin membutuhkan waktu beberapa detik. Untuk skala lebih besar, pertimbangkan optimisasi atau parallelization.

2. **Random Seed**: Setiap kali simulasi dijalankan, hasil akan berbeda karena randomness. Untuk reproducibility, tetapkan seed random di awal kode.

3. **Visualisasi**: Dashboard Streamlit menyediakan visualisasi dasar. Untuk analisis statistik lebih dalam atau publikasi, pertimbangkan tools visualisasi tambahan seperti Seaborn atau Plotly.

### Pengembangan Lebih Lanjut

Beberapa ide untuk memperluas project:

1. **Agent Learning**: Implementasikan mekanisme pembelajaran agar agen dapat mengubah atribut mereka berdasarkan pengalaman pembelian sebelumnya.

2. **Social Influence**: Tambahkan dinamika interaksi antar agen, misalnya word-of-mouth atau efek herd behavior.

3. **Temporal Dynamics**: Simulasi multi-periode di mana preferensi agen dan kondisi pasar berubah seiring waktu.

4. **Advanced Analytics**: Tambahkan analisis statistik lebih lanjut, clustering, atau machine learning untuk memprediksi outcome simulasi berdasarkan parameter input.

5. **Validation**: Validasi model dengan data empiris real dari e-commerce platform untuk memastikan model mencerminkan perilaku nyata.

### Troubleshooting

- **Streamlit Error "ModuleNotFoundError"**: Pastikan semua dependencies telah diinstall dengan `pip install -r requirements.txt` atau instalasi manual.

- **Dashboard Tidak Merespons**: Jika dashboard freeze setelah klik "Jalankan Simulasi", jumlah agent atau iterasi mungkin terlalu besar. Coba kurangi nilainya.

- **Grafik Tidak Ditampilkan**: Pastikan Matplotlib dan Streamlit terinstall dengan benar. Clear browser cache jika grafik tidak muncul.

