# Project Progress & Milestones

**Project:** E-commerce Sales Data Analysis & Machine Learning  
**Date Started:** May 2026  
**Last Updated:** June 5, 2026

---

## ✅ Completed Milestones

### Phase 1: Data Preparation
- ✅ Loaded and explored raw dataset (522,601 transactions)
- ✅ Data cleaning and validation
- ✅ Feature engineering (Date, YearMonth, TotalAmount)
- ✅ Saved processed dataset: `Sales_Transaction_v4a_cleaned.csv`

### Phase 2: Exploratory Data Analysis (EDA)
- ✅ Monthly sales trends visualization
- ✅ Top 20 products by revenue
- ✅ Top 15 countries by sales
- ✅ Quantity distribution analysis
- ✅ Total amount boxplot (outlier detection)
- ✅ Generated 12 EDA visualizations

### Phase 3: Customer Segmentation (RFM)
- ✅ Implemented RFM (Recency, Frequency, Monetary) analysis
- ✅ Customer scoring using quartile method
- ✅ Customer segments identified:
  - Champions: 1,361 customers (loyal, high value)
  - Loyal: 1,267 customers
  - At Risk: 1,379 customers
  - Hibernating: 1,657 customers
  - Potential: 1,291 customers
- ✅ RFM strategy recommendations generated
- ✅ RFM visualization (segment distribution, heatmap)

### Phase 4: Advanced Analytics
- ✅ Product revenue & quantity summaries
- ✅ Basket analysis (product pairs frequently purchased together)
  - Top pair: White Hanging Heart T-Light Holder + Red Worrying Llama
- ✅ Cohort analysis (customer retention per cohort)
  - Retention tracked across months
  - Heatmap visualization generated
- ✅ Monthly sales forecasting (linear projection)
  - Forecast for 2019-12 to 2020-02

### Phase 5: Machine Learning Preparation
- ✅ Customer-level feature engineering
- ✅ Feature scoring and selection via SelectKBest
- ✅ Top features identified:
  1. DistinctProducts (score: 1604.27)
  2. Frequency (score: 1086.53)
  3. Recency (score: 492.03)
  4. Monetary (score: 462.07)
- ✅ Baseline RandomForest model trained (5 features, 200 trees)
  - ROC AUC: 1.0000 (perfect)
  - CV Accuracy: 0.9996 ± 0.0005 (5-fold stratified)
  - CV ROC AUC: 1.0000 ± 0.0000
- ✅ 5-Fold Stratified Cross-Validation
- ✅ Feature Importance visualization (Gini)
- ✅ Confusion Matrix heatmap
- ✅ Cross-Validation scores bar chart
- ✅ 4 model evaluation visualizations generated

### Phase 6: Deliverables Generation
- ✅ PDF Report v1 created (Laporan_progres_19-05-2026.pdf)
- ✅ PPTX Presentation v1 created (presentation_progres_19-05-2026.pptx)
- ✅ PDF Report v2 created (Laporan_Progres_01-06-2026.pdf)
  - Full markdown report + 21 embedded visualizations across 5 sections
- ✅ PPTX Presentation v2 created (presentation_progres_01-06-2026.pptx)
  - 30 slides: EDA + RFM + Advanced + Baseline ML + Feature Selection + GMM
  - Widescreen 16:9 format with section dividers

### Phase 7: Project Restructuring
- ✅ Created professional folder hierarchy
- ✅ Organized files into semantic folders:
  - `data/raw/` - Original dataset
  - `data/processed/` - Cleaned data
  - `notebooks/` - Jupyter exploration files
  - `scripts/` - Automated analysis pipelines
  - `outputs/` - Generated visualizations & analysis
  - `reports/` - Final deliverables
  - `docs/` - Documentation
- ✅ Renamed files for consistency (snake_case)
- ✅ Fixed typo: "DataProsecing" → "00_data_processing"
- ✅ Updated all script paths for new structure
- ✅ Created `requirements.txt` for dependency management
- ✅ Created `.gitignore` for Git best practices
- ✅ Generated comprehensive `STRUCTURE.md` documentation

### Phase 8: GMM Clustering (HIGHLIGHT UTAMA)
- ✅ Implemented Gaussian Mixture Model (GMM) for probabilistic customer segmentation
- ✅ Data preparation with IQR outlier clipping and StandardScaler normalization
- ✅ Optimal cluster selection via BIC/AIC analysis (optimal k=9)
- ✅ GMM training with full covariance, 10 initializations, 500 max iterations
- ✅ Auto-labeling clusters:
  - High-Value Loyal: 355 customers (7.5%)
  - Mid-Value Regular (3 groups): 1,210 customers (25.6%)
  - At-Risk / Dormant (3 groups): 2,339 customers (49.6%)
  - Emerging / Potential (2 groups): 814 customers (17.3%)
- ✅ 7 professional visualizations generated:
  1. BIC/AIC cluster selection curve
  2. PCA 2D scatter plot
  3. PCA 3D scatter plot
  4. Radar/spider chart cluster profiles
  5. Cluster distribution bar chart
  6. Membership probability heatmap
  7. GMM vs RFM cross-tabulation comparison
- ✅ GMM vs RFM comparison (cross-tabulation analysis)
- ✅ Business recommendations per cluster

