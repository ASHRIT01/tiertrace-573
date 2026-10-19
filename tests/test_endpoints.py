import math

from tt.eval import endpoints as E


def test_clopper_pearson_exact():
    assert abs(E.clopper_pearson_upper(0, 30) - (1 - 0.05 ** (1 / 30))) < 1e-9
    assert abs(E.clopper_pearson_upper(0, 20) - 0.1391) < 1e-3
    assert abs(E.clopper_pearson_upper(3, 30) - 0.2386) < 1e-3      # 90% two-sided CP upper limit for 3/30
    assert E.clopper_pearson_upper(5, 5) == 1.0 and math.isnan(E.clopper_pearson_upper(0, 0))


def mk(errs, n_clusters=10):
    return [(i % 10 >= errs, 0, f"f{i // n_clusters}") for i in range(100)]   # errs/10 of claims wrong


def test_h5_pass_and_fail():
    r = E.h5(mk(6), mk(3))                                     # B1 error .6, B2 error .3
    assert r["pass"] and r["ci95"][0] > 0 and abs(r["b1_minus_b2"] - 0.3) < 1e-9
    assert not E.h5(mk(3), mk(3))["pass"] and not E.h5(mk(2), mk(5))["pass"]


def test_paired_uses_same_resample():
    a = [(True, 0, "x"), (False, 0, "y")]
    d = E.paired_cluster_bootstrap(a, a, lambda p, q: E.error(p) - E.error(q))
    assert d == (0.0, 0.0, 0.0)          # identical systems: difference is exactly 0 in every resample


def test_agent_vs_b1_prints_coverage():
    agent = [(True, 3, "a"), (False, 1, "b"), (True, 3, "c"), (False, 0, "d")]
    r = E.agent_vs_b1(agent, mk(5))
    assert r["coverage"] == 0.5 and "coverage 50.0%" in r["print"]


def test_h4_reports_bound():
    rep = {"x": [{"raw": True, "verifiers_agreement": False}] * 29 + [{"raw": False, "verifiers_agreement": True}]}
    r = E.h4(rep, {"pass_if_all": {"attack_success_rate_max": 0.10}})
    assert r["pass"] and r["successes"] == 1 and r["clopper_pearson_one_sided_95_upper"] > 0.10
