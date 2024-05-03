from choc_expr import build_attr as build


def test_attr_build_simple_evaluation():
    assert build("val", {"val": 1}) == "1"


def test_attr_build_simple_evaluation_and_endline():
    assert build("val~", {"val": 1}) == "1\n"


def test_attr_build_empty_simple_evaluation_and_endline():
    assert build("val~", {"val": ""}) == ""


def test_attr_build_iterable_evaluation():
    assert build("$(items)", {"items": (1, 2, 3)}) == "1, 2, 3"


def test_attr_build_iterable_evaluation_and_nested_attributes():
    assert build("$(items).b.c.val", {"items": ({"b": {"c": {"val": 42}}}, {"b": {"c": {"val": 43}}}, {"b": {"c": {"val": 44}}})}) == "42, 43, 44"


def test_attr_build_nested_iterable_evaluation_and_nested_attributes():
    assert build("$(box.items).b.c.val", {"box": {"items": ({"b": {"c": {"val": 42}}}, {"b": {"c": {"val": 43}}}, {"b": {"c": {"val": 44}}})}}) == "42, 43, 44"


def test_attr_build_nested_iterable_evaluation_and_nested_attributes_and_endline():
    assert build("$(box.items).b.c.val~", {"box": {"items": ({"b": {"c": {"val": 42}}}, {"b": {"c": {"val": 43}}}, {"b": {"c": {"val": 44}}})}}) == "42, 43, 44\n"
