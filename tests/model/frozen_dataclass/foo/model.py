from __future__ import annotations

from dataclasses import dataclass, field
from typing import ClassVar

from tests.model.frozen_dataclass.foo.bar.model_too import Type5, Type6


# fix circular import:
# from tests.model.frozen_dataclass.model import Type1, Type2


@dataclass(init=False, frozen=True)
class BaseForType3_2:
    Z: ClassVar[str] = "abc"
    o: int = field()

    def __init__(self):
        object.__setattr__(self, "o", 321)


@dataclass(init=False, frozen=True)
class BaseForBaseForType3:
    _tui: int = field()

    def __init__(self, tui=43):
        super().__init__()
        object.__setattr__(self, "_tui", tui)


@dataclass(init=False, frozen=True)
class BaseForType3_1(BaseForBaseForType3):
    X: ClassVar[int] = 12
    y: int = field()

    def __init__(self, y):
        super().__init__()
        object.__setattr__(self, "y", y)


@dataclass(init=False, frozen=True)
class Type4:
    x: int = field()
    y: dict = field()
    z: tuple = field()
    w: list = field()
    lst: list = field()
    type1: "Type1" = field(hash=False)
    type2: "Type2" = field(hash=False)
    type3: Type3 = field(hash=False)
    type5: Type5 = field(hash=False)
    type6: Type6 = field(hash=False)

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


@dataclass(init=False, frozen=True)
class Type3(BaseForType3_1, BaseForType3_2):
    _type5: Type5 = field()
    __dct: dict = field()
    type1: "Type1" = field(hash=False)
    type2: "Type2" = field(hash=False)
    type4: Type4 = field(hash=False)
    type5: Type5 = field(hash=False)
    type6: Type6 = field(hash=False)

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
