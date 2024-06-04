import pytest

from choc_expr import build_expr as build, inline_obj as _, Expr


def test_expr_build_without_init_params_must_return_empty_string():
    assert build() == ""


def test_expr_build_without_interpolation_must_return_original_string():
    assert build("NOTHING") == "NOTHING"


def test_expr_separator_characters_must_be_interpreted():
    assert build("1~1", compact=True) == "1 1"
    assert build("1~1", compact=False) == "1\n1"


def test_expr_build_must_interpolate_value_from_dict():
    assert build("SOMETHING {value}", {"value": 1}) == "SOMETHING 1"


def test_expr_build_must_interpolate_value_from_object():
    assert build("SOMETHING {value}", _(value=1)) == "SOMETHING 1"


def test_expr_build_must_interpolate_value_from_nested_objects_or_dicts():
    assert build("SOMETHING {value.a}", _(value=_(a=1))) == "SOMETHING 1"
    assert build("SOMETHING {value.a}", {"value": _(a=1)}) == "SOMETHING 1"
    assert build("SOMETHING {value.a}", {"value": {"a": 1}}) == "SOMETHING 1"
    assert build("SOMETHING {value.a}", _(value={"a": 1})) == "SOMETHING 1"


def test_expr_build_loop_must_return_joined_iterable_values():
    assert build("{$(values)}", {"values": (1, 2, 3)}) == "1, 2, 3"


def test_expr_build_loop_must_return_joined_iterable_values_and_apply_attribute():
    assert build("{$(values).value}", {"values": ({"value": 1}, {"value": 2}, {"value": 3})}) == "1, 2, 3"


def test_expr_readme_example():
    assert build("Kevin is @{age}>=18:an adult:a child; of {age} years old", {"age": 24}) == "Kevin is an adult of 24 years old"


def test_expr_build_condition_true_must_keep_the_then_value_only():
    assert build("@{cond}:{then_val}:{else_val};", {"cond": True, "then_val": 1, "else_val": 2}) == "1"


def test_expr_build_condition_false_must_keep_the_else_value_only():
    assert build("@{cond}:{then_val}:{else_val};", {"cond": False, "then_val": 1, "else_val": 2}) == "2"


def test_expr_build_condition_none_must_keep_the_else_value_only():
    assert build("@{cond}:{then_val}:{else_val};", {"cond": None, "then_val": 1, "else_val": 2}) == "2"


def test_expr_build_condition_true_must_evaluate_the_then_value_only():
    try:
        build("@{cond}::{obj.error};", {"cond": True, "obj": {"error": property(lambda self: 1/0)}})
    except ZeroDivisionError:
        pytest.fail()


def test_expr_build_condition_false_must_evaluate_the_else_value_only():
    try:
        build("@{cond}:{obj.error}:;", {"cond": False, "obj": {"error": property(lambda self: 1/0)}})
    except ZeroDivisionError:
        pytest.fail()


def test_expr_build_not_buildable_expr_must_not_be_evaluated_nor_interpolated():
    assert build("{not_buildable_expr}1", {"not_buildable_expr": _(buildable=property(lambda self: False), build=(lambda self: "b"), __str__=lambda self: "")}) == "1"


def test_expr_build_not_buildable_expr_with_separator_must_not_be_evaluated_nor_interpolated():
    assert build("{not_buildable_expr~}1", {"not_buildable_expr": _(buildable=property(lambda self: False), build=(lambda self: "b"), __str__=lambda self: "")}) == "1"


def test_expr_double_separator_characters_must_be_removed():
    assert build("1~~1") == "1 1"
    assert build("1~~1", compact=False) == "1\n1"


def test_expr_leading_and_ending_separator_must_be_removed():
    assert build(" 1 ") == "1"
    assert build("\n1\n") == "1"


def test_expr_build_buildable_expr_with_separator_must_keep_seperator():
    assert build("{buildable_expr~}1", {"buildable_expr": 1}) == "1 1"
    assert build("{buildable_expr~}1", {"buildable_expr": 1}, compact=False) == "1\n1"


def test_expr_eval_condition_interpolation():
   assert Expr.eval_condition(_(var=True), "{var}", "1", "2") == "1"
   assert Expr.eval_condition(_(var=False), "{var}", "1", "2") == "2"
   assert Expr.eval_condition(_(var=25), "{var}==25", "1", "2") == "1"


def test_expr_eval_condition():
   assert Expr.eval_condition(None, "25==25", "1", "2") == "1"
   assert Expr.eval_condition(None, "25!=25", "1", "2") == "2"
   assert Expr.eval_condition(None, "25>=25", "1", "2") == "1"
   assert Expr.eval_condition(None, "25<=25", "1", "2") == "1"
   assert Expr.eval_condition(None, "25<25", "1", "2") == "2"
   assert Expr.eval_condition(None, "25>25", "1", "2") == "2"
   assert Expr.eval_condition(None, "True", "1", "2") == "1"
   assert Expr.eval_condition(None, "False", "1", "2") == "2"


def test_expr_build_then_or_else_empty():
    assert build("@False::2;", {}) == "2"
    assert build("@True:1:;", {}) == "1"
