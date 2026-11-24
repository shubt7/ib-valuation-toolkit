import math

import numpy as np
import pytest

from ibval import DCFInputs, build_football_field, implied_range, project, sensitivity_per_share, value, wacc


def _inputs(**overrides):
    base = dict(
        revenue0=1000.0, growth=(0.05, 0.05, 0.05), ebit_margin=0.2, tax_rate=0.25,
        da_pct_revenue=0.04, capex_pct_revenue=0.05, nwc_pct_revenue=0.1,
        wacc=0.09, terminal_growth=0.02, exit_multiple=9.0, net_debt=500.0, shares=100.0,
    )
    base.update(overrides)
    return DCFInputs(**base)


def test_ufcf_matches_hand_calculation_year_one():
    inp = _inputs()
    p = project(inp)
    rev1 = 1000 * 1.05
    ebit1 = rev1 * 0.2
    da1 = rev1 * 0.04
    capex1 = rev1 * 0.05
    dnwc1 = rev1 * 0.1 - 1000 * 0.1
    expected = ebit1 * 0.75 + da1 - capex1 - dnwc1
    assert p.ufcf[0] == pytest.approx(expected, rel=1e-12)


def test_perpetuity_value_matches_closed_form():
    inp = _inputs()
    res = value(inp, "perpetuity")
    manual_pv = sum(res.projection.ufcf[t] / 1.09 ** (t + 1) for t in range(3))
    tv = res.projection.ufcf[-1] * 1.02 / (0.09 - 0.02)
    manual_ev = manual_pv + tv / 1.09 ** 3
    assert res.enterprise_value == pytest.approx(manual_ev, rel=1e-12)
    assert res.per_share == pytest.approx((manual_ev - 500) / 100, rel=1e-12)


def test_value_falls_as_wacc_rises():
    grid = sensitivity_per_share(_inputs(), np.array([0.08, 0.09, 0.10]), np.array([0.02]))
    assert grid[0, 0] > grid[1, 0] > grid[2, 0]


def test_wacc_must_exceed_growth():
    with pytest.raises(ValueError):
        _inputs(wacc=0.02, terminal_growth=0.03)


def test_sensitivity_marks_invalid_cells_nan():
    grid = sensitivity_per_share(_inputs(), np.array([0.02]), np.array([0.03]))
    assert math.isnan(grid[0, 0])


def test_wacc_weights():
    w = wacc(cost_equity=0.10, cost_debt=0.06, tax_rate=0.25, equity_value=600, debt=400)
    assert w == pytest.approx(0.6 * 0.10 + 0.4 * 0.06 * 0.75)


def test_implied_range_is_ordered_and_scales_with_metric():
    peers = np.array([8.0, 9.0, 10.0, 11.0, 12.0])
    r = implied_range(peers, metric=100.0)
    assert r.low <= r.mid <= r.high
    assert r.mid == pytest.approx(1000.0)


def test_implied_range_needs_three_peers():
    with pytest.raises(ValueError):
        implied_range(np.array([8.0, 9.0]), metric=100.0)


def test_football_field_bars_are_ordered():
    bars = build_football_field(
        _inputs(), peer_ev_ebitda=np.array([8, 9, 10, 11, 12.0]), ltm_ebitda=240.0,
        fifty_two_week=(20.0, 30.0),
    )
    assert len(bars) == 4
    for b in bars:
        assert b.low <= b.high
