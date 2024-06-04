import re
from typing import Any

from typeguard import typechecked

from .utils import inline_obj, to_bool
from .attr import Attr


@typechecked
class Expr:

    def __init__(
        self,
        choc_expr: str | None = None,
        ref: Any = None,
        list_join_sep: str = ", ",
        compact: bool = True
    ) -> None:
        if isinstance(ref, dict):
            ref = inline_obj(**ref)
        self._ref = ref or self
        self._expr = choc_expr or ""
        self.list_join_sep = list_join_sep
        self.compact = compact

    @property
    def buildable(self):
        return True

    def __str__(self) -> str:
        return self.build()

    def __expr__(self) -> str:
        return self.build()

    @property
    def list_join_sep(self) -> str:
        return self._list_join_sep

    @list_join_sep.setter
    def list_join_sep(self, value: str) -> None:
        self._list_join_sep = value

    @property
    def compact(self) -> bool:
        return self._compact

    @compact.setter
    def compact(self, value: bool) -> None:
        self._compact = value

    @staticmethod
    def resolve_condition(left_operand: Any, operator: str, right_operand: Any) -> bool:
        """"""
        match operator:
            case "==":
                return left_operand == right_operand
            case "!=":
                return left_operand != right_operand
            case ">=":
                return left_operand >= right_operand
            case "<=":
                return left_operand <= right_operand
            case ">":
                return left_operand > right_operand
            case "<":
                return left_operand < right_operand
            case '':
                return to_bool(left_operand)


    @staticmethod
    def eval_condition(obj: Any, cond_expr: str, then_expr: str, else_expr: str) -> str:
        """"""
        # interpolate value of condition expression
        for match in re.findall(r"{[.\w]+}", cond_expr):
            cond_expr = cond_expr.replace(match, Attr(expr=match[1:-1], obj=obj).build())
        # resolve condition
        matches = re.findall(r"([A-Za-z0-9._]+|True|False)(?:(==|>=|<=|>|<|!=)([A-Za-z0-9._]+|True|False))?", cond_expr)
        if len(matches) == 1:
            return then_expr if Expr.resolve_condition(*matches[0]) else else_expr
        raise ValueError("Cannot resolve condition")
    


    @staticmethod
    def eval_conditions(obj: Any, expr: str) -> str:
        """"""
        matches = re.findall(r"(@([^:;\s]+):([^:;]*):([^:;]*);)", expr)
        for match, cond_expr, then_expr, else_expr in matches:
            expr = expr.replace(match, Expr.eval_condition(obj, cond_expr, then_expr, else_expr))
        return expr

    def eval_attributes(self, expr: str) -> str:
        """"""
        if not self.buildable:
            return ""
        regex = r"{([A-Za-z_.$()~]+)}"
        to_replace = [key for key in re.findall(regex, expr)]
        for key in to_replace:
            expr = expr.replace(f"{{{key}}}", Attr(expr=key, obj=self._ref, list_join_sep=self.list_join_sep).build())
        return expr

    def build(self) -> str:
        """"""
        expr = self.eval_attributes(Expr.eval_conditions(self._ref, self._expr))
        expr = expr.replace("~", "\n")
        expr = expr.replace("\n\n", "\n")
        if self.compact:
            expr = expr.replace("\n", " ")
            expr = expr.strip()
        return expr


def build_expr(*args, **kwargs):
    """"""
    return Expr(*args, **kwargs).build()
