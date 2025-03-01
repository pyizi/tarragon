class Type6:
    def __init__(self, uid):
        self.uid = uid
        self._name = "say my name"


class Type5:
    def __init__(self):
        self.__type6 = Type6(12)
