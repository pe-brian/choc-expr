from choc_expr import build_attr as build


def test_attr_attr():
    assert build("val", {"val": 1}) == "1"
    assert build("$(items)", {"items": (1, 2, 3)}) == "1, 2, 3"
    assert build("$(items).b.c.val", {"items": ({"b": {"c": {"val": 42}}}, {"b": {"c": {"val": 43}}}, {"b": {"c": {"val": 44}}})}) == "42, 43, 44"
    assert build("$(box.items).b.c.val", {"box": {"items": ({"b": {"c": {"val": 42}}}, {"b": {"c": {"val": 43}}}, {"b": {"c": {"val": 44}}})}}) == "42, 43, 44"
    assert build("$(box.items).b.c.val~", {"box": {"items": ({"b": {"c": {"val": 42}}}, {"b": {"c": {"val": 43}}}, {"b": {"c": {"val": 44}}})}}) == "42, 43, 44\n"


def test_attr_attr_endline():
    assert build("val~", {"val": 1}) == "1\n"


def test_attr_attr_empty_endline():
    assert build("val~", {"val": ""}) == ""
