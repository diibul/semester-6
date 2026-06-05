"""
scripts/05_labeling/labeling.py
=================================
Minggu 9-10: Domain-Specific Labeling
Label sentimen berbasis keyword: Positif / Negatif / Netral

Input  : data/processed/ulasan_parfum_processed.csv
Output : data/processed/ulasan_parfum_processed.csv (+ kolom label)
"""

import sys
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

PROCESSED_DIR = ROOT_DIR / "data" / "processed"
FIGURES_DIR   = ROOT_DIR / "results" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("Labeling")

# Keywords sentimen domain parfum
KEYWORDS_POS = [
    "bagus", "wangi", "suka", "rekomen", "tahan lama", "long lasting",
    "enak", "mantap", "oke", "cocok", "puas", "keren", "seger", "fresh",
    "harum", "worth it", "worth", "top", "love", "best", "hits",
    "recommended", "good", "great", "nice", "excellent", "friendly",
    "helpful", "beautiful", "amazing", "awesome", "delicious", "happy",
    "favorite", "perfect", "comfortable", "satisfied", "cool", "fragrant",
    "durable", "affordable", "complete", "polite", "informative", "unique",
    "premium", "elegant", "superb", "fantastic", "wonderful", "impressive"
]

KEYWORDS_NEG = [
    "jelek", "bau", "tidak suka", "kecewa", "mahal", "ga worth",
    "gak worth", "luntur", "cepat hilang", "buruk", "mengecewakan",
    "rugi", "bohong", "palsu", "fake", "bad", "worst", "awful", "payah",
    "disappointed", "rude", "expensive", "overpriced", "poor", "terrible",
    "horrible", "broken", "not worth", "short", "disappear", "faded",
    "not polite", "bitchy", "not durable", "not lasting", "not good",
    "not friendly", "complaint", "regret"
]


def labeling_keyword(teks: str) -> str:
    teks_lower = str(teks).lower()
    skor_pos = sum(1 for k in KEYWORDS_POS if k in teks_lower)
    skor_neg = sum(1 for k in KEYWORDS_NEG if k in teks_lower)
    if skor_pos > skor_neg:
        return "Positif"
    elif skor_neg > skor_pos:
        return "Negatif"
    return "Netral"


def plot_distribusi(df: pd.DataFrame, simpan_ke: Path) -> None:
    counts = df["label"].value_counts()
    colors = {"Positif": "#4CAF50", "Negatif": "#F44336", "Netral": "#FF9800"}
    clrs = [colors.get(l, "#888") for l in counts.index]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Distribusi Label Sentimen - Ulasan Parfum Lokal",
                 fontsize=14, fontweight="bold")

    ax1.pie(counts.values, labels=counts.index, colors=clrs,
            autopct="%1.1f%%", startangle=90, textprops={"fontsize": 12})
    ax1.set_title("Proporsi Label")

    bars = ax2.bar(counts.index, counts.values, color=clrs,
                   edgecolor="white", linewidth=1.5)
    ax2.set_xlabel("Label Sentimen")
    ax2.set_ylabel("Jumlah Ulasan")
    ax2.set_title("Jumlah per Label")
    ax2.bar_label(bars, fmt="%d", padding=3)
    ax2.grid(axis="y", alpha=0.3)
    ax2.spines[["top", "right"]].set_visible(False)

    plt.tight_layout()
    plt.savefig(simpan_ke, dpi=150, bbox_inches="tight")
    plt.close()
    log.info(f"Grafik disimpan: {simpan_ke.name}")


def main():
    log.info("=" * 60)
    log.info("  LABELING — Minggu 9-10")
    log.info("=" * 60)

    data_path = PROCESSED_DIR / "ulasan_parfum_processed.csv"
    if not data_path.exists():
        log.error("Jalankan normalization.py terlebih dahulu!"); return

    df = pd.read_csv(data_path, encoding="utf-8")
    log.info(f"Data dimuat: {len(df):,} baris")

    norm_col = "text_normalized" if "text_normalized" in df.columns else "text_clean"
    log.info("Menerapkan keyword-based labeling...")
    df["label"] = df[norm_col].apply(labeling_keyword)

    dist = df["label"].value_counts()
    log.info("\nDistribusi Label:")
    for label, count in dist.items():
        log.info(f"  {label:<10}: {count:>5,} ({count/len(df)*100:.1f}%)")

    df.to_csv(data_path, index=False, encoding="utf-8-sig")
    log.info(f"Tersimpan: {data_path}")

    plot_distribusi(df, FIGURES_DIR / "distribusi_label.png")
    log.info("Labeling (Minggu 9-10) selesai!")
    return df


if __name__ == "__main__":
    main()
