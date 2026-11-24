"""Generate the client summary and banker model for the illustrative company.

Run:  PYTHONPATH=src python scripts/make_reports.py

All company data below is hypothetical. Replace it with verified inputs before use.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from ibval import DCFInputs, build_banker_model, build_client_summary, build_football_field, value

OUT = Path(__file__).resolve().parents[1] / "docs"

COMPANY = "Example Industrials Inc. (hypothetical)"
BANK = "Shubham"

inputs = DCFInputs(
    revenue0=2_400.0,
    growth=(0.09, 0.08, 0.07, 0.06, 0.05),
    ebit_margin=0.16,
    tax_rate=0.25,
    da_pct_revenue=0.04,
    capex_pct_revenue=0.05,
    nwc_pct_revenue=0.12,
    wacc=0.09,
    terminal_growth=0.025,
    exit_multiple=10.0,
    net_debt=600.0,
    shares=120.0,
)
CURRENT_PRICE = 38.00
LTM_EBITDA = inputs.revenue0 * inputs.ebit_margin + inputs.revenue0 * inputs.da_pct_revenue
PEER_EV_EBITDA = np.array([8.2, 9.1, 9.8, 10.4, 11.0, 11.7, 12.5, 13.3])

base = value(inputs, "perpetuity")
bars = build_football_field(
    inputs,
    peer_ev_ebitda=PEER_EV_EBITDA,
    ltm_ebitda=LTM_EBITDA,
    fifty_two_week=(31.50, 44.25),
)
waccs = np.array([0.08, 0.085, 0.09, 0.095, 0.10])
growths = np.array([0.015, 0.02, 0.025, 0.03, 0.035])

OUT.mkdir(parents=True, exist_ok=True)
(OUT / "client_summary.html").write_text(
    build_client_summary(COMPANY, inputs, bars, CURRENT_PRICE, base, bank=BANK), encoding="utf-8")
(OUT / "banker_model.html").write_text(
    build_banker_model(COMPANY, inputs, base, bars, CURRENT_PRICE, waccs, growths, bank=BANK), encoding="utf-8")

print(f"base per share: {base.per_share:.2f}  EV: {base.enterprise_value:.1f}")
for b in bars:
    print(f"{b.label:<30} {b.low:8.2f} – {b.high:8.2f}")
