# Data Mining Progress - E-commerce Sales Transactions

## Ringkasan Singkat
Dataset ini berisi transaksi penjualan e-commerce berbasis UK (online retail) selama 1 tahun. Toko menjual hadiah dan homewares untuk dewasa serta anak, dengan pelanggan dari berbagai negara. Data digunakan untuk memahami pola penjualan, perilaku pelanggan, dan peluang peningkatan profit.

## Konteks
E-commerce menjadi kanal penting untuk memperluas pasar melalui distribusi yang lebih murah dan efisien. Perilaku belanja juga berubah karena pelanggan dapat membeli produk secara online dari komputer atau perangkat pintar.

## Gambaran Dataset
- Sumber: UK-based online retail transactions
- Ukuran: sekitar 500K baris
- Jumlah kolom: 8
- License: CC0 (Public Domain)
- Usability: 10.00
- Update frequency: Never
- Tags: Business, Tabular, Retail and Shopping

## Deskripsi Kolom
- TransactionNo (categorical): ID transaksi 6 digit; huruf C menandakan pembatalan.
- Date (date): Tanggal transaksi.
- ProductNo (categorical): ID unik produk (5-6 digit/karakter).
- ProductName (categorical): Nama produk.
- Price (numeric): Harga per unit dalam pound sterling (GBP).
- Quantity (numeric): Jumlah unit per transaksi; nilai negatif terkait pembatalan.
- CustomerNo (categorical): ID unik pelanggan.
- Country (categorical): Negara pelanggan.

## Catatan Data
Terdapat sebagian kecil transaksi pembatalan, umumnya karena stok produk tidak tersedia sehingga pelanggan membatalkan pesanan.

## Progress yang Sudah Dikerjakan (Data Cleaning)
Pembersihan dilakukan di notebook [DataProsecing.ipynb](DataProsecing.ipynb) dengan langkah utama:
1. Load data CSV dengan pemisah ;
2. Standardisasi nama kolom;
3. Trim whitespace pada kolom teks;
4. Normalisasi nilai Country (termasuk typo seperti United King dom -> United Kingdom);
5. Konversi tipe data (Date, Price, Quantity);
6. Hapus duplikasi baris;
7. Tangani missing value pada kolom kritis;
8. Terapkan business rule (Price > 0, Quantity > 0);
9. Buat fitur baru TotalAmount dan YearMonth;
10. Simpan hasil ke [Sales_Transaction_v4a_cleaned.csv](Sales_Transaction_v4a_cleaned.csv).

## Hasil Cleaning (Ringkas)
- Data awal: 536,350 baris
- Setelah hapus duplikat: 531,150 baris
- Setelah drop missing (kolom kritis): 531,095 baris
- Data final setelah business-rule cleaning: 522,601 baris
- Missing value pada kolom utama setelah cleaning: 0

## Pertanyaan Analisis Lanjutan
1. Bagaimana tren penjualan per bulan?
2. Produk apa yang paling sering dibeli?
3. Berapa jumlah produk per transaksi?
4. Segmen pelanggan mana yang paling menguntungkan?
5. Strategi apa yang direkomendasikan untuk meningkatkan profit?

## Next Step yang Disarankan
- Lakukan EDA terarah: tren bulanan, top product, sebaran negara, dan pola quantity per transaksi.
- Segmentasi pelanggan berbasis nilai belanja (misal RFM sederhana).
- Rumuskan rekomendasi bisnis berbasis temuan data.
