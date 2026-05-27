"""
modelling.py
============
Pipeline Machine Learning untuk Klasifikasi Sentimen Ulasan Parfum Lokal.

Algoritma yang digunakan:
  - Model 1: Support Vector Machine (SVM) dengan LinearSVC
  - Model 2: Multinomial Naive Bayes (MNB)

Penanganan Data Tidak Seimbang:
  - Menggunakan class_weight='balanced' pada SVM
  - Menggunakan SMOTE (oversampling) pada data latih untuk Naive Bayes

Ekstraksi Fitur:
  - TF-IDF (Term Frequency - Inverse Document Frequency)

Penulis : Muhammad Iqbal Fadel | 202310370311268
Mata Kuliah : Data, Informasi, dan Pengetahuan
"""

import sys
import os
import logging
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    f1_score,
)

warnings.filterwarnings("ignore")

# ── Konfigurasi Path ────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

from config import (
    PROCESSED_DIR, PROCESSED_FILENAME,
    FIGURES_DIR, REPORTS_DIR, MODELS_DIR,
    COL_TEXT_NORM, COL_LABEL,
)

# ── Logging ─────────────────────────────────────────────────────
sys.stdout.reconfigure(encoding="utf-8")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("Modelling")


# =================================================================
#  STEP 1 — Muat & Siapkan Data
# =================================================================
def muat_data() -> pd.DataFrame:
    """Membaca dataset hasil preprocessing dan membuang baris kosong."""
    filepath = PROCESSED_DIR / PROCESSED_FILENAME
    log.info(f"Memuat dataset dari: {filepath.name}")

    try:
        df = pd.read_csv(filepath, encoding="utf-8")
    except Exception as e:
        log.error(f"Gagal membaca file: {e}")
        raise

    sebelum = len(df)
    df = df.dropna(subset=[COL_TEXT_NORM, COL_LABEL])
    sesudah = len(df)

    if sebelum != sesudah:
        log.info(f"  Baris kosong dibuang: {sebelum - sesudah}")

    log.info(f"  Total data valid: {sesudah:,} baris")
    log.info(f"  Distribusi label:")
    for label, jumlah in df[COL_LABEL].value_counts().items():
        pct = jumlah / sesudah * 100
        log.info(f"    - {label}: {jumlah} ({pct:.1f}%)")

    return df


# =================================================================
#  STEP 2 — Ekstraksi Fitur dengan TF-IDF
# =================================================================
def ekstraksi_fitur(df: pd.DataFrame):
    """
    Mengubah teks menjadi representasi numerik menggunakan TF-IDF.

    TF-IDF dipilih karena:
    - Cocok untuk dataset berukuran kecil-menengah
    - Mampu memberikan bobot tinggi pada kata-kata yang khas/unik
    - Kompatibel langsung dengan SVM dan Naive Bayes
    """
    log.info("Mengekstraksi fitur TF-IDF dari teks...")

    tfidf = TfidfVectorizer(
        max_features=5000,      # Batasi 5000 fitur teratas
        ngram_range=(1, 2),     # Gunakan unigram + bigram
        min_df=2,               # Abaikan kata yang muncul < 2 dokumen
        max_df=0.95,            # Abaikan kata yang muncul di > 95% dokumen
        sublinear_tf=True,      # Gunakan 1 + log(tf) untuk normalisasi
    )

    X = tfidf.fit_transform(df[COL_TEXT_NORM])
    y = df[COL_LABEL]

    log.info(f"  Dimensi matriks TF-IDF: {X.shape[0]} dokumen x {X.shape[1]} fitur")

    return X, y, tfidf


# =================================================================
#  STEP 3 — Bagi Data Latih & Data Uji
# =================================================================
def bagi_data(X, y, test_size=0.2, random_state=42):
    """
    Membagi data menjadi 80% latih dan 20% uji.
    Menggunakan stratify agar proporsi kelas tetap terjaga di kedua set.
    """
    log.info(f"Membagi data: {int((1-test_size)*100)}% latih, {int(test_size*100)}% uji (stratified)...")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    log.info(f"  Data latih: {X_train.shape[0]} baris")
    log.info(f"  Data uji  : {X_test.shape[0]} baris")

    return X_train, X_test, y_train, y_test


