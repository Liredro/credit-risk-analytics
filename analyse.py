#!/usr/bin/env python3
"""Reproducible UCI Default of Credit Card Clients analysis.

Use:
  python scripts/analyse.py --csv data/UCI_Credit_Card.csv
or (network access required):
  python scripts/analyse.py --download

Outputs: SQLite database, CSV, JSON, Markdown report, two PNG plots and
an offline dashboard with the full dataset embedded in its HTML.
"""
from __future__ import annotations
import argparse
import json
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data'
OUT = ROOT / 'outputs'
ORIGINAL_COLS = [
    'LIMIT_BAL', 'SEX', 'EDUCATION', 'MARRIAGE', 'AGE',
    'PAY_0', 'PAY_2', 'PAY_3', 'PAY_4', 'PAY_5', 'PAY_6',
    'BILL_AMT1', 'BILL_AMT2', 'BILL_AMT3', 'BILL_AMT4', 'BILL_AMT5', 'BILL_AMT6',
    'PAY_AMT1', 'PAY_AMT2', 'PAY_AMT3', 'PAY_AMT4', 'PAY_AMT5', 'PAY_AMT6',
]
TARGET = 'default.payment.next.month'


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Normalise UCI CSV or ucimlrepo columns; preserve raw codes."""
    data = df.copy()
    data.columns = [str(k).strip().replace('default payment next month', TARGET) for k in data.columns]
    renames = {f'X{i}': name for i, name in enumerate(ORIGINAL_COLS, 1)}
    renames.update({'Y': TARGET, 'default_next_month': TARGET,
                    'credit_limit_ntd': 'LIMIT_BAL', 'repayment_status_sep': 'PAY_0',
                    'age': 'AGE'})
    data = data.rename(columns=renames)
    required = ORIGINAL_COLS + [TARGET]
    missing = [k for k in required if k not in data.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}; input must be original UCI data.')
    if 'ID' not in data:
        data.insert(0, 'ID', range(1, len(data) + 1))
    for name in ['ID', *required]:
        data[name] = pd.to_numeric(data[name], errors='raise')
    if data[required].isna().any().any():
        raise ValueError('Missing values in required analytical fields.')
    if data.ID.duplicated().any():
        raise ValueError('Duplicate client identifiers.')
    if not data[TARGET].isin([0, 1]).all():
        raise ValueError('Target is not a valid binary 0/1 flag.')
    if (data.LIMIT_BAL <= 0).any():
        raise ValueError('Credit limit must be positive.')
    if (data.AGE < 0).any():
        raise ValueError('Age cannot be negative.')
    return data[['ID', *required]].copy()


def source_data(csv: Path | None, download: bool) -> pd.DataFrame:
    if csv is not None:
        return pd.read_csv(csv)
    if not download:
        raise SystemExit('Use --csv <file> or --download to fetch UCI dataset 350.')
    try:
        from ucimlrepo import fetch_ucirepo
    except ImportError as exc:
        raise SystemExit('Install requirements.txt to use --download.') from exc
    dataset = fetch_ucirepo(id=350)
    df = dataset.data.features.copy().reset_index(drop=True)
    target = dataset.data.targets.copy().reset_index(drop=True)
    df[TARGET] = target.iloc[:, 0]
    ids = getattr(dataset.data, 'ids', None)
    if isinstance(ids, pd.DataFrame) and not ids.empty:
        df.insert(0, 'ID', ids.iloc[:, 0].reset_index(drop=True))
    return df


def code_group(p: int) -> str:
    if p == -2:
        return 'Code -2'
    if p == -1:
        return 'Code -1'
    if p == 0:
        return 'Code 0'
    if p == 1:
        return '1 month late'
    if p >= 2:
        return '2+ months late'
    return 'Other'


def add_segments(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out['repayment_group'] = out.PAY_0.astype(int).map(code_group)
    out['limit_band'] = pd.cut(out.LIMIT_BAL, bins=[0, 50000, 100000, 200000, 300000, np.inf],
            labels=['≤ 50k', '50–100k', '100–200k', '200–300k', '> 300k'], include_lowest=True)
    out['age_band'] = pd.cut(out.AGE, bins=[0, 30, 40, 50, 60, np.inf], right=False,
            labels=['< 30', '30–39', '40–49', '50–59', '60+'])
    return out


def segment_stats(df: pd.DataFrame, group: str) -> list[dict]:
    values = []
    for name, row in df.groupby(group, observed=True)[TARGET].agg(['size', 'sum']).iterrows():
        n = int(row['size']); d = int(row['sum'])
        values.append({'segment': str(name), 'clients': n, 'defaults': d, 'rate': d/n})
    return values


def analyse(df: pd.DataFrame) -> dict:
    x = add_segments(df)
    n = len(x); defaults = int(x[TARGET].sum())
    monthly = []
    for month, no in [('Apr',6),('May',5),('Jun',4),('Jul',3),('Aug',2),('Sep',1)]:
        monthly.append({'month': month,
                        'mean_bill_ntd': float(x[f'BILL_AMT{no}'].mean()),
                        'mean_payment_ntd': float(x[f'PAY_AMT{no}'].mean())})
    dq = {'missing_cells': int(x.isna().sum().sum()),
          'duplicate_ids': int(x.ID.duplicated().sum()),
          'undocumented_education_codes': int(x.EDUCATION.isin([0,5,6]).sum()),
          'undocumented_marital_code': int((x.MARRIAGE==0).sum()),
          'repayment_sep_undocumented_minus2_or0': int(x.PAY_0.isin([-2,0]).sum()),
          'negative_september_bill_count': int((x.BILL_AMT1 < 0).sum())}
    return {'source': 'UCI Default of Credit Card Clients · 2005 · CC BY 4.0',
            'doi':'10.24432/C55S3H',
            'portfolio': {'clients': n, 'defaults': defaults, 'non_defaults':n-defaults,
                          'default_rate':defaults/n,'mean_credit_limit_ntd':float(x.LIMIT_BAL.mean()),
                          'median_credit_limit_ntd':float(x.LIMIT_BAL.median())},
            'monthly': monthly,
            'segments': {'repayment_group':segment_stats(x,'repayment_group'),
                         'limit_band':segment_stats(x,'limit_band'),
                         'age_band':segment_stats(x,'age_band')},
            'quality':dq}


def write_report(res: dict, location: Path) -> None:
    p=res['portfolio']; q=res['quality']
    content=['# Credit Portfolio & Risk Intelligence',
             '', '**Scope:** UCI Taiwanese credit-card client sample, 2005. Historical descriptive analysis, not a contemporary underwriting model.',
             '', '## Executive summary', '',
             f"- **Clients:** {p['clients']:,}",
             f"- **Next-month defaults:** {p['defaults']:,} ({p['default_rate']:.2%})",
             f"- **Mean credit limit:** NT${p['mean_credit_limit_ntd']:,.0f}",
             f"- **Median credit limit:** NT${p['median_credit_limit_ntd']:,.0f}",
             '', '## Segmented observed default rates', '']
    for title,k in [('September repayment status','repayment_group'),('Credit limit','limit_band'),('Age','age_band')]:
        content += [f'### {title}', '', '| Segment | Clients | Defaults | Default rate |', '|---|---:|---:|---:|']
        for r in res['segments'][k]:
            content.append(f"| {r['segment']} | {r['clients']:,} | {r['defaults']:,} | {r['rate']:.2%} |")
        content.append('')
    content += ['## Data-quality checks','']
    for key,value in q.items(): content.append(f'- {key.replace("_"," ").title()}: {value:,}')
    content += ['', '## Important limits', '',
                'These are descriptive associations, not causal effects or individual-level PD forecasts.',
                'No exposure-at-default, realised loss or recovery data are available. Credit limit is not equal to drawn exposure.',
                'Raw demographic variables should not be used for discriminatory lending decisions. The data are from 2005.',
                'Repayment codes -2 and 0 occur but are not defined in the original UCI data dictionary; retain them as distinct categories.',
                '', '## Source', '',
                'Yeh, I. (2009). *Default of Credit Card Clients*. UCI Machine Learning Repository. https://doi.org/10.24432/C55S3H',
                'License: CC BY 4.0. This project relabels data fields for presentation and computes derived aggregations.']
    location.write_text('\n'.join(content)+'\n',encoding='utf-8')


def draw_plots(result: dict) -> None:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    series=result['segments']['repayment_group']
    fig,ax=plt.subplots(figsize=(8.8,4.5))
    ax.bar([r['segment'] for r in series],[r['rate']*100 for r in series])
    ax.set_ylabel('Observed default rate (%)'); ax.set_title('Default rate by September repayment status')
    ax.tick_params(axis='x',rotation=25);fig.tight_layout();fig.savefig(OUT/'default_by_repayment.png',dpi=170);plt.close(fig)
    monthly=result['monthly']
    fig,ax=plt.subplots(figsize=(8.8,4.5))
    ax.plot([r['month'] for r in monthly],[r['mean_bill_ntd'] for r in monthly],marker='o',label='Average bill')
    ax.plot([r['month'] for r in monthly],[r['mean_payment_ntd'] for r in monthly],marker='o',label='Average payment')
    ax.set_ylabel('NT$ per client');ax.set_title('Historical average billing and payment · 2005'); ax.legend();fig.tight_layout()
    fig.savefig(OUT/'billing_and_payments.png',dpi=170);plt.close(fig)


def export_full_dashboard(df: pd.DataFrame) -> None:
    """Embed only analytical fields in a self-contained interactive HTML page."""
    # Four fields per row; no client identifiers, names or sensitive contact fields.
    rows = [{'default':int(t), 'limit':float(l), 'repayment':int(r), 'age':int(a)}
            for t,l,r,a in zip(df[TARGET],df.LIMIT_BAL,df.PAY_0,df.AGE)]
    payload = json.dumps(rows,separators=(',',':')).replace('</','<\\/')
    html=(ROOT/'index.html').read_text(encoding='utf-8')
    tag=f'<script type="application/json" id="embedded-portfolio">{payload}</script>'
    html=html.replace('<script>\n(function()',tag+'\n<script>\n(function()',1)
    (OUT/'dashboard_full.html').write_text(html,encoding='utf-8')


def main() -> None:
    ap=argparse.ArgumentParser(description=__doc__)
    source=ap.add_mutually_exclusive_group(required=True)
    source.add_argument('--csv',type=Path,help='Original UCI CSV file')
    source.add_argument('--download',action='store_true',help='Fetch from official UCI archive using ucimlrepo')
    args=ap.parse_args()
    df=prepare(source_data(args.csv,args.download))
    DATA.mkdir(exist_ok=True);OUT.mkdir(exist_ok=True)
    df.to_csv(DATA/'credit_clients_clean.csv',index=False)
    with sqlite3.connect(DATA/'credit_risk.sqlite') as connection:
        add_segments(df).to_sql('credit_clients',connection,index=False,if_exists='replace')
        connection.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_credit_id ON credit_clients (ID)')
    result=analyse(df)
    (OUT/'analysis_results.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
    write_report(result,OUT/'ANALYSIS_REPORT.md')
    draw_plots(result)
    export_full_dashboard(df)
    p=result['portfolio']
    print('Analysed',f"{p['clients']:,}",'clients;',f"{p['defaults']:,}",'defaults;',f"{p['default_rate']:.2%}",'observed default rate')
    print('Outputs:',OUT.resolve())
    print('Open outputs/dashboard_full.html to explore the complete dataset offline.')

if __name__=='__main__': main()
