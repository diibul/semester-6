"""
scripts/03_basic_cleaning/basic_cleaning.py
============================================
Minggu 5-6: Basic Cleaning Pipeline
Membersihkan teks ulasan parfum dari noise dasar.

Proses:
  1. Load CSV semicolon-delimited, buang baris noise struktural
  2. Case folding (lowercase)
  3. Hapus URL
  4. Hapus karakter khusus & tanda baca
  5. Hapus angka
  6. Normalisasi huruf berulang (waangi → wangi)
  7. Normalisasi spasi berlebih
  8. Filter teks terlalu pendek (<10 char) atau kosong
  9. Hapus duplikat

Input  : data/raw/ulasan_parfum_raw.csv
Output : data/interim/ulasan_parfum_interim.csv
"""

import sys
import re
from pathlib import Path

import pandas as pd
from tqdm import tqdm

# Force UTF-8 di Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

RAW_DIR     = ROOT_DIR / "data" / "raw"
INTERIM_DIR = ROOT_DIR / "data" / "interim"
INTERIM_DIR.mkdir(parents=True, exist_ok=True)

import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("BasicCleaning")

MIN_LEN = 10   # minimum panjang teks setelah cleaning
MAX_LEN = 500  # maximum panjang teks

# ==============================================================================
# LOAD & FILTER NOISE STRUKTURAL (sama seperti profiling)
# ==============================================================================

def load_dataset(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, sep=";", encoding="utf-8",
                     on_bad_lines="skip", engine="python")
    if "REVIEW" not in df.columns and len(df.columns) >= 3:
        df.columns = ["USERNAME", "TIME", "REVIEW"] + list(df.columns[3:])

    def is_noise_row(row) -> bool:
        rev = str(row.get("REVIEW", "") or "")
        usr = str(row.get("USERNAME", "") or "")
        if not rev.strip():
            return True
        for prefix in ("î", "ã", "Translated", "See original", "Like", "Share"):
            if rev.startswith(prefix) or usr.startswith("î"):
                return True
        return False

    mask = ~df.apply(is_noise_row, axis=1)
    df_valid = df[mask].copy().reset_index(drop=True)
    log.info(f"Dimuat: {len(df):,} baris raw -> {len(df_valid):,} valid")
    return df_valid


# ==============================================================================
# FUNGSI CLEANING (masing-masing bisa dipakai sendiri)
# ==============================================================================

def case_folding(teks: str) -> str:
    """Ubah semua huruf menjadi huruf kecil."""
    return str(teks).lower().strip()


def hapus_url(teks: str) -> str:
    """Hapus URL (http, https, www)."""
    return re.sub(r'https?://\S+|www\.\S+', ' ', teks)


def hapus_hashtag(teks: str) -> str:
    """Pertahankan kata setelah # (hapus simbol #)."""
    return re.sub(r'#(\w+)', r'\1', teks)


def hapus_mention(teks: str) -> str:
    """Hapus @username sepenuhnya."""
    return re.sub(r'@\w+', ' ', teks)


def hapus_karakter_khusus(teks: str) -> str:
    """Hapus tanda baca, simbol, dan karakter non-alfanumerik."""
    teks = re.sub(r'[^\w\s]', ' ', teks)   # hapus tanda baca
    teks = re.sub(r'_', ' ', teks)          # hapus underscore
    return teks


def hapus_angka(teks: str) -> str:
    """Hapus angka dalam teks."""
    return re.sub(r'\d+', ' ', teks)


def hapus_huruf_berulang(teks: str) -> str:
    """
    Normalisasi huruf yang diulang >2x.
    Contoh: 'waaangiiii' -> 'waangii'
    (2 huruf dipertahankan supaya masih "terasa" pengulangan)
    """
    return re.sub(r'(.)\1{2,}', r'\1\1', teks)


def normalisasi_spasi(teks: str) -> str:
    """Hapus spasi berlebih."""
    return re.sub(r'\s+', ' ', teks).strip()


