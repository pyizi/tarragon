from __future__ import annotations

from deepdiff import DeepDiff

from tests.model.vanilla.foo.bar.model_too import Type5, Type6
from tests.model.vanilla.foo.model import Type3, Type4


class Type2:
    X = {"a": 1, "b": 2, "c": 3}
    D = {"type3": Type3(None, None, None, None, None),
         "type4": Type4(None, None, None, None, None)}

    def __eq__(self, other: Type2) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    __hash__ = object.__hash__

    def __init__(self, type1: Type1, type3: Type3, type4: Type4, type5: Type5, type6: Type6):
        self.__Y = [1, True, 3]
        self.Z = (1, 2, False)
        self.W = {1, 2, 3, 3}
        self._S = (Type5(type1, self, type3, type4, type6), Type6(6, type1, self, type3, type4, type5))
        new_type4 = Type4(type1, self, type3, type5, type6)
        self.L = [Type3(type1, self, type4, type5, type6), new_type4]
        self.__T = (new_type4, Type5(type1, self, type3, type4, type6))
        self.type1 = type1
        self.type3 = type3
        self.type4 = type4
        self.type5 = type5
        self.type6 = type6


class Type1:
    __x = 1
    _y: str
    __z: float = 0.1

    def __eq__(self, other: Type1) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    __hash__ = object.__hash__

    def __init__(self, y):
        self._y = y
        self.a = 1
        self._b = "2"
        self.__type = Type2(self, None, None, None, None)
        self.__c = 3.0
