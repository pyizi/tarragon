from __future__ import annotations

from deepdiff import DeepDiff

from tests.model.vanilla.foo.bar.model_too import Type5, Type6


# fix circular import:
# from tests.model.vanilla.model import Type1, Type2


class BaseForType3_2:
    Z: str = "abc"

    def __eq__(self, other: BaseForType3_2) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    __hash__ = object.__hash__

    def __init__(self):
        self.o = 321


class BaseForBaseForType3:

    def __eq__(self, other: BaseForBaseForType3) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    __hash__ = object.__hash__

    def __init__(self, tui=43):
        super().__init__()
        self._tui = tui


class BaseForType3_1(BaseForBaseForType3):
    X: int = 12

    def __eq__(self, other: BaseForType3_1) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    __hash__ = object.__hash__

    def __init__(self, y):
        super().__init__()
        self.y = y


class Type4:

    def __eq__(self, other: Type4) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    __hash__ = object.__hash__

    def __init__(self, type1: "Type1", type2: "Type2", type3: Type3, type5: Type5, type6: Type6):
        self.x: int = 7
        self.y = dict(a="a", b=Type5(type1, type2, type3, self, type6), c="c")
        self.z = tuple([1, 2, 3])
        self.w = [1, Type6(123, type1, type2, type3, self, type5), 3, 3]
        self.lst: list = list(range(3))
        self.type1 = type1
        self.type2 = type2
        self.type3 = type3
        self.type5 = type5
        self.type6 = type6


class Type3(BaseForType3_1, BaseForType3_2):
    type6: Type6

    def __eq__(self, other: Type3) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    __hash__ = object.__hash__

    def __init__(self, type1: "Type1", type2: "Type2", type4: Type4, type5: Type5, type6: Type6):
        super().__init__(45)
        self._type5 = Type5(type1, type2, self, type4, type6)
        self.__dct = {Type5(type1, type2, self, type4, type6): "3",
                      Type6(7, type1, type2, self, type4, type5): Type4(type1, type2, self, type5, type6)}
        self.type1 = type1
        self.type2 = type2
        self.type4 = type4
        self.type5 = type5
        self.type6 = type6
