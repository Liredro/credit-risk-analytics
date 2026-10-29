# Credit Portfolio & Risk Intelligence

**An interactive credit-risk dashboard and reproducible Python/SQL analysis of historical credit-card data.**

This project explores how repayment behaviour, credit limits and client characteristics relate to observed payment defaults. It combines financial analysis, data validation and visualisation in a browser-based dashboard, supported by a Python and SQLite workflow.

The analysis uses the [UCI *Default of Credit Card Clients* dataset](https://doi.org/10.24432/C55S3H), which contains **30,000 client records** and **6,636 next-month defaults** — an observed default rate of **22.12%**.

> **Project scope:** This is an exploratory portfolio project using historical data, not a live banking system, predictive credit model or tool for making lending decisions.

## Explore the dashboard

**To view the website**, download or clone the repository and open `index.html` in your browser. The static site works without a server, account or Python installation. You can also publish it through GitHub Pages (instructions below).

The dashboard includes:

- **Portfolio overview:** headline client, default-rate and credit-limit statistics.
- **Repayment and payment patterns:** visualisations of historical repayment, billing and payment data.
- **Data Explorer:** load a compatible UCI CSV file to calculate client-level segment breakdowns in your browser.
- **Scenario analysis:** adjust a hypothetical default-rate multiplier to explore how the portfolio-level default count would change.

**How to interpret the website:** Before a CSV is loaded, the static dashboard presents independently published full-sample statistics. When you load data, the relevant outcome metrics and segment analyses are recalculated from those records. Historical monthly charts and published distribution statistics remain reference figures and are labelled accordingly. Uploaded files are processed locally in the browser.

## What this project demonstrates

| Area | Implementation |
| --- | --- |
| Financial analysis | Default incidence, repayment behaviour, portfolio segmentation and scenario interpretation |
| Python | Data ingestion, validation, analytical calculations and report generation |
| SQL / SQLite | Structured client-level data and reproducible aggregation queries |
| Front-end development | Interactive HTML, CSS and JavaScript dashboard |
| Data communication | Charts, summary statistics, documented assumptions and reproducible outputs |

## Run the full analysis locally

The raw UCI dataset is **not included** in this repository. The Python pipeline can download it or analyse a copy you provide.

**1. Set up the environment** (Python 3 required):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows, activate the virtual environment with `.venv\Scripts\activate` instead.

**2. Run the analysis**, using either option:

```bash
# Option A: Download the UCI source (internet connection required)
python scripts/analyse.py --download

# Option B: Use a local dataset placed in data/
python scripts/analyse.py --csv data/UCI_Credit_Card.csv
```

**3. Open the generated dashboard:** `outputs/dashboard_full.html`.

Unlike the static landing page, this generated HTML dashboard embeds the processed dataset for local, interactive segment exploration. No separate backend is needed to view it.

### Generated outputs

| File | Contents |
| --- | --- |
| `outputs/dashboard_full.html` | Standalone interactive dashboard generated from imported records |
| `outputs/ANALYSIS_REPORT.md` | Results summary and segmented risk analysis |
| `outputs/analysis_results.json` | Calculated metrics and data-quality checks |
| `outputs/default_by_repayment.png` | Default-rate visualisation by repayment category |
| `outputs/billing_and_payments.png` | Billing and payment visualisation |
| `data/credit_risk.sqlite` | SQLite database for client-level analysis |
| `data/credit_clients_clean.csv` | Validated and cleaned dataset |

## Project structure

The commands above assume the following repository organisation:

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

### Tests

```bash
# Python unit tests
python -m unittest discover -s tests -v

# Browser-logic tests (requires Node.js; no extra packages)
node tests/test_dashboard.cjs
```

## Analytical approach and limitations

- **Outcome:** The target is the recorded next-month default-payment flag (`0` or `1`), and the observed default rate is the number of flagged clients divided by the number of analysed clients.
- **Segmentation:** Group-level default rates describe associations in this historical sample; they do not establish causality or individual creditworthiness.
- **Repayment codes:** Codes `-2`, `-1`, `0`, `1` and `2+` are preserved separately rather than assigning unsupported meanings to undocumented codes.
- **Credit limits:** A credit limit is not an outstanding exposure, exposure at default or expected credit loss.
- **Scenario tool:** The multiplier is a simple sensitivity exercise, **not** a statistically estimated stress scenario or forecast.
- **Data quality:** The import workflows check key field values and data formats. Duplicate-client detection depends on the availability of actual client IDs; generated row IDs do not establish uniqueness.
- **Historical context:** The underlying records date from 2005. Results should not be treated as representative of today's credit portfolios.

Demographic breakdowns, where included, are descriptive and should be interpreted with attention to fairness and potential bias.

## Data sources and attribution

- **Original dataset:** Yeh, I. (2009), [*Default of Credit Card Clients*](https://doi.org/10.24432/C55S3H), UCI Machine Learning Repository. Dataset licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); this project contains transformations and analytical summaries.
- **Published default totals:** [PyML dataset documentation](https://pyml-datasets.readthedocs.io/en/latest/datasets/credit_card_default.html).
- **Published summary statistics:** [*Journal of Risk and Financial Management*, Table 3](https://www.mdpi.com/1911-8074/19/9/674).
