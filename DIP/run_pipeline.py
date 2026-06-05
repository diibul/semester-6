"""
run_pipeline.py
================
Master script untuk menjalankan SELURUH pipeline dari awal hingga akhir.
Cukup jalankan: python run_pipeline.py

Urutan: Profiling → Cleaning → Normalisasi → Labeling → Validasi
"""

import sys
import time
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger("Pipeline")

STEPS = [
    ("02_data_profiling",       "profiling",     "Data Profiling"),
    ("03_basic_cleaning",       "basic_cleaning","Basic Cleaning"),
    ("04_advanced_normalization","normalization", "Advanced Normalization"),
    ("05_labeling",             "labeling",      "Labeling Sentimen"),
    ("06_validation",           "validation",    "Validasi & Laporan"),
]


def jalankan_step(folder: str, modul: str, nama: str) -> bool:
    """Jalankan satu langkah pipeline."""
    import importlib.util, traceback
    script_path = ROOT_DIR / "scripts" / folder / f"{modul}.py"
    log.info(f"\n{'='*60}")
    log.info(f"  STEP: {nama}")
    log.info(f"{'='*60}")
    try:
        spec = importlib.util.spec_from_file_location(modul, script_path)
        mod  = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
        return True
    except Exception as e:
        log.error(f"❌ Error pada {nama}: {e}")
        traceback.print_exc()
        return False


def main():
    log.info("\n" + "█"*60)
    log.info("  PIPELINE PREPROCESSING — ULASAN PARFUM LOKAL")
    log.info("  Muhammad Iqbal Fadel | 202310370311268")
    log.info("█"*60 + "\n")

    mulai = time.time()
    hasil = {}

    for folder, modul, nama in STEPS:
        t0 = time.time()
        ok = jalankan_step(folder, modul, nama)
        durasi = round(time.time() - t0, 1)
        hasil[nama] = ("✅ Berhasil" if ok else "❌ Gagal", durasi)

    # Ringkasan akhir
    total = round(time.time() - mulai, 1)
    log.info("\n" + "="*60)
    log.info("  RINGKASAN PIPELINE")
    log.info("="*60)
    for nama, (status, dur) in hasil.items():
        log.info(f"  {status}  {nama:<35} ({dur}s)")
    log.info(f"\n  Total waktu: {total}s")
    log.info("="*60)


if __name__ == "__main__":
    main()
