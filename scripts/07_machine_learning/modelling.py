"""
modelling.py
============
Pipeline Machine Learning untuk Klasifikasi Sentimen Ulasan Parfum Lokal.

Algoritma:
  - Model 1: Support Vector Machine (SVM) dengan LinearSVC
  - Model 2: Multinomial Naive Bayes (MNB)

Penanganan Imbalance:
  - class_weight='balanced' pada SVM
  - SMOTE pada data latih untuk Naive Bayes

Ekstraksi Fitur:
  - TF-IDF -- PENTING: di-fit HANYA pada data latih (mencegah data leakage)

Evaluasi:
  - Train-test split 80/20 (stratified)
  - 5-Fold Stratified Cross Validation menggunakan sklearn Pipeline

Penulis : Muhammad Iqbal Fadel | 202310370311268
Mata Kuliah : Data, Informasi, dan Pengetahuan
"""

import sys
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
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
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

# -- Path ---------------------------------------------------------------
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

from config import (
    PROCESSED_DIR, PROCESSED_FILENAME,
    FIGURES_DIR, REPORTS_DIR, MODELS_DIR,
    COL_TEXT_NORM, COL_LABEL,
)

# -- Logging ------------------------------------------------------------
sys.stdout.reconfigure(encoding="utf-8")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("Modelling")


# =======================================================================
#  STEP 1 -- Muat Data
# =======================================================================
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
        log.info(f"    - {label}: {jumlah} ({jumlah/sesudah*100:.1f}%)")
    return df


# =======================================================================
#  STEP 2 -- Bagi Data (teks mentah, SEBELUM TF-IDF)
# =======================================================================
def bagi_data(X_text: pd.Series, y: pd.Series,
              test_size: float = 0.2, random_state: int = 42):
    """
    Membagi teks mentah menjadi 80% latih dan 20% uji SEBELUM TF-IDF di-fit.
    Langkah ini mencegah data leakage: statistik IDF dari data uji tidak
    boleh masuk ke dalam proses pelatihan model.
    """
    log.info(f"Membagi teks: {int((1-test_size)*100)}% latih / "
             f"{int(test_size*100)}% uji (stratified)...")
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_text, y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )
    log.info(f"  Data latih: {len(X_train_raw)} baris")
    log.info(f"  Data uji  : {len(X_test_raw)} baris")
    return X_train_raw, X_test_raw, y_train, y_test


# =======================================================================
#  STEP 3 -- Ekstraksi Fitur TF-IDF (fit HANYA pada data latih)
# =======================================================================
def ekstraksi_fitur(X_train_raw: pd.Series, X_test_raw: pd.Series):
    """
    Mengubah teks menjadi representasi numerik TF-IDF.

    PERBAIKAN DATA LEAKAGE:
    - tfidf.fit_transform() -> HANYA pada X_train_raw
    - tfidf.transform()     -> pada X_test_raw (vocabulary dari train)
    Statistik IDF data uji tidak mempengaruhi proses pelatihan.
    """
    log.info("Mengekstraksi fitur TF-IDF (fit pada train only)...")
    tfidf = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        min_df=2,
        max_df=0.95,
        sublinear_tf=True,
    )
    X_train = tfidf.fit_transform(X_train_raw)   # fit + transform pada train
    X_test  = tfidf.transform(X_test_raw)         # transform saja pada test
    log.info(f"  Dimensi train: {X_train.shape[0]} dok x {X_train.shape[1]} fitur")
    log.info(f"  Dimensi test : {X_test.shape[0]} dok x {X_test.shape[1]} fitur")
    return X_train, X_test, tfidf


# =======================================================================
#  STEP 4 -- SMOTE (hanya pada data latih)
# =======================================================================
def terapkan_smote(X_train, y_train):
    """
    SMOTE diterapkan HANYA pada data latih (setelah split).
    Data uji tidak tersentuh, sehingga evaluasi tetap valid.
    """
    try:
        from imblearn.over_sampling import SMOTE
        log.info("Menerapkan SMOTE pada data latih...")
        log.info(f"  Sebelum SMOTE: {dict(pd.Series(y_train).value_counts())}")
        smote = SMOTE(random_state=42, k_neighbors=1)
        X_res, y_res = smote.fit_resample(X_train, y_train)
        log.info(f"  Sesudah SMOTE: {dict(pd.Series(y_res).value_counts())}")
        return X_res, y_res
    except ImportError:
        log.warning("imbalanced-learn belum terinstall. Lanjut tanpa SMOTE.")
        return X_train, y_train


