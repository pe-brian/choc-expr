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
    def eval_conditions(obj: Any, expr: str) -> str:
        regex = r"(@{([A-Za-z_.$()=]+)}:([{}A-Za-z_.$()\s*~]*):([{}A-Za-z_.$()\s*~]*);)"
        matches = re.findall(regex, expr)
        to_replace = {cond: cond_attr_if_true if to_bool(Attr(expr=cond_attr, obj=obj, ).build()) else cond_attr_if_false for cond, cond_attr, cond_attr_if_true, cond_attr_if_false in matches}
        for cond, replacement in to_replace.items():
            expr = expr.replace(cond, replacement)
        return expr

    def eval_attributes(self, expr: str) -> str:
        if not self.buildable:
            return ""
        regex = r"{([A-Za-z_.$()~]+)}"
        to_replace = [key for key in re.findall(regex, expr)]
        for key in to_replace:
            expr = expr.replace(f"{{{key}}}", Attr(expr=key, obj=self._ref, list_join_sep=self.list_join_sep).build())
        return expr

    def build(self) -> str:
        expr = self.eval_attributes(Expr.eval_conditions(self._ref, self._expr))
        expr = expr.replace("~", "\n")
        expr = expr.replace("\n\n", "\n")
        if self.compact:
            expr = expr.replace("\n", " ")
            expr = expr.strip()
        return expr


def build_expr(*args, **kwargs):
    return Expr(*args, **kwargs).build()
