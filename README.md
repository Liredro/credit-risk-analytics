# Credit Portfolio & Risk Intelligence

**A finance × data × code portfolio project.** A standalone dark-mode interactive website alongside a reproducible Python/SQL analysis pipeline for the historical *Default of Credit Card Clients* dataset.

## Open the finished website

Open [`index.html`](index.html) in a modern browser. It requires no build tools, logins, external fonts, chart libraries, or servers. It displays independently published source-backed metrics immediately, including **30,000 clients**, **6,636 defaults (22.12%)**, mean credit limits and six months of statement/payment means. The default-rate stress slider works offline. You can also use **Load CSV** in the Data Explorer to calculate repayment, credit-limit and age breakdowns instantly using an official UCI CSV file. The file remains inside the user's browser.

**Important provenance distinction:** `index.html` is a *published-statistics snapshot*, not a claim that the complete raw dataset was executed in this environment. Published aggregates are shown for the full 30k sample; loading a subset updates outcome KPIs, but historical chart values and quartiles remain full-sample source statistics (as labelled). No subgroup statistics have been fabricated. The full pipeline can create a client-record-backed HTML page with all subgroup analyses included.

## Generate the full analysis & self-contained dashboard

The dataset is public, but its raw file is **not bundled** in this project. If you have `UCI_Credit_Card.csv`, put it inside `data/` and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python scripts/analyse.py --csv data/UCI_Credit_Card.csv
```

Or fetch the official UCI source directly (requires an internet connection):

```bash
python scripts/analyse.py --download
```

Open **`outputs/dashboard_full.html`** — the entire analytical dataset is embedded locally, allowing immediate interactive segment exploration without downloading records or uploading a CSV to the browser. Further outputs:

- `outputs/ANALYSIS_REPORT.md` — computed executive results and segmented risk table.
- `outputs/analysis_results.json` — machine-readable calculations & quality checks.
- `outputs/default_by_repayment.png` & `outputs/billing_and_payments.png` — illustrative findings visualised from the actual imported dataset.
- `data/credit_risk.sqlite` — client-level SQLite table with derived segment columns.
- `data/credit_clients_clean.csv` — canonical cleaned file with original feature codes intact.
- `sql/01_portfolio_analysis.sql` — fully reproducible SQL checks and aggregations.

Run Python unit tests:

```bash
python -m unittest discover -s tests -v
```

## Methodology

- Unit of analysis: one credit-card client. Outcome is the dataset's next-month payment-default flag (binary 0/1).
- Observed default incidence: `sum(default_flag)/number_of_clients`.
- Billing and payment figures: arithmetic mean per client per month; **not** a realised default-loss timeline.
- September repayment codes `-2`, `-1`, `0`, `1`, and `2+` are kept separate. `-2` and `0` occur in the real data but are undocumented by UCI's original dictionary. We do not arbitrarily relabel them as delinquency or non-use.
- Client credit limit is **not** drawn balance, EAD or expected credit loss.
- Scenario lab: a hypothetical relative multiplier applied to observed default incidence, not a trained stress model.
- Demographic group breakdowns are descriptive and require fairness review; no individual client credit decisions are advocated.
- Data are from 2005 and are not representative of a current lending portfolio.

## Sources & licence

- Yeh, I. (2009). *Default of Credit Card Clients*, UCI Machine Learning Repository: https://doi.org/10.24432/C55S3H — **CC BY 4.0**. The portfolio makes transformations and analytic summaries of the dataset.
- Source-based outcome totals: https://pyml-datasets.readthedocs.io/en/latest/datasets/credit_card_default.html (30,000 observations, 6,636 default flags).
- Published source statistics (percentiles, six-month bill and payment means): https://www.mdpi.com/1911-8074/19/9/674 (Table 3).

No live connection to a bank, regulated credit decisioning, or predictive model is claimed.
