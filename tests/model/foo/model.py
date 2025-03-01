from tests.model.foo.bar.model_too import Type5, Type6


class Type4:
    def __init__(self):
        self.x: int = 7
        self.y = dict(a="a", b=Type5(), c="c")
        self.z = tuple([1, 2, 3])
        self.w = set([1, Type6(123), 3, 3])
        self.lst: list = list(range(3))


class Type3:
    type6: Type6

    def __init__(self):
        self.type5 = Type5()
        self.__dct = {Type5(): "3", Type6(7): Type4()}
