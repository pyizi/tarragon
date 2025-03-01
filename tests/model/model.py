from model.foo.bar.model_too import Type5, Type6
from model.foo.model import Type3, Type4


class Type2:
    X = {"a": 1, "b": 2, "c": 3}
    D = {"type3": Type3(), "type4": Type4()}

    def __init__(self):
        self.__Y = [1, True, 3]
        self.Z = (1, 2, False)
        self.W = {1, 2, 3, 3}
        self._S = {Type5(), Type6(6)}
        self.L = [Type3(), Type4()]
        self.__T = (Type4(), Type5())


class Type1:
    __x = 1
    _y: str
    __z: float = 0.1

    def __init__(self, y):
        self._y = y
        self.a = 1
        self._b = "2"
        self.__type = Type2()
        self.__c = 3.0
