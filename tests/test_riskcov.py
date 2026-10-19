from tt.eval.riskcov import aurc, cluster_bootstrap, curve, risk_at


def test_ties_give_flat_risk():
    items = [(True, 0, "a"), (False, 0, "b"), (True, 0, "c"), (False, 0, "d")]
    assert curve(items) == [0.5] * 4 and risk_at(items, 0.5) == 0.5


def test_perfect_ranking():
    items = [(True, 3, "a"), (True, 2, "b"), (False, 1, "c")]
    assert curve(items) == [0, 0, 1 / 3] and abs(aurc(items) - 1 / 9) < 1e-12


def test_bootstrap_is_deterministic():
    items = [(i % 3 == 0, 0, f"f{i % 7}") for i in range(40)]
    s = lambda it: sum(not x[0] for x in it) / len(it)
    assert cluster_bootstrap(items, s, 200) == cluster_bootstrap(items, s, 200)
