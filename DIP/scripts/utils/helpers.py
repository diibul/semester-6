# =====================================================
# scripts/utils/helpers.py
# Utility: Fungsi-fungsi helper yang dipakai seluruh pipeline
# =====================================================

import json
import pandas as pd
from pathlib import Path
from typing import Union
from scripts.utils.logger import get_logger

log = get_logger(__name__)


# ─── I/O Helpers ──────────────────────────────────────────────────────────────

def load_csv(filepath: Union[str, Path], encoding: str = "utf-8") -> pd.DataFrame:
    """Load CSV dengan logging otomatis."""
    filepath = Path(filepath)
    log.info(f"Loading: {filepath.name} ({filepath.stat().st_size / 1024:.1f} KB)")
    df = pd.read_csv(filepath, encoding=encoding)
    log.info(f"  → {len(df):,} baris | {len(df.columns)} kolom")
    return df


def save_csv(df: pd.DataFrame, filepath: Union[str, Path], index: bool = False) -> None:
    """Simpan DataFrame ke CSV dengan logging."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=index, encoding="utf-8-sig")
    log.info(f"Saved: {filepath.name} ({len(df):,} baris)")


def load_json(filepath: Union[str, Path]) -> dict:
    """Load file JSON."""
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    log.info(f"Loaded JSON: {Path(filepath).name} ({len(data)} entri)")
    return data


def save_json(data: dict, filepath: Union[str, Path], indent: int = 2) -> None:
    """Simpan dict ke file JSON."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    log.info(f"Saved JSON: {filepath.name} ({len(data)} entri)")


# ─── DataFrame Helpers ────────────────────────────────────────────────────────

def print_df_info(df: pd.DataFrame, title: str = "DataFrame Info") -> None:
    """Cetak ringkasan DataFrame ke console."""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")
    print(f"  Shape     : {df.shape}")
    print(f"  Kolom     : {list(df.columns)}")
    print(f"  Duplikat  : {df.duplicated().sum():,}")
    print(f"  Null Total: {df.isnull().sum().sum():,}")
    print(f"{'='*50}\n")


def get_missing_report(df: pd.DataFrame) -> pd.DataFrame:
    """Buat laporan missing values per kolom."""
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    return pd.DataFrame({
        "missing_count": missing,
        "missing_pct": pct
    }).query("missing_count > 0").sort_values("missing_pct", ascending=False)