# =================================================================
#  STEP 4 — Penanganan Data Tidak Seimbang dengan SMOTE
# =================================================================
def terapkan_smote(X_train, y_train):
    """
    Menerapkan SMOTE (Synthetic Minority Oversampling Technique)
    HANYA pada data latih untuk menghindari data leakage.

    SMOTE bekerja dengan cara membuat sampel sintetis (buatan) untuk
    kelas minoritas (Negatif dan Netral) sehingga jumlahnya setara
    dengan kelas mayoritas (Positif).

    Catatan: SMOTE TIDAK boleh diterapkan pada data uji karena akan
    menghasilkan evaluasi yang tidak valid (data leakage).
    """
    try:
        from imblearn.over_sampling import SMOTE

        log.info("Menerapkan SMOTE pada data latih...")
        log.info(f"  Sebelum SMOTE: {dict(pd.Series(y_train).value_counts())}")

        smote = SMOTE(random_state=42, k_neighbors=1)
        X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

        log.info(f"  Sesudah SMOTE: {dict(pd.Series(y_resampled).value_counts())}")
        return X_resampled, y_resampled

    except ImportError:
        log.warning("Library imbalanced-learn belum terinstall.")
        log.warning("Lanjut tanpa SMOTE, menggunakan class_weight sebagai gantinya.")
        return X_train, y_train


# =================================================================
#  STEP 5 — Pelatihan Model
# =================================================================
def latih_svm(X_train, y_train):
    """
    Melatih model Support Vector Machine (SVM) dengan LinearSVC.

    Alasan memilih SVM:
    - Performa terbaik untuk klasifikasi teks berdimensi tinggi
    - class_weight='balanced' otomatis menyesuaikan bobot kelas
      sehingga kelas minoritas mendapat perhatian lebih
    - Linear kernel sangat efisien untuk data TF-IDF yang sparse
    """
    log.info("Melatih model SVM (LinearSVC)...")

    # LinearSVC tidak punya predict_proba, jadi dibungkus CalibratedClassifierCV
    base_svm = LinearSVC(
        class_weight="balanced",
        max_iter=10000,
        random_state=42,
        C=1.0,
    )
    model = CalibratedClassifierCV(base_svm, cv=3)
    model.fit(X_train, y_train)

    log.info("  Model SVM berhasil dilatih.")
    return model


def latih_naive_bayes(X_train, y_train):
    """
    Melatih model Multinomial Naive Bayes (MNB).

    Alasan memilih Naive Bayes:
    - Baseline klasik untuk klasifikasi teks
    - Sangat cepat dan ringan secara komputasi
    - Bekerja baik dengan fitur frekuensi kata (TF-IDF)
    - alpha=0.1 sebagai smoothing agar tidak ada probabilitas nol
    """
    log.info("Melatih model Naive Bayes (MultinomialNB)...")

    model = MultinomialNB(alpha=0.1)
    model.fit(X_train, y_train)

    log.info("  Model Naive Bayes berhasil dilatih.")
    return model


# =================================================================
#  STEP 6 — Evaluasi Model
# =================================================================
def evaluasi_model(model, X_test, y_test, nama_model: str) -> dict:
    """Mengevaluasi performa model dan mencetak hasilnya."""
    log.info(f"Mengevaluasi model {nama_model}...")

    y_pred = model.predict(X_test)

    akurasi = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average="macro", zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average="weighted", zero_division=0)

    report_str = classification_report(
        y_test, y_pred, zero_division=0, digits=4
    )

    log.info(f"  Akurasi        : {akurasi:.4f} ({akurasi*100:.2f}%)")
    log.info(f"  F1-Score Macro  : {f1_macro:.4f}")
    log.info(f"  F1-Score Weighted: {f1_weighted:.4f}")

    return {
        "nama": nama_model,
        "akurasi": akurasi,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "report": report_str,
        "y_pred": y_pred,
        "model": model,
    }


