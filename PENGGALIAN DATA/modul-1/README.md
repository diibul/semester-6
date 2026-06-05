# Ringkasan Tugas

## Identitas
- Nama: Muhammad Iqbal Fadel
- NIM: 202310370311268
- Kelas: Penggalian Data C

## Instruksi Tugas
### CODELAB 1
- a. Buat 12 tuple data, masing-masing berisi 4 data int, float, dan string dalam urutan acak.
- b. Konversi tuple menjadi list.
- c. Tambahkan 2 data baru pada indeks sesuai digit terakhir NIM (jika 0, gunakan indeks 10).
- d. Hapus tipe data float dari list.
- e. Urutkan elemen list secara descending.

### CODELAB 2
- a. Buat array 2D berdasarkan 6 digit terakhir NIM.
- b. Lakukan operasi penjumlahan, pengurangan, dan perkalian pada matriks tersebut.
- c. Ubah matriks ke bentuk 1D.
- d. Lakukan slicing pada matriks.

### CODELAB 3
- a. Buat series berisi dictionary dengan nama produk dan ID produk.
- b. Buat dataframe berisi dictionary dengan 4 kolom, masing-masing 5 data (tidak boleh sama antar mahasiswa).
- c. Tambahkan 1 kolom baru.
- d. Urutkan dataframe, misal alfabetis jika kolomnya "Name".

## Modul1_lab_assigment (LAB ASSIGNMENT 80%)

Semua pengerjaan ada di notebook `Modul1_lab_assigment.ipynb`.

### ASSIGNMENT 1
Buat sebuah fungsi yang menerima list sebagai parameter dan melakukan operasi berikut:
- Menambahkan 10 elemen numerik acak (tipe campuran int dan float).
- Menghapus elemen pada indeks tertentu sesuai NIM (ganjil/genap, disesuaikan aturan di kelas).
- Membalik urutan seluruh elemen dalam list (reverse).
- Menghapus elemen dengan nilai terbesar dari list.
- Mengurutkan sisa elemen dalam list secara descending.

### ASSIGNMENT 2
Buat sebuah tuple yang berisi dictionary dengan 10 pasangan key-value (mata kuliah dan nilai),
setidaknya 3 di antaranya memiliki nilai kosong. Lakukan operasi berikut:
- Menghapus entri yang tidak lengkap atau memiliki nilai kosong.
- Menghitung jumlah entri yang tersisa setelah penghapusan.
- Mengurutkan pasangan key-value berdasarkan nilai secara ascending.
- Menemukan mata kuliah dengan nilai tertinggi.
- Menghitung nilai rata-rata dari seluruh mata kuliah.

### ASSIGNMENT 3 (NIM GENAP)
Buat sebuah DataFrame dengan 10 baris dan 6 kolom dengan informasi:
- Brand, Branch, Price (ribu), Stock, Status, dan (jika ada) kolom tambahan sesuai kebutuhan.
- Data contoh mengacu pada tabel kosmetik (Avoskin, G2G, Skintific, Wardah, Emina, Somethinc, Azarine, Lacoco, Y.O.U, Madame Gie) dengan variasi harga, stok, dan status (Sold/Available).

Lakukan analisis berikut pada DataFrame:
- Menampilkan ringkasan statistik deskriptif: min, max, sum, mean, standar deviasi, serta kuartil 1, 2, dan 3.
- Mengidentifikasi 3 brand dengan revenue terbesar (price × stock).
- Mengelompokkan brand dengan harga yang sama (group by price).
- Membuat kolom kategori baru dengan label "Cheap", "Medium", dan "Expensive" berdasarkan aturan:
	- Harga di bawah kuartil 1 → "Cheap".
	- Harga di antara kuartil 1 dan kuartil 3 → "Medium".
	- Harga di atas kuartil 3 → "Expensive".

## Catatan
- Semua contoh kode ada di notebook: codelab1.ipynb, codelab2.ipynb, codelab3.ipynb.
- Jalankan setiap sel secara berurutan untuk melihat hasilnya.
