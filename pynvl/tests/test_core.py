from src.core import decode, nvl, sign


def test_nvl():
    assert nvl(expr=None, default=5) == 5
    assert nvl(expr=10, default=5) == 10


def test_decode_basic_pairs():
    assert decode("A", "A","Alpha","B","Beta") == "Alpha"
    assert decode("B", "A","Alpha","B","Beta") == "Beta"


def test_decode_implicit_default():
    assert decode("Z", "A","Alpha","B","Beta","Unknown") == "Unknown"


def test_decode_explicit_default_overrides_implicit():
    assert decode("Z", "A","Alpha","B","Beta","X", default="Y") == "Y"


def test_decode_no_pairs_returns_none_or_explicit_default():
    assert decode("A") is None
    assert decode("A", default="D") == "D"


def test_decode_none_equals_none():
    assert decode(None, None, "N/A", "Should not see") == "N/A"
    assert decode(None, "X", "other", default="nope") == "nope"


def test_sign():
    assert sign(n=-5) == -1
    assert sign(n=0) == 0
    assert sign(n=9) == 1