# =================================================================
#  STEP 7 — Visualisasi Confusion Matrix
# =================================================================
def simpan_confusion_matrix(y_test, y_pred, nama_model: str, labels: list):
    """Membuat dan menyimpan visualisasi Confusion Matrix."""
    cm = confusion_matrix(y_test, y_pred, labels=labels)

    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=labels,
        yticklabels=labels,
        linewidths=0.5,
        linecolor="gray",
        ax=ax,
    )
    ax.set_title(f"Confusion Matrix - {nama_model}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Prediksi", fontsize=12)
    ax.set_ylabel("Aktual", fontsize=12)
    plt.tight_layout()

    filename = f"confusion_matrix_{nama_model.lower().replace(' ', '_')}.png"
    filepath = FIGURES_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)

    log.info(f"  Confusion matrix disimpan: {filepath.name}")


def simpan_perbandingan_model(hasil_svm: dict, hasil_nb: dict):
    """Membuat visualisasi perbandingan performa kedua model."""
    metrik = ["Akurasi", "F1 Macro", "F1 Weighted"]
    skor_svm = [hasil_svm["akurasi"], hasil_svm["f1_macro"], hasil_svm["f1_weighted"]]
    skor_nb = [hasil_nb["akurasi"], hasil_nb["f1_macro"], hasil_nb["f1_weighted"]]

    x = np.arange(len(metrik))
    lebar = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    bar1 = ax.bar(x - lebar/2, skor_svm, lebar, label="SVM", color="#2196F3", edgecolor="white")
    bar2 = ax.bar(x + lebar/2, skor_nb, lebar, label="Naive Bayes", color="#FF9800", edgecolor="white")

    ax.set_ylabel("Skor", fontsize=12)
    ax.set_title("Perbandingan Performa Model", fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(metrik, fontsize=11)
    ax.set_ylim(0, 1.15)
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.3)

    for bar in bar1:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{bar.get_height():.3f}", ha="center", fontsize=10, fontweight="bold")
    for bar in bar2:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{bar.get_height():.3f}", ha="center", fontsize=10, fontweight="bold")

    plt.tight_layout()
    filepath = FIGURES_DIR / "perbandingan_model.png"
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)

    log.info(f"  Grafik perbandingan disimpan: {filepath.name}")


# =================================================================
#  STEP 8 — Simpan Artefak (Model, Laporan)
# =================================================================
def simpan_model(model, tfidf, nama_file_model: str):
    """Menyimpan model terlatih dan TF-IDF vectorizer ke file .pkl."""
    model_path = MODELS_DIR / nama_file_model
    tfidf_path = MODELS_DIR / "tfidf_vectorizer.pkl"

    joblib.dump(model, model_path)
    joblib.dump(tfidf, tfidf_path)

    log.info(f"  Model disimpan   : {model_path.name}")
    log.info(f"  Vectorizer disimpan: {tfidf_path.name}")


def simpan_laporan_evaluasi(hasil_svm: dict, hasil_nb: dict, pemenang: str):
    """Menyimpan laporan evaluasi perbandingan kedua model ke file teks."""
    filepath = REPORTS_DIR / "ml_evaluation_report.txt"

    garis = "=" * 65

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{garis}\n")
        f.write("  LAPORAN EVALUASI MODEL MACHINE LEARNING\n")
        f.write("  Klasifikasi Sentimen Ulasan Parfum Lokal\n")
        f.write(f"  Muhammad Iqbal Fadel | 202310370311268\n")
        f.write(f"{garis}\n\n")

        for hasil in [hasil_svm, hasil_nb]:
            f.write(f"--- {hasil['nama']} ---\n")
            f.write(f"Akurasi          : {hasil['akurasi']:.4f} ({hasil['akurasi']*100:.2f}%)\n")
            f.write(f"F1-Score (Macro)  : {hasil['f1_macro']:.4f}\n")
            f.write(f"F1-Score (Weighted): {hasil['f1_weighted']:.4f}\n\n")
            f.write("Classification Report:\n")
            f.write(hasil["report"])
            f.write("\n\n")

        f.write(f"{garis}\n")
        f.write(f"  KESIMPULAN: Model terbaik adalah {pemenang}\n")
        f.write(f"{garis}\n")

    log.info(f"  Laporan evaluasi disimpan: {filepath.name}")


