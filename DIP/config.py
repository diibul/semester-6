# =====================================================
# config.py
# Konfigurasi global untuk seluruh pipeline
# =====================================================

import os
from pathlib import Path

# ─── Root Directory ────────────────────────────────
ROOT_DIR = Path(__file__).parent.resolve()

# ─── Direktori Data ────────────────────────────────
DATA_DIR        = ROOT_DIR / "data"
RAW_DIR         = DATA_DIR / "raw"
INTERIM_DIR     = DATA_DIR / "interim"
PROCESSED_DIR   = DATA_DIR / "processed"


# ─── Direktori Skrip ───────────────────────────────
SCRIPTS_DIR     = ROOT_DIR / "scripts"

# ─── Direktori Output ──────────────────────────────
DICT_DIR        = ROOT_DIR / "dictionary"
RESULTS_DIR     = ROOT_DIR / "results"
FIGURES_DIR     = RESULTS_DIR / "figures"
REPORTS_DIR     = RESULTS_DIR / "reports"
MODELS_DIR      = RESULTS_DIR / "models"
LOGS_DIR        = ROOT_DIR / "logs"

# ─── Nama File Utama ───────────────────────────────
RAW_FILENAME        = "ulasan_parfum_raw.csv"
INTERIM_FILENAME    = "ulasan_parfum_interim.csv"
PROCESSED_FILENAME  = "ulasan_parfum_processed.csv"
SLANG_DICT_FILENAME = "slang_dictionary_parfum.json"
FORMAL_DICT_FILE    = DICT_DIR / SLANG_DICT_FILENAME

# ─── Format CSV ─────────────────────────────────────────────────
CSV_SEPARATOR   = ";"              # Delimiter dataset: semicolon

# ─── Kolom Dataset (sesuai file asli) ───────────────────────────
COL_USERNAME    = "USERNAME"        # Nama reviewer
COL_TIME        = "TIME"            # Waktu ulasan
COL_TEXT_RAW    = "REVIEW"          # Teks ulasan mentah (kolom asli)
COL_TEXT_CLEAN  = "text_clean"      # Teks setelah basic cleaning
COL_TEXT_NORM   = "text_normalized" # Teks setelah normalisasi
COL_LABEL       = "label"           # Positif / Negatif / Netral
COL_SOURCE      = "source"          # Sumber data
COL_ID          = "id"
COL_RATING      = "rating"
COL_DATE        = "date"
COL_PRODUCT     = "product_name"

# ─── Label Sentimen ────────────────────────────────
LABEL_POSITIF   = "Positif"
LABEL_NEGATIF   = "Negatif"
LABEL_NETRAL    = "Netral"

# ─── Keyword Labeling (Minggu 9-10) ────────────────
KEYWORDS_POSITIF = [
    "bagus", "wangi", "suka", "rekomen", "tahan lama",
    "enak", "mantap", "oke", "cocok", "puas", "keren",
    "seger", "fresh", "harum", "worth it", "worth", "top",
    "love", "best", "hits", "recommended", "good"
]

KEYWORDS_NEGATIF = [
    "jelek", "bau", "tidak suka", "kecewa", "mahal",
    "ga worth", "gak worth", "tidak worth", "luntur",
    "tidak tahan", "ga enak", "gak enak", "buruk",
    "mengecewakan", "salah", "rugi", "bohong", "palsu",
    "fake", "bad", "worst", "awful", "payah"
]

# ─── Parameter Cleaning ────────────────────────────
MIN_TEXT_LENGTH = 10    # Hapus teks < 10 karakter
MAX_TEXT_LENGTH = 500   # Hapus teks > 500 karakter

# ─── Logging ───────────────────────────────────────
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"

# ─── Buat direktori jika belum ada ─────────────────
for _dir in [RAW_DIR, INTERIM_DIR, PROCESSED_DIR,
             DICT_DIR, FIGURES_DIR, REPORTS_DIR, MODELS_DIR, LOGS_DIR]:
    _dir.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    print("=== Konfigurasi Proyek ===")
    print(f"Root     : {ROOT_DIR}")
    print(f"Data Raw : {RAW_DIR}")
    print(f"Processed: {PROCESSED_DIR}")
    print(f"Dict     : {DICT_DIR}")
    print(f"Results  : {RESULTS_DIR}")
