"""
scripts/02_data_profiling/profiling.py
=======================================
Minggu 3-4: Data Profiling
Menganalisis seberapa "kotor" dataset ulasan parfum lokal.

Dataset format: CSV dengan delimiter ';'
Kolom: USERNAME | TIME | REVIEW

Output:
  - results/reports/profiling_report.txt
  - results/figures/top_kata_raw.png
  - results/figures/wordcloud_before.png
"""

import sys
import re
from pathlib import Path
from collections import Counter

# Force UTF-8 output di Windows terminal
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Path setup ─────────────────────────────────────────────────────────────────
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()
sys.path.insert(0, str(ROOT_DIR))

RAW_DIR      = ROOT_DIR / "data" / "raw"
REPORTS_DIR  = ROOT_DIR / "results" / "reports"
FIGURES_DIR  = ROOT_DIR / "results" / "figures"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s | %(levelname)-8s | %(message)s",
                    datefmt="%H:%M:%S")
log = logging.getLogger("DataProfiling")

# ──────────────────────────────────────────────────────────────────────────────
# LOAD & BERSIHKAN DATA (hanya noise struktural, bukan teks)
# ──────────────────────────────────────────────────────────────────────────────

def load_dataset(path: Path) -> pd.DataFrame:
    """Load CSV semicolon-delimited, buang baris noise struktural."""
    df = pd.read_csv(path, sep=";", encoding="utf-8",
                     on_bad_lines="skip", engine="python")
    log.info(f"Dimuat mentah: {len(df):,} baris | kolom: {list(df.columns)}")

    # Pastikan kolom REVIEW ada
    if "REVIEW" not in df.columns:
        # Coba rename kolom pertama sebagai USERNAME, kedua TIME, ketiga REVIEW
        if len(df.columns) >= 3:
            df.columns = ["USERNAME", "TIME", "REVIEW"] + list(df.columns[3:])
        else:
            raise ValueError(f"Kolom tidak dikenali: {list(df.columns)}")

    # Buang baris noise struktural (bukan review asli):
    # - REVIEW kosong / NaN
    # - Baris yang berisi karakter aneh (î£œ, Share, Like, dst)
    def is_noise_row(row) -> bool:
        rev = str(row.get("REVIEW", "") or "")
        usr = str(row.get("USERNAME", "") or "")
        if not rev.strip():
            return True
        for prefix in ("î", "ã", "Translated", "See original", "Like", "Share"):
            if rev.startswith(prefix) or usr.startswith("î"):
                return True
        return False

    mask_valid = ~df.apply(is_noise_row, axis=1)
    df_clean = df[mask_valid].copy().reset_index(drop=True)
    n_buang = len(df) - len(df_clean)
    log.info(f"Baris noise struktural dibuang: {n_buang:,}")
    log.info(f"Baris valid tersisa: {len(df_clean):,}")
    return df, df_clean

# ──────────────────────────────────────────────────────────────────────────────
# FUNGSI ANALISIS
# ──────────────────────────────────────────────────────────────────────────────

def hitung_duplikat(df: pd.DataFrame, col: str = "REVIEW") -> dict:
    n_dup = df[col].duplicated().sum()
    return {"jumlah": int(n_dup), "persen": round(n_dup / len(df) * 100, 2)}


def hitung_missing(df: pd.DataFrame) -> pd.DataFrame:
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    return pd.DataFrame({"missing": missing, "persen": pct}).query("missing > 0")


def identifikasi_noise(teks: pd.Series) -> dict:
    n = len(teks)
    return {
        "mengandung_url"         : int(teks.str.contains(r"https?://|www\.", regex=True, na=False).sum()),
        "mengandung_hashtag"     : int(teks.str.contains(r"#\w+", regex=True, na=False).sum()),
        "mengandung_mention"     : int(teks.str.contains(r"@\w+", regex=True, na=False).sum()),
        "mengandung_emoji"       : int(teks.apply(
                                       lambda t: any(ord(c) > 127 and
                                       (0x1F300 <= ord(c) <= 0x1FAFF or
                                        0x2600 <= ord(c) <= 0x27BF or
                                        0x1F600 <= ord(c) <= 0x1F64F)
                                       for c in str(t))).sum()),
        "mengandung_angka"       : int(teks.str.contains(r"\d+", regex=True, na=False).sum()),
        "teks_sangat_pendek_<10" : int((teks.str.len() < 10).sum()),
        "teks_sangat_panjang_500": int((teks.str.len() > 500).sum()),
        "total"                  : n,
    }