# =================================================================
#  MAIN — Orkestrasi Seluruh Pipeline
# =================================================================
def main():
    """Fungsi utama yang menjalankan seluruh pipeline ML secara berurutan."""
    log.info("")
    log.info("=" * 60)
    log.info("  PIPELINE MACHINE LEARNING - KLASIFIKASI SENTIMEN")
    log.info("  Muhammad Iqbal Fadel | 202310370311268")
    log.info("=" * 60)
    log.info("")

    # 1. Muat data
    df = muat_data()

    # 2. Ekstraksi fitur TF-IDF
    X, y, tfidf = ekstraksi_fitur(df)

    # 3. Bagi data latih & uji
    X_train, X_test, y_train, y_test = bagi_data(X, y)

    # 4. Terapkan SMOTE pada data latih (untuk Naive Bayes)
    X_train_smote, y_train_smote = terapkan_smote(X_train, y_train)

    # 5. Latih model
    # SVM menggunakan class_weight='balanced' (tanpa SMOTE)
    model_svm = latih_svm(X_train, y_train)
    # Naive Bayes menggunakan data yang sudah di-SMOTE
    model_nb = latih_naive_bayes(X_train_smote, y_train_smote)

    # 6. Evaluasi model
    hasil_svm = evaluasi_model(model_svm, X_test, y_test, "SVM")
    hasil_nb = evaluasi_model(model_nb, X_test, y_test, "Naive Bayes")

    # 7. Tentukan model terbaik berdasarkan F1-Score Weighted
    #    (Weighted lebih adil untuk data yang tidak seimbang)
    if hasil_svm["f1_weighted"] >= hasil_nb["f1_weighted"]:
        pemenang = "SVM"
        model_terbaik = model_svm
    else:
        pemenang = "Naive Bayes"
        model_terbaik = model_nb

    log.info("")
    log.info(f"  Model terbaik: {pemenang}")
    log.info("")

    # 8. Simpan visualisasi
    labels = sorted(y.unique())
    simpan_confusion_matrix(y_test, hasil_svm["y_pred"], "SVM", labels)
    simpan_confusion_matrix(y_test, hasil_nb["y_pred"], "Naive Bayes", labels)
    simpan_perbandingan_model(hasil_svm, hasil_nb)

    # 9. Simpan model terbaik & vectorizer
    nama_file = f"model_terbaik_{pemenang.lower().replace(' ', '_')}.pkl"
    simpan_model(model_terbaik, tfidf, nama_file)

    # 10. Simpan laporan evaluasi
    simpan_laporan_evaluasi(hasil_svm, hasil_nb, pemenang)

    # Ringkasan akhir
    log.info("")
    log.info("=" * 60)
    log.info("  PIPELINE ML SELESAI")
    log.info("=" * 60)
    log.info(f"  Model terbaik   : {pemenang}")
    log.info(f"  Akurasi          : {max(hasil_svm['akurasi'], hasil_nb['akurasi'])*100:.2f}%")
    log.info(f"  Output tersimpan di:")
    log.info(f"    - results/figures/  (confusion matrix, perbandingan)")
    log.info(f"    - results/models/   (model .pkl, vectorizer .pkl)")
    log.info(f"    - results/reports/  (ml_evaluation_report.txt)")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
