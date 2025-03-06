from __future__ import annotations

from typing import ClassVar

import attr
from deepdiff import DeepDiff

from tests.model.frozen_attr.foo.bar.model_too import Type5, Type6
from tests.model.frozen_attr.foo.model import Type3, Type4


@attr.define(init=False, frozen=True, slots=False, eq=False, unsafe_hash=True)
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

    def __eq__(self, other: Type2) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self, type1: Type1, type3: Type3, type4: Type4, type5: Type5, type6: Type6):
        object.__setattr__(self, "_Type2__Y", [1, True, 3])
        object.__setattr__(self, "Z", (1, 2, False))
        object.__setattr__(self, "W", {1, 2, 3, 3})
        object.__setattr__(self, "_S",
                           (Type5(type1, self, type3, type4, type6), Type6(6, type1, self, type3, type4, type5)))
        new_type4 = Type4(type1, self, type3, type5, type6)
        object.__setattr__(self, "L",
                           [Type3(type1, self, type4, type5, type6), new_type4])
        object.__setattr__(self, "_Type2__T",
                           (new_type4, Type5(type1, self, type3, type4, type6)))
        object.__setattr__(self, "type1", type1)
        object.__setattr__(self, "type3", type3)
        object.__setattr__(self, "type4", type4)
        object.__setattr__(self, "type5", type5)
        object.__setattr__(self, "type6", type6)


@attr.define(init=False, frozen=True, slots=False, eq=False, unsafe_hash=True)
class Type1:
    __x: ClassVar = 1
    _y: str = attr.field()
    __z: ClassVar[float] = 0.1

    a: int = attr.field()
    _b: str = attr.field()
    __type: Type2 = attr.field()
    __c: float = attr.field()

    def __eq__(self, other: Type1) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self, y):
        object.__setattr__(self, "_y", y)
        object.__setattr__(self, "a", 1)
        object.__setattr__(self, "_b", "2")
        object.__setattr__(self, "_Type1__type", Type2(self, None, None, None, None))
        object.__setattr__(self, "_Type1__c", 3.0)