# =======================================================================
#  STEP 5 -- Pelatihan Model
# =======================================================================
def latih_svm(X_train, y_train):
    """SVM LinearSVC dengan class_weight='balanced'."""
    log.info("Melatih model SVM (LinearSVC)...")
    base_svm = LinearSVC(
        class_weight="balanced", max_iter=10000,
        random_state=42, C=1.0,
    )
    model = CalibratedClassifierCV(base_svm, cv=3)
    model.fit(X_train, y_train)
    log.info("  Model SVM selesai dilatih.")
    return model


def latih_naive_bayes(X_train, y_train):
    """Multinomial Naive Bayes dengan alpha=0.1 (Laplace smoothing)."""
    log.info("Melatih model Naive Bayes (MultinomialNB)...")
    model = MultinomialNB(alpha=0.1)
    model.fit(X_train, y_train)
    log.info("  Model Naive Bayes selesai dilatih.")
    return model


# =======================================================================
#  STEP 6 -- Evaluasi Model (train-test split)
# =======================================================================
def evaluasi_model(model, X_test, y_test, nama_model: str) -> dict:
    """Evaluasi performa model pada data uji."""
    log.info(f"Mengevaluasi {nama_model}...")
    y_pred = model.predict(X_test)
    akurasi    = accuracy_score(y_test, y_pred)
    f1_macro   = f1_score(y_test, y_pred, average="macro",    zero_division=0)
    f1_weighted = f1_score(y_test, y_pred, average="weighted", zero_division=0)
    report_str = classification_report(y_test, y_pred, zero_division=0, digits=4)
    log.info(f"  Akurasi          : {akurasi:.4f} ({akurasi*100:.2f}%)")
    log.info(f"  F1-Score Macro    : {f1_macro:.4f}")
    log.info(f"  F1-Score Weighted : {f1_weighted:.4f}")
    return {
        "nama": nama_model,
        "akurasi": akurasi,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "report": report_str,
        "y_pred": y_pred,
        "model": model,
    }


# =======================================================================
#  STEP 7 -- 5-Fold Cross Validation (sklearn Pipeline)
# =======================================================================
def cross_validate_model(df: pd.DataFrame,
                         nama_model: str = "Naive Bayes",
                         cv: int = 5) -> dict:
    """
    Menjalankan k-Fold Stratified Cross Validation menggunakan sklearn Pipeline.

    Pipeline memastikan TF-IDF di-fit ulang di setiap fold hanya pada data
    latih fold tersebut -- tidak ada data leakage antar fold.

    Catatan: CV ini tidak menyertakan SMOTE di setiap fold (memerlukan
    imblearn.Pipeline yang terpisah). SVM menggunakan class_weight='balanced'.
    """
    log.info(f"Menjalankan {cv}-Fold Cross Validation [{nama_model}]...")
    X_text = df[COL_TEXT_NORM]
    y      = df[COL_LABEL]

    tfidf = TfidfVectorizer(
        max_features=5000, ngram_range=(1, 2),
        min_df=2, max_df=0.95, sublinear_tf=True,
    )
    if nama_model == "Naive Bayes":
        clf = MultinomialNB(alpha=0.1)
    else:
        clf = LinearSVC(class_weight="balanced", max_iter=10000,
                        random_state=42, C=1.0)

    pipe = Pipeline([("tfidf", tfidf), ("clf", clf)])
    skf  = StratifiedKFold(n_splits=cv, shuffle=True, random_state=42)

    scores = cross_validate(
        pipe, X_text, y, cv=skf,
        scoring=["accuracy", "f1_macro", "f1_weighted"],
        error_score="raise",
    )

    acc_mean  = scores["test_accuracy"].mean()
    acc_std   = scores["test_accuracy"].std()
    f1m_mean  = scores["test_f1_macro"].mean()
    f1m_std   = scores["test_f1_macro"].std()
    f1w_mean  = scores["test_f1_weighted"].mean()
    f1w_std   = scores["test_f1_weighted"].std()

    log.info(f"  Akurasi     : {acc_mean:.4f} +- {acc_std:.4f}")
    log.info(f"  F1-Macro    : {f1m_mean:.4f} +- {f1m_std:.4f}")
    log.info(f"  F1-Weighted : {f1w_mean:.4f} +- {f1w_std:.4f}")

    return {
        "nama": nama_model, "cv": cv,
        "acc_mean": acc_mean, "acc_std": acc_std,
        "f1_macro_mean": f1m_mean, "f1_macro_std": f1m_std,
        "f1_weighted_mean": f1w_mean, "f1_weighted_std": f1w_std,
        "raw_scores": scores,
    }


