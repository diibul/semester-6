"""
scripts/04_advanced_normalization/normalization.py
====================================================
Minggu 7-8: Advanced Normalization (Tahap Krusial)
Fungsi Slang-to-Formal menggunakan Slang Dictionary.

Proses:
  1. Load flat slang dictionary (gabung semua kategori)
  2. Tokenisasi teks
  3. Lookup setiap token ke slang dictionary
  4. Ganti slang -> kata formal
  5. Normalisasi huruf berulang sisa

Input  : data/interim/ulasan_parfum_interim.csv
Output : data/processed/ulasan_parfum_processed.csv
"""

import sys
import re
import json
from pathlib import Path

import pandas as pd
from tqdm import tqdm

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

INTERIM_DIR  = ROOT_DIR / "data" / "interim"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
DICT_DIR     = ROOT_DIR / "dictionary"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("Normalization")


# ==============================================================================
# LOAD DICTIONARY
# ==============================================================================

def load_slang_dict(dict_path: Path) -> dict:
    """
    Load kamus slang dari file JSON.
    JSON kita berstruktur nested (per kategori), jadi perlu di-flatten.
    Format final: {"kata_gaul": "kata_formal", ...}
    """
    if not dict_path.exists():
        log.warning(f"Kamus tidak ditemukan: {dict_path}")
        return {}

    with open(dict_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    # Flatten: gabungkan semua kategori jadi 1 dict datar
    flat = {}
    for key, value in raw.items():
        if key.startswith("_"):
            continue  # skip _metadata
        if isinstance(value, dict):
            for slang, formal in value.items():
                flat[slang.lower()] = formal
        elif isinstance(value, str):
            flat[key.lower()] = value

    log.info(f"Kamus dimuat: {len(flat):,} entri dari {dict_path.name}")
    return flat


# ==============================================================================
# FUNGSI NORMALISASI
# ==============================================================================

def normalisasi_huruf_berulang(teks: str) -> str:
    """Normalisasi huruf diulang >2x ke 1 huruf. 'wangiiii' -> 'wangi'"""
    return re.sub(r'(.)\1{2,}', r'\1', teks)


def slang_to_formal(teks: str, kamus: dict) -> str:
    """
    Ganti setiap kata slang dengan padanan formalnya.
    Proses word-by-word lookup O(1).

    Example:
        >>> slang_to_formal("aq suka bgt parfum ini", kamus)
        'saya suka sangat parfum ini'
    """
    tokens = teks.split()
    hasil = []
    for token in tokens:
        formal = kamus.get(token, token)
        if formal:  # skip jika nilai kosong "" (noise filler)
            hasil.append(formal)
    return " ".join(hasil)


def normalisasi_penuh(teks: str, kamus: dict) -> str:
    """Pipeline normalisasi lengkap."""
    teks = normalisasi_huruf_berulang(teks)
    teks = slang_to_formal(teks, kamus)
    teks = re.sub(r'\s+', ' ', teks).strip()
    return teks


def hitung_coverage(df: pd.DataFrame, kamus: dict, col: str) -> dict:
    """Hitung berapa persen token dalam dataset yang ada di kamus."""
    semua = []
    for t in df[col].dropna():
        semua.extend(str(t).split())
    total = len(semua)
    di_kamus = sum(1 for k in semua if k in kamus)
    return {
        "total_token"    : total,
        "token_di_kamus" : di_kamus,
        "coverage_pct"   : round(di_kamus / total * 100, 2) if total else 0
    }


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    log.info("=" * 60)
    log.info("  ADVANCED NORMALIZATION — Minggu 7-8 (UTS)")
    log.info("=" * 60)

    # ── Load kamus ────────────────────────────────────────────────
    dict_path = DICT_DIR / "slang_dictionary_parfum.json"
    kamus = load_slang_dict(dict_path)
    if not kamus:
        log.error("Kamus kosong! Buat dictionary terlebih dahulu."); return

    # ── Load data interim ─────────────────────────────────────────
    interim_path = INTERIM_DIR / "ulasan_parfum_interim.csv"
    if not interim_path.exists():
        candidates = list(INTERIM_DIR.glob("*.csv"))
        if not candidates:
            log.error("Jalankan basic_cleaning.py terlebih dahulu!"); return
        interim_path = candidates[0]

    df = pd.read_csv(interim_path, encoding="utf-8")
    log.info(f"Data dimuat: {len(df):,} baris")

    # Deteksi kolom clean
    clean_col = "text_clean"
    if clean_col not in df.columns:
        candidates = [c for c in df.columns if "clean" in c.lower()]
        clean_col = candidates[0] if candidates else df.columns[-1]
        log.warning(f"Menggunakan kolom: '{clean_col}'")

    # ── Coverage sebelum ──────────────────────────────────────────
    cov_before = hitung_coverage(df, kamus, clean_col)
    log.info(f"Coverage SEBELUM: {cov_before['coverage_pct']}% "
             f"({cov_before['token_di_kamus']:,}/{cov_before['total_token']:,})")

    # ── Normalisasi ───────────────────────────────────────────────
    log.info("Menerapkan slang-to-formal normalization...")
    tqdm.pandas(desc="  Normalisasi")
    df["text_normalized"] = df[clean_col].progress_apply(
        lambda x: normalisasi_penuh(str(x), kamus)
    )

    # ── Coverage sesudah ──────────────────────────────────────────
    cov_after = hitung_coverage(df, kamus, "text_normalized")

    # ── Simpan ────────────────────────────────────────────────────
    out_path = PROCESSED_DIR / "ulasan_parfum_processed.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    log.info(f"Tersimpan: {out_path}")

    # ── Demo perbandingan (untuk UTS) ─────────────────────────────
    log.info("\n" + "=" * 60)
    log.info("  DEMO UTS: DATA MENTAH vs DATA BERSIH (5 Sampel)")
    log.info("=" * 60)

    raw_col = "REVIEW" if "REVIEW" in df.columns else df.columns[0]
    for i, (_, row) in enumerate(df.head(5).iterrows(), 1):
        raw  = str(row.get(raw_col, ""))[:85]
        cln  = str(row.get(clean_col, ""))[:85]
        nrm  = str(row.get("text_normalized", ""))[:85]
        print(f"\n  [{i}] RAW   : {raw}")
        print(f"      CLEAN : {cln}")
        print(f"      NORMAL: {nrm}")

    # ── Statistik akhir ───────────────────────────────────────────
    log.info(f"\n{'─'*50}")
    log.info(f"  Total baris      : {len(df):,}")
    log.info(f"  Kamus entri      : {len(kamus):,}")
    log.info(f"  Coverage sebelum : {cov_before['coverage_pct']}%")
    log.info(f"  Coverage sesudah : {cov_after['coverage_pct']}%")
    log.info(f"{'─'*50}")
    log.info("Advanced Normalization (Minggu 7-8) selesai!")


if __name__ == "__main__":
    main()
