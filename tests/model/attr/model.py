from __future__ import annotations

from typing import ClassVar

import attr

from tests.model.attr.foo.bar.model_too import Type5, Type6
from tests.model.attr.foo.model import Type3, Type4


@attr.define(init=False, unsafe_hash=True, slots=False)
class Type2:
    X: ClassVar = {"a": 1, "b": 2, "c": 3}
    D: ClassVar = {"type3": Type3(None, None, None, None, None),
                   "type4": Type4(None, None, None, None, None)}

    __Y: list = attr.field()
    Z: tuple = attr.field()
    W: set = attr.field()
    _S: tuple = attr.field()
    L: list = attr.field()
    __T: tuple = attr.field()
    type1: Type1 = attr.field(hash=False)
    type3: Type3 = attr.field(hash=False)
    type4: Type4 = attr.field(hash=False)
    type5: Type5 = attr.field(hash=False)
    type6: Type6 = attr.field(hash=False)

    def __init__(self, type1: Type1, type3: Type3, type4: Type4, type5: Type5, type6: Type6):
        self.__Y = [1, True, 3]
        self.Z = (1, 2, False)
        self.W = {1, 2, 3, 3}
        self._S = (Type5(type1, self, type3, type4, type6), Type6(6, type1, self, type3, type4, type5))
        self.L = [Type3(type1, self, type4, type5, type6), Type4(type1, self, type3, type5, type6)]
        self.__T = (Type4(type1, self, type3, type5, type6), Type5(type1, self, type3, type4, type6))
        self.type1 = type1
        self.type3 = type3
        self.type4 = type4
        self.type5 = type5
        self.type6 = type6


@attr.define(init=False, unsafe_hash=True, slots=False)
class Type1:
    __x: ClassVar = 1
    _y: str = attr.field()
    __z: ClassVar[float] = 0.1

    a: int = attr.field()
    _b: str = attr.field()
    __type: Type2 = attr.field()
    __c: float = attr.field()

    def __init__(self, y):
        self._y = y
        self.a = 1
        self._b = "2"
        self.__type = Type2(self, None, None, None, None)
        self.__c = 3.0