# =======================================================================
#  STEP 8 -- Visualisasi
# =======================================================================
def simpan_confusion_matrix(y_test, y_pred, nama_model: str, labels: list):
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels,
                linewidths=0.5, linecolor="gray", ax=ax)
    ax.set_title(f"Confusion Matrix - {nama_model}", fontsize=14, fontweight="bold")
    ax.set_xlabel("Prediksi", fontsize=12)
    ax.set_ylabel("Aktual",   fontsize=12)
    plt.tight_layout()
    filename = f"confusion_matrix_{nama_model.lower().replace(' ', '_')}.png"
    filepath = FIGURES_DIR / filename
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info(f"  Confusion matrix disimpan: {filepath.name}")


def simpan_perbandingan_model(hasil_svm: dict, hasil_nb: dict):
    metrik   = ["Akurasi", "F1 Macro", "F1 Weighted"]
    skor_svm = [hasil_svm["akurasi"], hasil_svm["f1_macro"], hasil_svm["f1_weighted"]]
    skor_nb  = [hasil_nb["akurasi"],  hasil_nb["f1_macro"],  hasil_nb["f1_weighted"]]
    x, lebar = np.arange(len(metrik)), 0.35
    fig, ax = plt.subplots(figsize=(10, 6))
    bar1 = ax.bar(x - lebar/2, skor_svm, lebar, label="SVM",         color="#2196F3", edgecolor="white")
    bar2 = ax.bar(x + lebar/2, skor_nb,  lebar, label="Naive Bayes", color="#FF9800", edgecolor="white")
    ax.set_ylabel("Skor", fontsize=12)
    ax.set_title("Perbandingan Performa Model", fontsize=14, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(metrik, fontsize=11)
    ax.set_ylim(0, 1.15); ax.legend(fontsize=11); ax.grid(axis="y", alpha=0.3)
    for bar in [*bar1, *bar2]:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
                f"{bar.get_height():.3f}", ha="center", fontsize=10, fontweight="bold")
    plt.tight_layout()
    filepath = FIGURES_DIR / "perbandingan_model.png"
    fig.savefig(filepath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    log.info(f"  Grafik perbandingan disimpan: {filepath.name}")


# =======================================================================
#  STEP 9 -- Simpan Artefak
# =======================================================================
def simpan_model(model, tfidf, nama_file_model: str):
    model_path = MODELS_DIR / nama_file_model
    tfidf_path = MODELS_DIR / "tfidf_vectorizer.pkl"
    joblib.dump(model, model_path)
    joblib.dump(tfidf, tfidf_path)
    log.info(f"  Model disimpan     : {model_path.name}")
    log.info(f"  Vectorizer disimpan: {tfidf_path.name}")


def simpan_laporan_evaluasi(hasil_svm: dict, hasil_nb: dict, pemenang: str,
                             cv_nb: dict = None, cv_svm: dict = None):
    """Menyimpan laporan evaluasi -- train-test split + cross-validation."""
    filepath = REPORTS_DIR / "ml_evaluation_report.txt"
    garis = "=" * 65

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"{garis}\n")
        f.write("  LAPORAN EVALUASI MODEL MACHINE LEARNING\n")
        f.write("  Klasifikasi Sentimen Ulasan Parfum Lokal\n")
        f.write(f"  Muhammad Iqbal Fadel | 202310370311268\n")
        f.write(f"{garis}\n\n")

        f.write("CATATAN METODOLOGI:\n")
        f.write("  TF-IDF di-fit hanya pada data latih untuk mencegah data leakage.\n")
        f.write("  Evaluasi menggunakan (1) train-test split 80/20 stratified dan\n")
        f.write("  (2) 5-Fold Stratified Cross Validation via sklearn Pipeline.\n\n")
        f.write(f"{garis}\n\n")

        f.write("BAGIAN A -- EVALUASI TRAIN-TEST SPLIT (80/20)\n\n")
        for hasil in [hasil_svm, hasil_nb]:
            f.write(f"--- {hasil['nama']} ---\n")
            f.write(f"Akurasi           : {hasil['akurasi']:.4f} ({hasil['akurasi']*100:.2f}%)\n")
            f.write(f"F1-Score (Macro)   : {hasil['f1_macro']:.4f}\n")
            f.write(f"F1-Score (Weighted): {hasil['f1_weighted']:.4f}\n\n")
            f.write("Classification Report:\n")
            f.write(hasil["report"])
            f.write("\n\n")

        if cv_nb or cv_svm:
            f.write(f"{garis}\n\n")
            f.write("BAGIAN B -- 5-FOLD CROSS VALIDATION\n")
            f.write("(sklearn Pipeline -- TF-IDF di-fit per fold)\n\n")
            for cv in [cv_svm, cv_nb]:
                if cv is None:
                    continue
                f.write(f"--- {cv['nama']} ({cv['cv']}-Fold CV) ---\n")
                f.write(f"Akurasi     : {cv['acc_mean']:.4f} +- {cv['acc_std']:.4f}\n")
                f.write(f"F1-Macro    : {cv['f1_macro_mean']:.4f} +- {cv['f1_macro_std']:.4f}\n")
                f.write(f"F1-Weighted : {cv['f1_weighted_mean']:.4f} +- {cv['f1_weighted_std']:.4f}\n\n")

        f.write(f"{garis}\n")
        f.write(f"  KESIMPULAN: Model terbaik adalah {pemenang}\n")
        f.write(f"{garis}\n")

    log.info(f"  Laporan evaluasi disimpan: {filepath.name}")


