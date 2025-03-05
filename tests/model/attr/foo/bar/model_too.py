from __future__ import annotations

import attr


# fix circular import:
# from tests.model.attr.foo.model import Type3, Type4
# from tests.model.attr.model import Type2, Type1


@attr.define(init=False, unsafe_hash=True, slots=False)
class Type6:
    uid: int = attr.field()
    _name: str = attr.field()
    type1: "Type1" = attr.field(hash=False)
    type2: "Type2" = attr.field(hash=False)
    type3: "Type3" = attr.field(hash=False)
    type4: "Type4" = attr.field(hash=False)
    type5: Type5 = attr.field(hash=False)

    def __init__(self, uid, type1: "Type1", type2: "Type2", type3: "Type3", type4: "Type4", type5: Type5):
        self.uid = uid
        self._name = "say my name"
        self.type1 = type1
        self.type2 = type2
        self.type3 = type3
        self.type4 = type4
        self.type5 = type5


@attr.define(init=False, unsafe_hash=True, slots=False)
class Type5:
    __type6: Type6 = attr.field()
    type1: "Type1" = attr.field(hash=False)
    type2: "Type2" = attr.field(hash=False)
    type3: "Type3" = attr.field(hash=False)
    type4: "Type4" = attr.field(hash=False)
    type6: Type6 = attr.field(hash=False)

    def __init__(self, type1: "Type1", type2: "Type2", type3: "Type3", type4: "Type4", type6: Type6):
        self.__type6 = Type6(12, type1, type2, type3, type4, self)
        self.type1 = type1
        self.type2 = type2
        self.type3 = type3
        self.type4 = type4
        self.type6 = type6
