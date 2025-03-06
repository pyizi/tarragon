from __future__ import annotations

from typing import ClassVar

import attr
from deepdiff import DeepDiff

from tests.model.frozen_attr.foo.bar.model_too import Type5, Type6


# fix circular import:
# from tests.model.frozen_attr.model import Type1, Type2


@attr.define(init=False, frozen=True, slots=False, eq=False, unsafe_hash=True)
class BaseForType3_2:
    Z: ClassVar[str] = "abc"
    o: int = attr.field()

    def __eq__(self, other: BaseForType3_2) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self):
        object.__setattr__(self, "o", 321)


@attr.define(init=False, frozen=True, slots=False, eq=False, unsafe_hash=True)
class BaseForBaseForType3:
    _tui: int = attr.field()

    def __eq__(self, other: BaseForBaseForType3) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self, tui=43):
        super().__init__()
        object.__setattr__(self, "_tui", tui)


@attr.define(init=False, frozen=True, slots=False, eq=False, unsafe_hash=True)
class BaseForType3_1(BaseForBaseForType3):
    X: ClassVar[int] = 12
    y: int = attr.field()

    def __eq__(self, other: BaseForType3_1) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self, y):
        super().__init__()
        object.__setattr__(self, "y", y)


@attr.define(init=False, frozen=True, slots=False, eq=False, unsafe_hash=True)
class Type4:
    x: int = attr.field()
    y: dict = attr.field()
    z: tuple = attr.field()
    w: list = attr.field()
    lst: list = attr.field()
    type1: "Type1" = attr.field(hash=False)
    type2: "Type2" = attr.field(hash=False)
    type3: Type3 = attr.field(hash=False)
    type5: Type5 = attr.field(hash=False)
    type6: Type6 = attr.field(hash=False)

    def __eq__(self, other: Type4) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self, type1: "Type1", type2: "Type2", type3: Type3, type5: Type5, type6: Type6):
        object.__setattr__(self, "x", 7)
        object.__setattr__(self, "y", dict(a="a", b=Type5(type1, type2, type3, self, type6), c="c"))
        object.__setattr__(self, "z", tuple([1, 2, 3]))
        object.__setattr__(self, "w", [1, Type6(123, type1, type2, type3, self, type5), 3, 3])
        object.__setattr__(self, "lst", list(range(3)))
        object.__setattr__(self, "type1", type1)
        object.__setattr__(self, "type2", type2)
        object.__setattr__(self, "type3", type3)
        object.__setattr__(self, "type5", type5)
        object.__setattr__(self, "type6", type6)


@attr.define(init=False, frozen=True, slots=False, eq=False, unsafe_hash=True)
class Type3(BaseForType3_1, BaseForType3_2):
    _type5: Type5 = attr.field(
        init=False)  # init=False - in order for "attrs" not to consider names "_type5" and "type5" equal.
    __dct: dict = attr.field()
    type1: "Type1" = attr.field(hash=False)
    type2: "Type2" = attr.field(hash=False)
    type4: Type4 = attr.field(hash=False)
    type5: Type5 = attr.field(hash=False)
    type6: Type6 = attr.field(hash=False)

    def __eq__(self, other: Type3) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self, type1: "Type1", type2: "Type2", type4: Type4, type5: Type5, type6: Type6):
        super().__init__(45)
        object.__setattr__(self, "_type5", Type5(type1, type2, self, type4, type6))
        object.__setattr__(self, "_Type3__dct",
                           {Type5(type1, type2, self, type4, type6): "3",
                            Type6(7, type1, type2, self, type4, type5): Type4(type1, type2, self, type5, type6)})
        object.__setattr__(self, "type1", type1)
        object.__setattr__(self, "type2", type2)
        object.__setattr__(self, "type4", type4)
        object.__setattr__(self, "type5", type5)
        object.__setattr__(self, "type6", type6)
