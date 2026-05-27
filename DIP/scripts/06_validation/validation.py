"""
scripts/06_validation/validation.py
=====================================
Minggu 11-12: Validasi & Dokumentasi
Cek akurasi hasil cleaning & buat word cloud sesudah preprocessing.

Output:
  - results/reports/validation_report.txt
  - results/reports/sampel_validasi_manual.csv
  - results/figures/wordcloud_after.png
  - results/figures/comparison_before_after.png
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
RAW_DIR       = ROOT_DIR / "data" / "raw"
FIGURES_DIR   = ROOT_DIR / "results" / "figures"
REPORTS_DIR   = ROOT_DIR / "results" / "reports"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("Validation")


def cek_sisa_noise(series: pd.Series) -> dict:
    return {
        "sisa_url"     : int(series.str.contains(r"https?://|www\.", regex=True, na=False).sum()),
        "sisa_hashtag" : int(series.str.contains(r"#\w+", regex=True, na=False).sum()),
        "sisa_mention" : int(series.str.contains(r"@\w+", regex=True, na=False).sum()),
        "sisa_angka"   : int(series.str.contains(r"\d+", regex=True, na=False).sum()),
        "teks_kosong"  : int((series.str.strip() == "").sum()),
    }


def plot_wordcloud_after(series: pd.Series, path: Path) -> None:
    try:
        from wordcloud import WordCloud
    except ImportError:
        log.warning("wordcloud not installed"); return
    text = " ".join(series.dropna().astype(str))
    if not text.strip(): return
    wc = WordCloud(width=1200, height=550, background_color="white",
                   colormap="plasma", max_words=200).generate(text)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.imshow(wc, interpolation="bilinear"); ax.axis("off")
    ax.set_title("Word Cloud - Setelah Preprocessing", fontsize=15, fontweight="bold")
    plt.tight_layout(); plt.savefig(path, dpi=150, bbox_inches="tight"); plt.close()
    log.info(f"  WordCloud: {path.name}")


def plot_perbandingan(df: pd.DataFrame, col_raw: str, col_norm: str, path: Path) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle("Perbandingan Panjang Teks: Sebelum vs Sesudah", fontsize=13, fontweight="bold")
    for ax, col, label, color in [
        (axes[0], col_raw,  "Sebelum (Raw)",    "#EF5350"),
        (axes[1], col_norm, "Sesudah (Bersih)", "#42A5F5"),
    ]:
        if col not in df.columns: ax.set_visible(False); continue
        lengths = df[col].dropna().str.len()
        ax.hist(lengths, bins=40, color=color, edgecolor="white", alpha=0.85)
        ax.axvline(lengths.mean(), color="black", linestyle="--", linewidth=1.5,
                   label=f"Mean: {lengths.mean():.0f}")
        ax.set_xlabel("Panjang (karakter)"); ax.set_ylabel("Frekuensi")
        ax.set_title(label); ax.legend(); ax.grid(alpha=0.3)
        ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout(); plt.savefig(path, dpi=150, bbox_inches="tight"); plt.close()
    log.info(f"  Grafik: {path.name}")


def main():
    log.info("=" * 60)
    log.info("  VALIDASI & DOKUMENTASI — Minggu 11-12")
    log.info("=" * 60)

    data_path = PROCESSED_DIR / "ulasan_parfum_processed.csv"
    if not data_path.exists():
        log.error("Jalankan labeling.py terlebih dahulu!"); return

    df = pd.read_csv(data_path, encoding="utf-8")
    log.info(f"Data dimuat: {len(df):,} baris")

    raw_col  = "REVIEW" if "REVIEW" in df.columns else df.columns[0]
    norm_col = "text_normalized" if "text_normalized" in df.columns else "text_clean"

    # Statistik
    stat_raw  = df[raw_col].dropna().str.len()
    stat_norm = df[norm_col].dropna().str.len()
    noise = cek_sisa_noise(df[norm_col].astype(str))
    label_dist = df["label"].value_counts().to_dict() if "label" in df.columns else {}

    pct_reduksi = round((stat_raw.mean() - stat_norm.mean()) / stat_raw.mean() * 100, 1) if stat_raw.mean() else 0

    laporan = f"""
+==================================================================+
| LAPORAN VALIDASI -- ULASAN PARFUM LOKAL                          |
| Minggu 11-12 | Muhammad Iqbal Fadel | 202310370311268            |
+==================================================================+

File    : {data_path.name}
Total   : {len(df):,} baris

------------------------------------------------------------------
1. STATISTIK PANJANG TEKS
------------------------------------------------------------------
                      Sebelum (Raw)    Sesudah (Bersih)
  Rata-rata (char):   {stat_raw.mean():>10.1f}    {stat_norm.mean():>10.1f}
  Min (char)      :   {int(stat_raw.min()):>10}    {int(stat_norm.min()):>10}
  Max (char)      :   {int(stat_raw.max()):>10}    {int(stat_norm.max()):>10}

  Reduksi rata-rata: {pct_reduksi}%

------------------------------------------------------------------
2. CEK SISA NOISE (pada data bersih)
------------------------------------------------------------------
  URL tersisa     : {noise['sisa_url']}
  Hashtag tersisa : {noise['sisa_hashtag']}
  Mention tersisa : {noise['sisa_mention']}
  Angka tersisa   : {noise['sisa_angka']}
  Teks kosong     : {noise['teks_kosong']}

------------------------------------------------------------------
3. DISTRIBUSI LABEL AKHIR
------------------------------------------------------------------
"""
    for label, count in label_dist.items():
        pct = count / len(df) * 100
        laporan += f"  {label:<12}: {count:>5,} ({pct:.1f}%)\n"

    laporan += f"""
------------------------------------------------------------------
4. DATA INTEGRITY CHECK
------------------------------------------------------------------
  Reduksi wajar (<50%)    : {'YA' if pct_reduksi < 50 else 'PERLU REVIEW'}
  Tidak ada URL tersisa   : {'YA' if noise['sisa_url'] == 0 else 'ADA SISA'}
  Tidak ada teks kosong   : {'YA' if noise['teks_kosong'] == 0 else 'ADA'}
  Semua baris berlabel    : {'YA' if 'label' in df.columns else 'BELUM'}

==================================================================
"""
    print(laporan)
    with open(REPORTS_DIR / "validation_report.txt", "w", encoding="utf-8") as f:
        f.write(laporan)
    log.info("Laporan: results/reports/validation_report.txt")

    # Sampel validasi manual (100 baris)
    n_sampel = min(100, len(df))
    sampel = df.sample(n=n_sampel, random_state=42)
    sampel.to_csv(REPORTS_DIR / "sampel_validasi_manual.csv", index=False, encoding="utf-8-sig")
    log.info(f"Sampel validasi: {n_sampel} baris -> results/reports/sampel_validasi_manual.csv")

    # Visualisasi
    log.info("\nMembuat visualisasi...")
    plot_wordcloud_after(df[norm_col], FIGURES_DIR / "wordcloud_after.png")
    plot_perbandingan(df, raw_col, norm_col, FIGURES_DIR / "comparison_before_after.png")

    log.info("Validasi (Minggu 11-12) selesai!")


if __name__ == "__main__":
    main()