def top_kata(teks: pd.Series, n: int = 30) -> list:
    stopwords = {
        "the","and","is","in","of","to","a","for","it","with","very","so",
        "yang","dan","di","ke","dari","ini","itu","dengan","untuk","pada",
        "tidak","ada","juga","atau","sudah","saya","kami","kamu","anda",
        "mereka","ia","dia","nya","adalah","jadi","bisa","lebih","itu",
        "ini","ya","ga","gak","si","lah","deh","aja","banget","bgt",
        "sangat","really","also","are","was","were","be","been","have",
        "has","had","they","them","their","all","at","by","as","an","he",
        "she","we","my","me","you","your","our","from","on","about","that",
        "this","but","not","i","good","great","nice","service","staff","very",
        "perfume","parfum","smell","scent","friendly","the"
    }
    words = []
    for t in teks.dropna():
        words.extend(re.findall(r"\b[a-zA-Z]{2,}\b", str(t).lower()))
    filtered = [w for w in words if w not in stopwords]
    return Counter(filtered).most_common(n)


def top_kata_indonesia(teks: pd.Series, n: int = 20) -> list:
    """Fokus kata gaul / informal Bahasa Indonesia."""
    gaul_pattern = re.compile(
        r"\b(bgt|banget|bngt|ga|gak|nggak|kagak|makasih|trims|terima kasih|"
        r"oke|ok|sip|mantap|keren|parah|anjir|waduh|aduh|wah|yah|duh|"
        r"sis|bro|kak|mbak|mas|bg|abg|kakak|adek|dek|mba|om|tante|"
        r"receh|lebay|garing|absurd|bucin|baper|galau|bete|kesel|seneng|"
        r"kece|kece badai|hits|viral|fomo|wkwk|haha|hehe|xixi|lol|"
        r"btw|cmiiw|oot|imho|fyi|afaik|asap|asik|seru|asyik|laper|"
        r"healing|coba|cobain|worth|recomen|rekomend|rekomen)\b",
        re.IGNORECASE
    )
    found = []
    for t in teks.dropna():
        found.extend(gaul_pattern.findall(str(t).lower()))
    return Counter(found).most_common(n)


# ──────────────────────────────────────────────────────────────────────────────
# VISUALISASI
# ──────────────────────────────────────────────────────────────────────────────

def plot_top_kata(top_list: list, simpan_ke: Path, judul: str) -> None:
    if not top_list:
        return
    kata, freq = zip(*top_list)
    fig, ax = plt.subplots(figsize=(12, 7))
    colors = plt.cm.viridis_r([i / len(kata) for i in range(len(kata))])
    bars = ax.barh(list(kata)[::-1], list(freq)[::-1], color=colors[::-1])
    ax.set_xlabel("Frekuensi", fontsize=12)
    ax.set_title(judul, fontsize=14, fontweight="bold", pad=12)
    ax.bar_label(bars, padding=3, fontsize=9)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(simpan_ke, dpi=150, bbox_inches="tight")
    plt.close()
    log.info(f"  Grafik: {simpan_ke.name}")


