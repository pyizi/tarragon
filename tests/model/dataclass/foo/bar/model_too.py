from __future__ import annotations

from dataclasses import dataclass, field

from deepdiff import DeepDiff


# fix circular import:
# from tests.model.dataclass.foo.model import Type3, Type4
# from tests.model.dataclass.model import Type2, Type1


@dataclass(init=False, unsafe_hash=True, eq=False)
class Type6:
    uid: int = field()
    _name: str = field()
    type1: "Type1" = field(hash=False)
    type2: "Type2" = field(hash=False)
    type3: "Type3" = field(hash=False)
    type4: "Type4" = field(hash=False)
    type5: Type5 = field(hash=False)

    def __eq__(self, other: Type6) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self, uid, type1: "Type1", type2: "Type2", type3: "Type3", type4: "Type4", type5: Type5):
        self.uid = uid
        self._name = "say my name"
        self.type1 = type1
        self.type2 = type2
        self.type3 = type3
        self.type4 = type4
        self.type5 = type5


@dataclass(init=False, unsafe_hash=True, eq=False)
class Type5:
    __type6: Type6 = field()
    type1: "Type1" = field(hash=False)
    type2: "Type2" = field(hash=False)
    type3: "Type3" = field(hash=False)
    type4: "Type4" = field(hash=False)
    type6: Type6 = field(hash=False)

    def __eq__(self, other: Type5) -> bool:
        if type(other) is not type(self):
            return False
        else:
            return not bool(DeepDiff(self, other))

    def __init__(self, type1: "Type1", type2: "Type2", type3: "Type3", type4: "Type4", type6: Type6):
        self.__type6 = Type6(12, type1, type2, type3, type4, self)
        self.type1 = type1
        self.type2 = type2
        self.type3 = type3
        self.type4 = type4
        self.type6 = type6
