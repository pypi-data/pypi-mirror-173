import re
from typing import Generator, List, Type

from pydantic import BaseModel

from redacted.info_types import InfoType


class Match(BaseModel):
    text: str
    start: int
    end: int
    len: int
    type: Type[InfoType]


class AnonymisedText(BaseModel):
    original: str
    text: str
    matches: List[Match]
    info_types: List[Type[InfoType]]


class Anonymiser:
    expr: re.Pattern
    _expr_string: str

    def __init__(self, info_types: List[Type[InfoType]]):
        self.info_types = info_types
        self._info_types_dict = dict(zip(map(lambda x: x.name, self.info_types), self.info_types))
        self._make_search_expr()

    def _make_search_expr(self) -> re.Pattern:
        self._expr_string = '|'.join(rf'(?P<{t.name}>\b{t.expr})\b' for t in self.info_types)
        self.expr = re.compile(self._expr_string)
        return self.expr

    def get_matches(self, text: str) -> Generator:
        mo = self.expr.search(text)
        while mo is not None:
            typ = mo.lastgroup
            val = mo.group(typ)  # type: ignore
            yield Match(
                text=val,
                start=mo.start(),
                end=mo.end(),
                len=len(val),
                type=self._info_types_dict[typ],  # type: ignore
            )
            mo = self.expr.search(text, mo.end())

    @staticmethod
    def anonymise_text(text: str, matches: List[Match]) -> str:
        _new_text = text
        for match in matches:
            _new_text = _new_text.replace(match.text, match.type.generate())
        return _new_text

    def anonymise(self, text: str):
        matches = [match for match in self.get_matches(text)]
        anonymised_text = self.anonymise_text(text, matches)
        return AnonymisedText(original=text, text=anonymised_text, matches=matches, info_types=self.info_types)