def basic_clean(teks: str) -> str:
    """
    Pipeline basic cleaning lengkap.

    Example:
        >>> basic_clean("Waaanginya bgt!! check @parfumlokal https://toko.com 😍")
        'waanginya bgt check'
    """
    teks = case_folding(teks)
    teks = hapus_url(teks)
    teks = hapus_hashtag(teks)
    teks = hapus_mention(teks)
    teks = hapus_karakter_khusus(teks)
    teks = hapus_angka(teks)
    teks = hapus_huruf_berulang(teks)
    teks = normalisasi_spasi(teks)
    return teks


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    log.info("=" * 60)
    log.info("  BASIC CLEANING — Ulasan Parfum Lokal (Minggu 5-6)")
    log.info("=" * 60)

    # ── Load ──────────────────────────────────────────────────────
    raw_path = RAW_DIR / "ulasan_parfum_raw.csv"
    if not raw_path.exists():
        candidates = list(RAW_DIR.glob("*.csv"))
        if not candidates:
            log.error("Tidak ada CSV di data/raw/"); return
        raw_path = candidates[0]

    df = load_dataset(raw_path)
    n_awal = len(df)

    # ── Cleaning ──────────────────────────────────────────────────
    log.info("Menerapkan basic cleaning pipeline...")
    tqdm.pandas(desc="  Cleaning")
    df["text_clean"] = df["REVIEW"].progress_apply(basic_clean)

    # ── Filter panjang ────────────────────────────────────────────
    mask_len = df["text_clean"].str.len().between(MIN_LEN, MAX_LEN)
    n_hapus_len = (~mask_len).sum()
    df = df[mask_len].copy()
    log.info(f"Difilter (panjang): -{n_hapus_len:,} baris")

    # ── Hapus baris kosong setelah cleaning ───────────────────────
    mask_kosong = df["text_clean"].str.strip() != ""
    n_hapus_kosong = (~mask_kosong).sum()
    df = df[mask_kosong].copy()
    log.info(f"Difilter (kosong setelah clean): -{n_hapus_kosong:,} baris")

    # ── Hapus duplikat ────────────────────────────────────────────
    n_sebelum = len(df)
    df = df.drop_duplicates(subset=["text_clean"]).reset_index(drop=True)
    n_hapus_dup = n_sebelum - len(df)
    log.info(f"Duplikat dihapus: -{n_hapus_dup:,} baris")

    # ── Statistik ─────────────────────────────────────────────────
    n_akhir = len(df)
    log.info(f"\n{'─'*45}")
    log.info(f"  Awal    : {n_awal:>6,} baris")
    log.info(f"  Dihapus : {n_awal - n_akhir:>6,} baris")
    log.info(f"  Akhir   : {n_akhir:>6,} baris  ({n_akhir/n_awal*100:.1f}% tersisa)")
    log.info(f"  Rata-rata panjang : {df['text_clean'].str.len().mean():.1f} char")
    log.info(f"  Rata-rata kata    : {df['text_clean'].str.split().str.len().mean():.1f} kata")
    log.info(f"{'─'*45}")

    # ── Simpan ────────────────────────────────────────────────────
    out_path = INTERIM_DIR / "ulasan_parfum_interim.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    log.info(f"Tersimpan: {out_path}")

    # ── Demo perbandingan ─────────────────────────────────────────
    log.info("\n--- Contoh Hasil Cleaning (5 baris) ---")
    sample = df[["REVIEW", "text_clean"]].head(5)
    for i, (_, row) in enumerate(sample.iterrows(), 1):
        raw_txt = str(row["REVIEW"])[:80]
        cln_txt = str(row["text_clean"])[:80]
        print(f"\n  [{i}] SEBELUM: {raw_txt}")
        print(f"      SESUDAH: {cln_txt}")

    log.info("\nBasic Cleaning (Minggu 5-6) selesai!")
    return df


if __name__ == "__main__":
    main()