def plot_noise_overview(noise: dict, simpan_ke: Path) -> None:
    """Bar chart ringkasan noise."""
    labels = list(noise.keys())[:-1]   # hapus 'total'
    values = list(noise.values())[:-1]
    n_total = noise["total"]
    pct = [round(v / n_total * 100, 1) for v in values]

    label_display = [l.replace("_", " ").title() for l in labels]
    colors = ["#EF5350" if v > 0 else "#B0BEC5" for v in values]

    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(label_display, values, color=colors, edgecolor="white", linewidth=1.2)
    for bar, p in zip(bars, pct):
        if bar.get_height() > 0:
            ax.text(bar.get_x() + bar.get_width()/2,
                    bar.get_height() + 0.5,
                    f"{p}%", ha="center", va="bottom", fontsize=9, fontweight="bold")
    ax.set_ylabel("Jumlah Baris", fontsize=11)
    ax.set_title(f"Distribusi Tipe Noise (Total data valid: {n_total:,} baris)",
                 fontsize=13, fontweight="bold")
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=20, ha="right", fontsize=9)
    plt.tight_layout()
    plt.savefig(simpan_ke, dpi=150, bbox_inches="tight")
    plt.close()
    log.info(f"  Grafik: {simpan_ke.name}")


def plot_wordcloud(teks: pd.Series, simpan_ke: Path, judul: str) -> None:
    try:
        from wordcloud import WordCloud
    except ImportError:
        log.warning("wordcloud tidak terinstall, skip WordCloud.")
        return
    all_text = " ".join(teks.dropna().astype(str))
    if not all_text.strip():
        return
    wc = WordCloud(width=1200, height=550, background_color="white",
                   colormap="plasma", max_words=200,
                   prefer_horizontal=0.7).generate(all_text)
    fig, ax = plt.subplots(figsize=(14, 6))
    ax.imshow(wc, interpolation="bilinear")
    ax.axis("off")
    ax.set_title(judul, fontsize=15, fontweight="bold", pad=12)
    plt.tight_layout()
    plt.savefig(simpan_ke, dpi=150, bbox_inches="tight")
    plt.close()
    log.info(f"  WordCloud: {simpan_ke.name}")


def plot_distribusi_waktu(df: pd.DataFrame, simpan_ke: Path) -> None:
    """Bar chart distribusi waktu ulasan."""
    if "TIME" not in df.columns:
        return
    time_counts = df["TIME"].value_counts().head(15)
    fig, ax = plt.subplots(figsize=(12, 5))
    bars = ax.bar(time_counts.index, time_counts.values, color="#5C6BC0",
                  edgecolor="white", linewidth=1.2)
    ax.set_xlabel("Waktu", fontsize=11)
    ax.set_ylabel("Jumlah Ulasan", fontsize=11)
    ax.set_title("Distribusi Waktu Ulasan (Top 15)", fontsize=13, fontweight="bold")
    ax.bar_label(bars, fmt="%d", padding=2, fontsize=9)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.spines[["top", "right"]].set_visible(False)
    plt.xticks(rotation=25, ha="right", fontsize=9)
    plt.tight_layout()
    plt.savefig(simpan_ke, dpi=150, bbox_inches="tight")
    plt.close()
    log.info(f"  Grafik: {simpan_ke.name}")


def plot_panjang_teks(teks: pd.Series, simpan_ke: Path) -> None:
    """Histogram distribusi panjang teks."""
    lengths = teks.dropna().str.len()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle("Distribusi Panjang Teks Ulasan (Raw)", fontsize=13, fontweight="bold")

    ax1.hist(lengths, bins=40, color="#42A5F5", edgecolor="white", alpha=0.85)
    ax1.axvline(lengths.mean(), color="#E53935", linestyle="--", linewidth=2,
                label=f"Mean: {lengths.mean():.0f} char")
    ax1.axvline(10, color="#FF9800", linestyle=":", linewidth=1.5, label="Min threshold (10)")
    ax1.set_xlabel("Panjang (karakter)", fontsize=11)
    ax1.set_ylabel("Frekuensi", fontsize=11)
    ax1.set_title("Distribusi Panjang (karakter)")
    ax1.legend(fontsize=9)
    ax1.grid(alpha=0.3)

    word_lengths = teks.dropna().str.split().str.len()
    ax2.hist(word_lengths, bins=30, color="#AB47BC", edgecolor="white", alpha=0.85)
    ax2.axvline(word_lengths.mean(), color="#E53935", linestyle="--", linewidth=2,
                label=f"Mean: {word_lengths.mean():.1f} kata")
    ax2.set_xlabel("Jumlah Kata", fontsize=11)
    ax2.set_ylabel("Frekuensi", fontsize=11)
    ax2.set_title("Distribusi Jumlah Kata")
    ax2.legend(fontsize=9)
    ax2.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(simpan_ke, dpi=150, bbox_inches="tight")
    plt.close()
    log.info(f"  Grafik: {simpan_ke.name}")


