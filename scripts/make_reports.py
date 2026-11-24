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

index = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Valuation dashboard</title>
<style>body{{font:15px/1.55 system-ui,sans-serif;margin:0;padding:32px;background:#fff;color:#1d1d1f}}
main{{max-width:900px;margin:0 auto}}h1{{font-size:26px;margin:0 0 4px}}.sub{{color:#6e6e73;margin-bottom:20px}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin-bottom:24px}}
.kpi{{background:#f5f5f7;border-radius:12px;padding:16px 18px}}.kpi .v{{font-size:24px;font-weight:600}}.kpi .l{{color:#6e6e73;font-size:13px}}
.links a{{display:block;background:#f5f5f7;border-radius:12px;padding:16px 18px;margin-bottom:12px;color:#0b3d91;text-decoration:none;font-weight:600}}
.links span{{display:block;color:#6e6e73;font-weight:400;font-size:13px}}
@media (prefers-color-scheme: dark){{body{{background:#111;color:#f2f2f2}}.kpi,.links a{{background:#1c1c1e}}.sub,.kpi .l,.links span{{color:#9a9aa0}}.links a{{color:#7fb2ff}}}}
</style></head><body><main>
<h1>{COMPANY}: valuation dashboard</h1>
<div class="sub">Illustrative analysis on hypothetical inputs · prepared by {BANK}</div>
<div class="kpis">
  <div class="kpi"><div class="v">${base.per_share:,.2f}</div><div class="l">Base-case value per share</div></div>
  <div class="kpi"><div class="v">${CURRENT_PRICE:,.2f}</div><div class="l">Current share price</div></div>
  <div class="kpi"><div class="v">{base.per_share / CURRENT_PRICE - 1:+.0%}</div><div class="l">Base case vs. current</div></div>
  <div class="kpi"><div class="v">{base.terminal_share_of_ev:.0%}</div><div class="l">Value in terminal period</div></div>
</div>
<div class="links">
  <a href="client_summary.html">Client summary<span>Plain-English valuation range and takeaways</span></a>
  <a href="banker_model.html">Banker model<span>Assumptions, projections, DCF bridge, sensitivity grid</span></a>
</div>
<div class="sub">Not investment advice, a fairness opinion, or a recommendation to buy or sell any security.</div>
</main></body></html>"""
(OUT / "index.html").write_text(index, encoding="utf-8")

print(f"base per share: {base.per_share:.2f}  EV: {base.enterprise_value:.1f}")
for b in bars:
    print(f"{b.label:<30} {b.low:8.2f} – {b.high:8.2f}")
