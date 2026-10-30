# 🛡️ Credit Risk Intelligence

### Credit Portfolio & Risk Intelligence

**📊 An interactive credit-risk dashboard and reproducible Python/SQL analysis of historical credit-card data.**

This project explores how repayment behaviour, credit limits and client characteristics relate to observed payment defaults. It combines **financial analysis, data validation and visualisation** in a browser-based dashboard, supported by a Python and SQLite workflow.

The analysis uses the [UCI *Default of Credit Card Clients* dataset](https://doi.org/10.24432/C55S3H), which contains **30,000 client records** and **6,636 next-month defaults** — an observed default rate of **22.12%**.

> 💡 **Project scope:** This is an exploratory portfolio project using historical data, not a live banking system, predictive credit model or tool for making lending decisions.

---

## 🌐 Explore the Dashboard

**To view the website**, download or clone the repository and open `index.html` in your browser.

The static site works without a server, account or Python installation. You can also publish it through GitHub Pages.

### ✨ Dashboard Features

- **📊 Portfolio Overview:** Headline client statistics, default rates and credit-limit distributions.
- **💳 Repayment & Payment Patterns:** Visualisations of historical repayment behaviour, billing amounts and payment activity.
- **🔎 Data Explorer:** Load a compatible UCI CSV file to calculate client-level segment breakdowns directly in your browser.
- **🎛️ Scenario Analysis:** Adjust a hypothetical default-rate multiplier to explore how the portfolio-level default count would change.

### 🧭 Understanding the Dashboard

Before a CSV is loaded, the static dashboard presents independently published full-sample statistics.

When you load data, the relevant outcome metrics and segment analyses are recalculated from those records.

Historical monthly charts and published distribution statistics remain reference figures and are labelled accordingly.

🔒 **Privacy:** Uploaded files are processed locally in the browser.

---

## 🧠 What This Project Demonstrates

| Area | Implementation |
| --- | --- |
| 📈 Financial Analysis | Default incidence, repayment behaviour, portfolio segmentation and scenario interpretation |
| 🐍 Python | Data ingestion, validation, analytical calculations and report generation |
| 🗄️ SQL / SQLite | Structured client-level data and reproducible aggregation queries |
| 💻 Front-End Development | Interactive HTML, CSS and JavaScript dashboard |
| 📊 Data Communication | Charts, summary statistics, documented assumptions and reproducible outputs |

---

## ⚙️ Run the Full Analysis Locally

The raw UCI dataset is **not included** in this repository.

The Python pipeline can download it automatically or analyse a local copy you provide.

### 1️⃣ Set Up the Environment

**Requirements:** Python 3

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the virtual environment using:

```bash
.venv\Scripts\activate
```

### 2️⃣ Run the Analysis

Choose one of the following options.

**Option A — Download the UCI dataset**

*Internet connection required.*

```bash
python scripts/analyse.py --download
```

**Option B — Use a local dataset**

Place your CSV file inside the `data/` directory.

```bash
python scripts/analyse.py --csv data/UCI_Credit_Card.csv
```

### 3️⃣ Open the Generated Dashboard

After running the analysis, open:

`outputs/dashboard_full.html`

Unlike the static landing page, this generated HTML dashboard embeds the processed dataset for local, interactive segment exploration.

✅ No separate backend is needed to view the generated dashboard.

---

## 📁 Generated Outputs

The analysis pipeline generates the following files:

| File | Description |
| --- | --- |
| `outputs/dashboard_full.html` | Standalone interactive dashboard generated from imported records |
| `outputs/ANALYSIS_REPORT.md` | Results summary and segmented risk analysis |
| `outputs/analysis_results.json` | Calculated metrics and data-quality checks |
| `outputs/default_by_repayment.png` | Default-rate visualisation by repayment category |
| `outputs/billing_and_payments.png` | Billing and payment visualisation |
| `data/credit_risk.sqlite` | SQLite database for client-level analysis |
| `data/credit_clients_clean.csv` | Validated and cleaned dataset |

---

## 🗂️ Project Structure

The repository is organised as follows:

```text
.
├── index.html                 # Interactive static website
├── README.md                  # Project documentation
├── requirements.txt           # Python dependencies
├── scripts/
│   └── analyse.py             # Data pipeline and report generation
├── sql/
│   └── 01_portfolio_analysis.sql
├── tests/                     # Python and browser-logic tests
│   ├── test_analysis.py
│   └── test_dashboard.cjs
├── data/                      # Local input and generated data
└── outputs/                   # Generated reports, charts and dashboard
```

The SQL analysis file contains queries to reproduce portfolio checks and aggregations from the processed data.

---

## 🧪 Testing & Validation

The project includes automated tests for both the Python analysis pipeline and JavaScript dashboard logic.

**🐍 Python unit tests**

```bash
python -m unittest discover -s tests -v
```

**💻 JavaScript browser-logic tests**

Requires Node.js. No additional packages are needed.

```bash
node tests/test_dashboard.cjs
```

---

## 📐 Analytical Approach & Limitations

The project follows a descriptive, evidence-based approach to credit portfolio analysis.

- **🎯 Default Definition:** The target is the recorded next-month default-payment flag (`0` or `1`). The observed default rate is calculated as the number of flagged clients divided by the number of analysed clients.

- **📊 Portfolio Segmentation:** Group-level default rates describe associations within the historical sample. They do not establish causality or individual creditworthiness.

- **💳 Repayment Status Codes:** Codes `-2`, `-1`, `0`, `1` and `2+` are preserved separately rather than assigning unsupported meanings to undocumented codes.

- **💰 Credit Exposure:** A credit limit is not equivalent to outstanding exposure, exposure at default (EAD) or expected credit loss (ECL).

- **🎛️ Scenario Analysis:** The default-rate multiplier is a simplified sensitivity exercise, **not** a statistically estimated stress scenario or predictive forecast.

- **✅ Data Quality:** The import workflows validate key field values and data formats. Duplicate-client detection depends on the availability of actual client IDs; generated row IDs do not establish uniqueness.

- **📅 Historical Context:** The underlying records date from 2005. Results should not be interpreted as representative of contemporary credit portfolios.

> ⚠️ **Responsible interpretation:** Demographic breakdowns, where included, are descriptive and should be interpreted with attention to fairness, potential bias and the limitations of historical data.

---

## 📚 Data Sources & Attribution

**📂 Original Dataset**

Yeh, I. (2009). [*Default of Credit Card Clients*](https://doi.org/10.24432/C55S3H). UCI Machine Learning Repository.

Dataset licensed under [Creative Commons Attribution 4.0 (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). This project contains transformations and analytical summaries.

**📊 Published Default Totals**

[PyML Dataset Documentation — Credit Card Default](https://pyml-datasets.readthedocs.io/en/latest/datasets/credit_card_default.html)

**📈 Published Summary Statistics**

[*Journal of Risk and Financial Management* — Table 3](https://www.mdpi.com/1911-8074/19/9/674)

---

### 🛡️ Credit Risk Intelligence

*Exploring historical credit risk through financial analysis, reproducible data workflows and interactive visualisation.*