# ──────────────────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────────────────

def main():
    log.info("=" * 65)
    log.info("  DATA PROFILING — Ulasan Parfum Lokal (Minggu 3-4)")
    log.info("=" * 65)

    # ── Load ──────────────────────────────────────────────────────────────────
    raw_path = RAW_DIR / "ulasan_parfum_raw.csv"
    if not raw_path.exists():
        candidates = list(RAW_DIR.glob("*.csv"))
        if not candidates:
            log.error("Tidak ada CSV di data/raw/"); return
        raw_path = candidates[0]
        log.warning(f"Menggunakan: {raw_path.name}")

    df_raw, df = load_dataset(raw_path)
    teks = df["REVIEW"].astype(str)

    # ── Analisis ──────────────────────────────────────────────────────────────
    log.info("Menghitung duplikat...")
    dup = hitung_duplikat(df)

    log.info("Menghitung missing values...")
    miss = hitung_missing(df)

    log.info("Mengidentifikasi noise...")
    noise = identifikasi_noise(teks)

    log.info("Mencari top 30 kata umum...")
    top30 = top_kata(teks, 30)

    log.info("Mencari kata gaul/informal...")
    gaul = top_kata_indonesia(teks, 20)

    # Statistik panjang teks
    lengths_char = teks.str.len()
    lengths_word = teks.str.split().str.len()

    # ── Laporan Teks ──────────────────────────────────────────────────────────
    laporan = f"""
╔══════════════════════════════════════════════════════════════════╗
║     LAPORAN DATA PROFILING — ULASAN PARFUM LOKAL                 ║
║     Minggu 3-4 | Muhammad Iqbal Fadel | 202310370311268          ║
╚══════════════════════════════════════════════════════════════════╝

📁 File Raw   : {raw_path.name}
📊 Total Raw  : {len(df_raw):,} baris (termasuk noise struktural)
✅ Data Valid : {len(df):,} baris (setelah buang baris kosong/noise)
📋 Kolom      : {list(df.columns)}

──────────────────────────────────────────────────────────────────
1. DUPLIKAT
──────────────────────────────────────────────────────────────────
   Jumlah duplikat : {dup['jumlah']:,} baris
   Persentase      : {dup['persen']}% dari total data valid

──────────────────────────────────────────────────────────────────
2. MISSING VALUES
──────────────────────────────────────────────────────────────────
{miss.to_string() if not miss.empty else "   Tidak ada missing values pada data valid!"}

──────────────────────────────────────────────────────────────────
3. STATISTIK PANJANG TEKS ULASAN
──────────────────────────────────────────────────────────────────
   Rata-rata : {lengths_char.mean():.1f} karakter | {lengths_word.mean():.1f} kata
   Minimum   : {int(lengths_char.min())} karakter | {int(lengths_word.min())} kata
   Maximum   : {int(lengths_char.max())} karakter | {int(lengths_word.max())} kata
   Median    : {lengths_char.median():.1f} karakter | {lengths_word.median():.1f} kata

──────────────────────────────────────────────────────────────────
4. NOISE DETECTION (pada {noise['total']:,} baris valid)
──────────────────────────────────────────────────────────────────
   Mengandung URL          : {noise['mengandung_url']:>5,} baris  ({noise['mengandung_url']/noise['total']*100:.1f}%)
   Mengandung Hashtag (#)  : {noise['mengandung_hashtag']:>5,} baris  ({noise['mengandung_hashtag']/noise['total']*100:.1f}%)
   Mengandung Mention (@)  : {noise['mengandung_mention']:>5,} baris  ({noise['mengandung_mention']/noise['total']*100:.1f}%)
   Mengandung Emoji        : {noise['mengandung_emoji']:>5,} baris  ({noise['mengandung_emoji']/noise['total']*100:.1f}%)
   Mengandung Angka        : {noise['mengandung_angka']:>5,} baris  ({noise['mengandung_angka']/noise['total']*100:.1f}%)
   Teks Sangat Pendek (<10): {noise['teks_sangat_pendek_<10']:>5,} baris  ({noise['teks_sangat_pendek_<10']/noise['total']*100:.1f}%)
   Teks Sangat Panjang     : {noise['teks_sangat_panjang_500']:>5,} baris  ({noise['teks_sangat_panjang_500']/noise['total']*100:.1f}%)

──────────────────────────────────────────────────────────────────
5. TOP 30 KATA PALING SERING MUNCUL
──────────────────────────────────────────────────────────────────
"""
    for i, (kata, freq) in enumerate(top30, 1):
        laporan += f"   {i:>2}. {kata:<22} : {freq:,}\n"

    laporan += f"""
──────────────────────────────────────────────────────────────────
6. KATA GAUL / INFORMAL DOMAIN PARFUM YANG DITEMUKAN
──────────────────────────────────────────────────────────────────
"""
    if gaul:
        for i, (kata, freq) in enumerate(gaul, 1):
            laporan += f"   {i:>2}. {kata:<22} : {freq:,}\n"
    else:
        laporan += "   (Kata gaul formal belum banyak terdeteksi — data dominan Bahasa Inggris)\n"

    laporan += f"""
──────────────────────────────────────────────────────────────────
7. RINGKASAN KUALITAS DATA
──────────────────────────────────────────────────────────────────
   ✅ Data valid terkumpul  : {len(df):,} baris (memenuhi syarat >1.000)
   ⚠️  Duplikat             : {dup['jumlah']:,} baris ({dup['persen']}%) → perlu dihapus
   ⚠️  Teks pendek (<10 ch) : {noise['teks_sangat_pendek_<10']:,} baris → perlu difilter
   ⚠️  Mengandung emoji     : {noise['mengandung_emoji']:,} baris → perlu dibersihkan
   ℹ️  Bahasa campuran      : Indonesia + Inggris (multi-language dataset)
   ℹ️  Sumber               : Google Review / HMNS & Saff&Co outlet

══════════════════════════════════════════════════════════════════
Laporan dibuat oleh: scripts/02_data_profiling/profiling.py
══════════════════════════════════════════════════════════════════
"""
    print(laporan)

    # Simpan laporan
    report_path = REPORTS_DIR / "profiling_report.txt"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(laporan)
    log.info(f"Laporan disimpan: {report_path}")

    # ── Visualisasi ───────────────────────────────────────────────────────────
    log.info("\nMembuat visualisasi...")
    plot_top_kata(top30, FIGURES_DIR / "top_kata_raw.png",
                  "Top 30 Kata Paling Sering Muncul (Data Mentah)")
    if gaul:
        plot_top_kata(gaul, FIGURES_DIR / "top_kata_gaul.png",
                      "Kata Gaul/Informal yang Ditemukan")
    plot_noise_overview(noise, FIGURES_DIR / "noise_overview.png")
    plot_panjang_teks(teks, FIGURES_DIR / "distribusi_panjang_teks.png")
    plot_distribusi_waktu(df, FIGURES_DIR / "distribusi_waktu.png")
    plot_wordcloud(teks, FIGURES_DIR / "wordcloud_before.png",
                   "Word Cloud — Sebelum Preprocessing (Data Mentah)")

    log.info("\n✅ Data Profiling (Minggu 3-4) selesai!")
    log.info(f"   Laporan  : results/reports/profiling_report.txt")
    log.info(f"   Grafik   : results/figures/ ({len(list(FIGURES_DIR.glob('*.png')))} file)")
    return df


if __name__ == "__main__":
    main()
