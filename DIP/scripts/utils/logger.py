# =====================================================
# scripts/utils/logger.py
# Utility: Centralized Logger untuk semua skrip pipeline
# =====================================================

import logging
import sys
from pathlib import Path
from datetime import datetime

# Root project dir (2 level up dari utils/)
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
LOGS_DIR = ROOT_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str, log_to_file: bool = True) -> logging.Logger:
    """
    Buat logger dengan format profesional.
    
    Args:
        name: Nama modul/skrip yang memanggil logger
        log_to_file: Jika True, simpan log ke file di /logs/
    
    Returns:
        logging.Logger: Logger yang sudah dikonfigurasi
    
    Example:
        >>> from scripts.utils.logger import get_logger
        >>> log = get_logger(__name__)
        >>> log.info("Memulai proses cleaning...")
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Hindari duplicate handler
    if logger.handlers:
        return logger

    fmt = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ── Handler: Console ──────────────────────────
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(fmt)
    logger.addHandler(console_handler)

    # ── Handler: File ─────────────────────────────
    if log_to_file:
        log_filename = LOGS_DIR / f"{datetime.now().strftime('%Y%m%d')}_{name.split('.')[-1]}.log"
        file_handler = logging.FileHandler(log_filename, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(fmt)
        logger.addHandler(file_handler)

    return logger
