# Laporan Mingguan — Minggu 13 & 14
## Drafting Jurnal & Finalisasi Dokumentasi

| Field | Detail |
|---|---|
| **Nama** | Muhammad Iqbal Fadel |
| **NIM** | 202310370311268 |
| **Periode** | Minggu 13–14 (Bulan 4) |
| **Tanggal** | Juni 2026 |
| **Status** | SELESAI |

---

## Capaian Minggu Ini

- [x] Menyelesaikan pipeline machine learning (SVM & Naive Bayes) dari minggu sebelumnya
- [x] Membuat draft artikel jurnal di `docs/jurnal/draft_jurnal.md`
- [x] Menyusun metodologi lengkap termasuk alasan tidak menggunakan stemming
- [x] Mendokumentasikan seluruh hasil evaluasi model ke dalam narasi jurnal
- [x] Memperbarui README.md agar lebih informatif dan profesional
- [x] Menambahkan contoh transformasi teks (sebelum-sesudah) di README

---

## Hasil Machine Learning (Rekap dari Minggu 13)

Eksperimen klasifikasi sentimen dilakukan menggunakan dua model dengan TF-IDF (1,2)-gram sebagai representasi fitur. Data latih berjumlah 694 baris (80%) dan data uji 174 baris (20%).

| Model | Akurasi | F1-Macro | F1-Weighted |
|---|---|---|---|
| Multinomial Naive Bayes | 92,53% | 0,7102 | 0,9227 |
| SVM (LinearSVC) | 89,66% | 0,6163 | 0,8776 |

Model terbaik adalah **Naive Bayes** dengan akurasi 92,53%.

Penanganan class imbalance:
- Naive Bayes: SMOTE pada data latih
- SVM: `class_weight='balanced'`

---

## Progres Jurnal

Draft jurnal sudah mencakup seluruh komponen yang disyaratkan:

| Bagian | Status |
|---|---|
| Abstrak | Selesai |
| Pendahuluan & Latar Belakang | Selesai |
| Metodologi (6 tahap preprocessing) | Selesai |
| Alasan tidak pakai Stemming | Selesai — terdokumentasi di bagian 2.4 |
| Deskripsi Data (tabel statistik) | Selesai |
| Hasil ML | Selesai |
| Nilai Guna Dataset | Selesai |
| Keterbatasan | Selesai |
| Referensi | 5 referensi terkait |

---

## Output

| File | Lokasi |
|---|---|
| `draft_jurnal.md` | `docs/jurnal/` |
| `model_terbaik_naive_bayes.pkl` | `results/models/` |
| `tfidf_vectorizer.pkl` | `results/models/` |
| `perbandingan_model.png` | `results/figures/` |
| `confusion_matrix_naive_bayes.png` | `results/figures/` |
| `confusion_matrix_svm.png` | `results/figures/` |

---

## Rencana Minggu 15-16

- [ ] Finalisasi semua file untuk GitHub push
- [ ] Pastikan README sudah menampilkan word cloud sebelum-sesudah
- [ ] Verifikasi struktur folder sesuai arahan penugasan
- [ ] Push ke GitHub dan rapikan repositori
- [ ] Siapkan link GitHub untuk pengumpulan UAS
