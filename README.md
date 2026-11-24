# ib-valuation-toolkit

An investment banking valuation toolkit by **Shubham**: a DCF model, trading comparables, a football-field summary of valuation ranges, and two reports generated from the same inputs.

- **Client summary**: a plain-English valuation range and takeaways, with a football-field chart and the current price marked.
- **Banker model**: assumptions, projections, the enterprise-to-equity bridge, a WACC × terminal-growth sensitivity grid, and the football field.
- **Dashboard**: an index page that links the two reports and shows the headline numbers.

> All company data in this repo is **hypothetical**. The outputs are illustrative and are not investment advice, a fairness opinion, or a recommendation to buy or sell any security. Verify every input against filings and market data before use.

## Quick start

```bash
pip install -e ".[dev]"
pytest -q                                   # 9 tests
PYTHONPATH=src python scripts/make_reports.py   # writes docs/index.html and the two reports
```

Requires Python 3.10+ and NumPy.

## What's inside

| Module | Purpose |
|---|---|
| `ibval/dcf.py` | Unlevered FCF projection, DCF with perpetuity or exit-multiple terminal value, WACC, sensitivity grid |
| `ibval/comps.py` | Implied valuation from the interquartile range of peer multiples |
| `ibval/football_field.py` | Per-share ranges across methods, with sensitivity bands |
| `ibval/report.py` | Self-contained HTML reports (inline SVG and CSS, no external assets) |

## Method

- Unlevered FCF = EBIT × (1 − tax) + D&A − capex − Δ net working capital.
- Cash flows are end-of-year and discounted at WACC.
- Terminal value uses either Gordon growth on the final-year FCF or an exit multiple on final-year EBITDA.
- Equity value = enterprise value − net debt. Per-share value divides by diluted shares.
- Football-field DCF bars flex WACC and terminal growth (or the exit multiple) around the base case.

## Viewing the reports

The reports are plain HTML in `docs/`. GitHub shows that folder as source code. To view the pages rendered, enable GitHub Pages for this repo (Settings → Pages → `main` branch, `/docs` folder), or open the files locally.

## Replacing the sample data

Edit the `inputs`, `CURRENT_PRICE`, `PEER_EV_EBITDA`, and `COMPANY` values in `scripts/make_reports.py`. Everything else is driven by those inputs.

## License

MIT. © Shubham
