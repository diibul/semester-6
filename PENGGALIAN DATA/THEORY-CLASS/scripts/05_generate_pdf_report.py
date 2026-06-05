"""
05_generate_pdf_report.py
=========================
Generate a comprehensive PDF report from the latest progress markdown file.
Includes all visualizations: EDA, RFM, Advanced Analytics, Baseline Model, and GMM.

Author: Muhammad Iqbal Fadel
Date: May 2026 (updated June 2026)
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Try latest markdown first, fallback to older one
MD_CANDIDATES = [
    os.path.join(ROOT, 'reports', 'markdown', 'Laporan_Progres_24-05-2026.md'),
    os.path.join(ROOT, 'reports', 'markdown', 'Laporan - progres (apa yang kita lakukan sekarang).md'),
]

MD_PATH = None
for candidate in MD_CANDIDATES:
    if os.path.exists(candidate):
        MD_PATH = candidate
        break

if MD_PATH is None:
    print('[ERROR] No markdown report found!')
    exit(1)

OUT_PDF = os.path.join(ROOT, 'reports', 'Laporan_Progres_01-06-2026.pdf')

# All visualizations to include in the report
EDA_DIR = os.path.join(ROOT, 'outputs', 'figures', 'eda')
GMM_DIR = os.path.join(ROOT, 'outputs', 'figures', 'gmm')
MODEL_DIR = os.path.join(ROOT, 'outputs', 'figures', 'models')
ANALYSIS_DIR = os.path.join(ROOT, 'outputs', 'figures', 'analysis')

IMAGE_SECTIONS = [
    ("--- EDA Visualizations ---", EDA_DIR, [
        'monthly_sales_trend.png',
        'top20_products_by_revenue.png',
        'top15_countries_by_sales.png',
        'quantity_distribution.png',
        'totalamount_boxplot.png',
    ]),
    ("--- RFM Segmentation ---", EDA_DIR, [
        'rfm_segment_counts.png',
        'rfm_segment_averages_heatmap.png',
    ]),
    ("--- Advanced Analytics ---", EDA_DIR, [
        'basket_top_pairs.png',
        'cohort_retention_heatmap.png',
        'monthly_sales_forecast.png',
    ]),
    ("--- Baseline Model Evaluation ---", MODEL_DIR, [
        'baseline_roc.png',
        'feature_importance.png',
        'confusion_matrix.png',
        'cross_validation_scores.png',
    ]),
    ("--- GMM Clustering (HIGHLIGHT) ---", GMM_DIR, [
        'gmm_bic_aic_selection.png',
        'gmm_cluster_scatter_2d.png',
        'gmm_cluster_scatter_3d.png',
        'gmm_cluster_profiles_radar.png',
        'gmm_cluster_distribution.png',
        'gmm_probability_heatmap.png',
        'gmm_vs_rfm_comparison.png',
    ]),
]


def wrap_text(text, max_chars=95):
    """Wrap long lines of text."""
    lines = []
    for paragraph in text.splitlines():
        if not paragraph:
            lines.append('')
            continue
        while len(paragraph) > max_chars:
            split_at = paragraph.rfind(' ', 0, max_chars)
            if split_at == -1:
                split_at = max_chars
            lines.append(paragraph[:split_at])
            paragraph = paragraph[split_at + 1:]
        lines.append(paragraph)
    return lines


def main():
    print('=' * 60)
    print('  GENERATING PDF REPORT')
    print('=' * 60)

    c = canvas.Canvas(OUT_PDF, pagesize=A4)
    width, height = A4
    left_margin = 2 * cm
    top = height - 2 * cm
    line_height = 12

    # ── Write markdown text ──────────────────────────────────────
    print(f'\n  Reading markdown: {MD_PATH}')
    with open(MD_PATH, 'r', encoding='utf-8') as f:
        md = f.read()

    lines = wrap_text(md, max_chars=100)
    y = top

    for line in lines:
        if y < 3 * cm:
            c.showPage()
            y = top

        # Simple formatting: bold for headers
        if line.startswith('# '):
            c.setFont('Helvetica-Bold', 14)
            line = line.lstrip('# ')
        elif line.startswith('## '):
            c.setFont('Helvetica-Bold', 12)
            line = line.lstrip('# ')
        elif line.startswith('### '):
            c.setFont('Helvetica-Bold', 11)
            line = line.lstrip('# ')
        elif line.startswith('**') and line.endswith('**'):
            c.setFont('Helvetica-Bold', 10)
            line = line.strip('*')
        else:
            c.setFont('Helvetica', 10)

        c.drawString(left_margin, y, line)
        y -= line_height

    # ── Add image sections ───────────────────────────────────────
    print(f'\n  Adding visualizations...')
    margin = 2 * cm
    max_w = width - 2 * margin
    max_h = height - 4 * cm  # Leave room for title

    for section_title, img_dir, images in IMAGE_SECTIONS:
        # Section title page
        c.showPage()
        c.setFont('Helvetica-Bold', 16)
        c.drawCentredString(width / 2, height / 2, section_title)

        for img in images:
            img_path = os.path.join(img_dir, img)
            if not os.path.exists(img_path):
                print(f'  [SKIP] Not found: {img_path}')
                continue

            c.showPage()

            # Image title
            title = img.replace('.png', '').replace('_', ' ').title()
            c.setFont('Helvetica-Bold', 12)
            c.drawCentredString(width / 2, height - 1.5 * cm, title)

            try:
                im = Image.open(img_path)
                iw, ih = im.size
                scale = min(max_w / iw, max_h / ih)
                iw_scaled = iw * scale
                ih_scaled = ih * scale
                x = (width - iw_scaled) / 2
                y = (height - ih_scaled) / 2 - 0.5 * cm
                c.drawImage(img_path, x, y, iw_scaled, ih_scaled)
                print(f'  [OK] Added: {img}')
            except Exception as e:
                c.drawImage(img_path, margin, margin, width - 2 * margin, height - 2 * margin)
                print(f'  [WARN] Fallback render: {img} ({e})')

    c.save()
    print(f'\n  [OK] Saved PDF: {OUT_PDF}')
    print(f'  [OK] Source: {os.path.basename(MD_PATH)}')


if __name__ == '__main__':
    main()