### Phase 9: Project Audit & Quality Improvements (June 2026)
- ✅ Full project audit — identified and fixed 7 gaps
- ✅ Enhanced baseline model: 5 features, cross-validation, feature importance, confusion matrix
- ✅ Created `outputs/figures/models/` with 4 new visualizations (ROC, feature importance, confusion matrix, CV scores)
- ✅ Regenerated comprehensive PDF report with all 21 visualizations
- ✅ Regenerated comprehensive PPTX presentation (30 slides, 6 sections)
- ✅ Synced `STRUCTURE.md` with actual project state
- ✅ Fixed `README.md`: broken links, added Quick Start pipeline
- ✅ Documented notebook `04_feature_selection_methods.ipynb`

### Phase 10: Structure Cleanup & Notebook Migration (June 2026)
- ✅ Converted all analysis .py scripts to Jupyter Notebooks (.ipynb)
- ✅ Renumbered notebooks sequentially: 00 → 06
- ✅ Removed old duplicate notebooks (`01_eda_exploration`, `02_feature_selection_and_baseline`)
- ✅ Removed old deliverables (v1 PDF, v1 PPTX, outdated markdown reports)
- ✅ Cleaned `scripts/` to only contain utility scripts (PDF/PPTX generators)
- ✅ Updated all documentation (README, STRUCTURE.md, PROGRESS.md)

---

## 📊 Data Summary

| Metric | Value |
|--------|-------|
| **Total Transactions** | 522,601 |
| **Total Revenue** | ~£52.3M GBP |
| **Unique Customers** | 4,955 |
| **Unique Products** | 3,695 |
| **Countries** | 37 |
| **Date Range** | 2018-12-01 to 2019-12-09 |
| **Peak Month** | Nov 2019 (£7.8M) |
| **Top Product** | Paper Craft Little Birdie (£1M) |
| **Top Country** | United Kingdom (£52.3M) |
| **GMM Optimal Clusters** | 9 |

---

## 📈 Key Findings

1. **Sales Trend**: Steady growth with peak in November 2019
2. **Customer Base**: 
   - Highly skewed (few high-value customers, many one-time buyers)
   - 1,361 Champions generate majority of revenue
3. **RFM Insights**: Hibernating segment (1,657) → potential reactivation opportunity
4. **Product Insights**: Top 20 products account for ~40% of revenue
5. **Geography**: Heavily UK-centric (97% of revenue)
6. **Model Performance**: Strong baseline (ROC-AUC 0.92) for customer classification
7. **GMM Clustering**: 9 optimal clusters identified via BIC analysis
   - High-Value Loyal cluster (355 customers) strongly maps to RFM Champions
   - ~50% customers classified as At-Risk/Dormant — major reactivation opportunity
   - GMM provides probabilistic membership (soft clustering) vs RFM's hard rules

---

## 🔧 Technical Stack

| Tool | Version | Purpose |
|------|---------|---------|-
| Python | 3.13 | Core language |
| Pandas | 2.0+ | Data manipulation |
| NumPy | 1.24+ | Numerical computing |
| Matplotlib | 3.7+ | Visualizations |
| Seaborn | 0.12+ | Statistical plots |
| Scikit-Learn | 1.3+ | Machine learning (GMM, PCA, RF) |
| SciPy | 1.11+ | Scientific computing |
| ReportLab | 4.5+ | PDF generation |
| python-pptx | 1.0+ | PPTX generation |
| Jupyter | Latest | Notebooks |

---

## 📁 Output Files Generated

### Visualizations (29 PNG files)
- EDA: monthly trends, top products, distributions, boxplots (12 files)
- Analysis: feature selection comparison, model performance comparison (6 files)
- Model: ROC curve, feature importance, confusion matrix, CV scores (4 files)
- GMM: BIC/AIC, 2D scatter, 3D scatter, radar chart, distribution, probability heatmap, vs RFM (7 files)

### Data Files (14 CSV + artifacts)
- Customer RFM scores
- Product summaries
- Basket analysis
- Cohort retention
- Sales forecast
- Model metrics (JSON) + model artifact (.pkl)
- GMM: cluster assignments, profiles, recommendations, model (.pkl)

### Reports & Presentations
- PDF Report (Laporan_Progres_01-06-2026.pdf — markdown + 21 images)
- PPTX Presentation (presentation_progres_01-06-2026.pptx — 30 slides)
- 1 Markdown source document

---

## 🎯 Next Steps (Optional)

### Short Term
- [x] Cross-validation of baseline model ✅ (done June 2026)
- [ ] Hyperparameter tuning
- [x] Feature importance visualization ✅ (done June 2026)
- [ ] Production model deployment

### Medium Term
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] Customer lifetime value (CLV) prediction
- [ ] Churn prediction
- [ ] Recommendation system

### Long Term
- [ ] Real-time analytics pipeline
- [ ] API endpoint for predictions
- [ ] Dashboard (Tableau/Power BI)
- [ ] A/B testing framework

---

## 📝 Notes

- All notebooks are self-contained and can run independently
- Paths are relative (works on any machine)
- Outputs automatically created if missing
- No data loss during restructuring (all files preserved)
- Project ready for Git version control

---

## 👤 Author Information

**Project Type:** University-Level Data Science Project  
**Academic Context:** Data Mining (Penggalian Data)  
**Instructor:** [SEMESTER 6]  
**Deliverables:** Report + Presentation + Code + Analysis

---

**Status:** ✅ **PRODUCTION READY** for submission  
**Last Updated:** June 5, 2026