# =======================================================================
#  MAIN -- Orkestrasi Pipeline
# =======================================================================
def main():
    log.info("")
    log.info("=" * 60)
    log.info("  PIPELINE MACHINE LEARNING - KLASIFIKASI SENTIMEN")
    log.info("  Muhammad Iqbal Fadel | 202310370311268")
    log.info("=" * 60)
    log.info("")

    # 1. Muat data
    df = muat_data()

    # 2. Split teks TERLEBIH DAHULU (sebelum TF-IDF)
    X_train_raw, X_test_raw, y_train, y_test = bagi_data(
        df[COL_TEXT_NORM], df[COL_LABEL]
    )

    # 3. Ekstraksi fitur TF-IDF -- fit HANYA pada data latih
    X_train, X_test, tfidf = ekstraksi_fitur(X_train_raw, X_test_raw)

    # 4. SMOTE pada data latih (untuk Naive Bayes)
    X_train_smote, y_train_smote = terapkan_smote(X_train, y_train)

    # 5. Latih model
    model_svm = latih_svm(X_train, y_train)
    model_nb  = latih_naive_bayes(X_train_smote, y_train_smote)

    # 6. Evaluasi train-test split
    hasil_svm = evaluasi_model(model_svm, X_test, y_test, "SVM")
    hasil_nb  = evaluasi_model(model_nb,  X_test, y_test, "Naive Bayes")

    # 7. Tentukan model terbaik (F1-Weighted)
    if hasil_svm["f1_weighted"] >= hasil_nb["f1_weighted"]:
        pemenang, model_terbaik = "SVM", model_svm
    else:
        pemenang, model_terbaik = "Naive Bayes", model_nb
    log.info(f"\n  Model terbaik: {pemenang}\n")

    # 8. 5-Fold Cross Validation
    log.info("")
    log.info("=" * 60)
    log.info("  5-FOLD CROSS VALIDATION")
    log.info("=" * 60)
    cv_nb  = cross_validate_model(df, "Naive Bayes", cv=5)
    cv_svm = cross_validate_model(df, "SVM",         cv=5)

    # 9. Visualisasi
    labels = sorted(df[COL_LABEL].unique())
    simpan_confusion_matrix(y_test, hasil_svm["y_pred"], "SVM",         labels)
    simpan_confusion_matrix(y_test, hasil_nb["y_pred"],  "Naive Bayes", labels)
    simpan_perbandingan_model(hasil_svm, hasil_nb)

    # 10. Simpan model & laporan
    nama_file = f"model_terbaik_{pemenang.lower().replace(' ', '_')}.pkl"
    simpan_model(model_terbaik, tfidf, nama_file)
    simpan_laporan_evaluasi(hasil_svm, hasil_nb, pemenang, cv_nb, cv_svm)

    log.info("")
    log.info("=" * 60)
    log.info("  PIPELINE ML SELESAI")
    log.info("=" * 60)
    log.info(f"  Model terbaik    : {pemenang}")
    log.info(f"  Akurasi (split)  : {max(hasil_svm['akurasi'], hasil_nb['akurasi'])*100:.2f}%")
    log.info(f"  Akurasi CV (NB)  : {cv_nb['acc_mean']*100:.2f}% +- {cv_nb['acc_std']*100:.2f}%")
    log.info(f"  Output:")
    log.info(f"    results/figures/  -- confusion matrix, perbandingan")
    log.info(f"    results/models/   -- model .pkl, vectorizer .pkl")
    log.info(f"    results/reports/  -- ml_evaluation_report.txt")
    log.info("=" * 60)


if __name__ == "__main__":
    main()
