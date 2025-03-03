from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generator


def next_id(start_id: int = 0) -> Generator[int, None, None]:
    while True:
        yield start_id
        start_id += 1


class __BaseTypeRepresentation(ABC):
    def __init__(self, next_id_generator: Generator[int, None, None]):
        self.__already_called = False
        self._current_id = None
        self._next_id_generator = next_id_generator

    @staticmethod
    def _get_type_representation(type_representation: __BaseTypeRepresentation | None) -> str:
        return "null" if type_representation is None else type_representation()

    @abstractmethod
    def _get_self_representation(self) -> str:
        pass

    def __call__(self) -> str:
        if not self.__already_called:
            self.__already_called = True
            self._current_id = next(self._next_id_generator)
            return self._get_self_representation()
        else:
            return f'{{ "ref_id": {self._current_id} }}'


class Type6Representation(__BaseTypeRepresentation):
    def __init__(self, uid: int,
                 type1_representation: Type1Representation | None,
                 type2_representation: Type2Representation | None,
                 type3_representation: Type3Representation | None,
                 type4_representation: Type4Representation | None,
                 type5_representation: Type5Representation | None,
                 next_id_generator: Generator[int, None, None]):
        super().__init__(next_id_generator)
        self.__uid = uid
        self.__type1_representation = type1_representation
        self.__type2_representation = type2_representation
        self.__type3_representation = type3_representation
        self.__type4_representation = type4_representation
        self.__type5_representation = type5_representation

    def _get_self_representation(self) -> str:
        return f"""{{
            "type": "tests.model.foo.bar.model_too.Type6",
            "id": {self._current_id},
            "object": {{
                "uid": {self.__uid},
                "_name": "say my name",
                "type1": {self._get_type_representation(self.__type1_representation)},
                "type2": {self._get_type_representation(self.__type2_representation)},
                "type3": {self._get_type_representation(self.__type3_representation)},
                "type4": {self._get_type_representation(self.__type4_representation)},
                "type5": {self._get_type_representation(self.__type5_representation)}
            }}
        }}"""


class Type5Representation(__BaseTypeRepresentation):
    def __init__(self,
                 type1_representation: Type1Representation | None,
                 type2_representation: Type2Representation | None,
                 type3_representation: Type3Representation | None,
                 type4_representation: Type4Representation | None,
                 type6_representation: Type6Representation | None,
                 next_id_generator: Generator[int, None, None]):
        super().__init__(next_id_generator)
        self.__type1_representation = type1_representation
        self.__type2_representation = type2_representation
        self.__type3_representation = type3_representation
        self.__type4_representation = type4_representation
        self.__type6_representation = type6_representation
        self.____type6_representation = Type6Representation(12,
                                                            type1_representation,
                                                            type2_representation,
                                                            type3_representation,
                                                            type4_representation,
                                                            self,
                                                            next_id_generator)

    def _get_self_representation(self) -> str:
        return f"""{{
            "type": "tests.model.foo.bar.model_too.Type5",
            "id": {self._current_id},
            "object": {{
                "_Type5__type6": {self.____type6_representation()},
                "type1": {self._get_type_representation(self.__type1_representation)},
                "type2": {self._get_type_representation(self.__type2_representation)},
                "type3": {self._get_type_representation(self.__type3_representation)},
                "type4": {self._get_type_representation(self.__type4_representation)},
                "type6": {self._get_type_representation(self.__type6_representation)}
            }}
        }}"""


class Type4Representation(__BaseTypeRepresentation):
    def __init__(self,
                 type1_representation: Type1Representation | None,
                 type2_representation: Type2Representation | None,
                 type3_representation: Type3Representation | None,
                 type5_representation: Type5Representation | None,
                 type6_representation: Type6Representation | None,
                 next_id_generator: Generator[int, None, None]):
        super().__init__(next_id_generator)
        self.__type1_representation = type1_representation
        self.__type2_representation = type2_representation
        self.__type3_representation = type3_representation
        self.__type5_representation = type5_representation
        self.__type6_representation = type6_representation
        self.____type5_representation = Type5Representation(type1_representation,
                                                            type2_representation,
                                                            type3_representation,
                                                            self,
                                                            type6_representation,
                                                            next_id_generator)
        self.____type6_representation = Type6Representation(123,
                                                            type1_representation,
                                                            type2_representation,
                                                            type3_representation,
                                                            self,
                                                            type5_representation,
                                                            next_id_generator)

    def _get_self_representation(self) -> str:
        return f"""{{
            "type": "tests.model.foo.model.Type4",
            "id": {self._current_id},
            "object": {{
                "x": 7,
                "y": {{
                    "type": "dict",
                    "id": {next(self._next_id_generator)},
                    "items": [
                        {{
                            "key": "a",
                            "value": "a"
                        }},
                        {{
                            "key": "b",
                            "value": {self.____type5_representation()}
                        }},
                        {{
                            "key": "c",
                            "value": "c"
                        }}
                    ]
                }},
                "z": {{
                    "type": "tuple",
                    "id": {next(self._next_id_generator)},
                    "array": [1, 2, 3]
                }},
                "w": {{
                    "type": "list",
                    "id": {next(self._next_id_generator)},
                    "array": [
                        1, 
                        {self.____type6_representation()}, 
                        3,
                        3
                    ]
                }},
                "lst": {{
                    "type": "list",
                    "id": {next(self._next_id_generator)},
                    "array": [0, 1, 2]
                }},
                "type1": {self._get_type_representation(self.__type1_representation)},
                "type2": {self._get_type_representation(self.__type2_representation)},
                "type3": {self._get_type_representation(self.__type3_representation)},
                "type5": {self._get_type_representation(self.__type5_representation)},
                "type6": {self._get_type_representation(self.__type6_representation)}
            }}
        }}"""


class Type3Representation(__BaseTypeRepresentation):
    def __init__(self,
                 type1_representation: Type1Representation | None,
                 type2_representation: Type2Representation | None,
                 type4_representation: Type4Representation | None,
                 type5_representation: Type5Representation | None,
                 type6_representation: Type6Representation | None,
                 next_id_generator: Generator[int, None, None]):
        super().__init__(next_id_generator)
        self.__type1_representation = type1_representation
        self.__type2_representation = type2_representation
        self.__type4_representation = type4_representation
        self.__type5_representation = type5_representation
        self.__type6_representation = type6_representation
        self.____type5_representation1 = Type5Representation(type1_representation,
                                                             type2_representation,
                                                             self,
                                                             type4_representation,
                                                             type6_representation,
                                                             next_id_generator)
        self.____type5_representation2 = Type5Representation(type1_representation,
                                                             type2_representation,
                                                             self,
                                                             type4_representation,
                                                             type6_representation,
                                                             next_id_generator)
        self.____type6_representation = Type6Representation(7,
                                                            type1_representation,
                                                            type2_representation,
                                                            self,
                                                            type4_representation,
                                                            type5_representation,
                                                            next_id_generator)
        self.____type4_representation = Type4Representation(type1_representation,
                                                            type2_representation,
                                                            self,
                                                            type5_representation,
                                                            type6_representation,
                                                            next_id_generator)

    def _get_self_representation(self) -> str:
        return f"""{{
            "type": "tests.model.foo.model.Type3",
            "id": {self._current_id},
            "object": {{
                "o": 321,
                "_tui": 43,
                "y": 45,
                "_type5": {self.____type5_representation1()},
                "_Type3__dct": {{
                    "type": "dict",
                    "id": {next(self._next_id_generator)},
                    "items": [
                        {{
                            "key": {self.____type5_representation2()},
                            "value": "3"
                        }},
                        {{
                            "key": {self.____type6_representation()},
                            "value": {self.____type4_representation()}
                        }}
                    ]
                }},
                "type1": {self._get_type_representation(self.__type1_representation)},
                "type2": {self._get_type_representation(self.__type2_representation)},
                "type4": {self._get_type_representation(self.__type4_representation)},
                "type5": {self._get_type_representation(self.__type5_representation)},
                "type6": {self._get_type_representation(self.__type6_representation)}
            }}
        }}"""


class Type2Representation(__BaseTypeRepresentation):
    def __init__(self,
                 type1_representation: Type1Representation | None,
                 type3_representation: Type3Representation | None,
                 type4_representation: Type4Representation | None,
                 type5_representation: Type5Representation | None,
                 type6_representation: Type6Representation | None,
                 next_id_generator: Generator[int, None, None]):
        super().__init__(next_id_generator)
        self.__type1_representation = type1_representation
        self.__type3_representation = type3_representation
        self.__type4_representation = type4_representation
        self.__type5_representation = type5_representation
        self.__type6_representation = type6_representation
        self.____type5_representation1 = Type5Representation(type1_representation,
                                                             self,
                                                             type3_representation,
                                                             type4_representation,
                                                             type6_representation,
                                                             next_id_generator)
        self.____type5_representation2 = Type5Representation(type1_representation,
                                                             self,
                                                             type3_representation,
                                                             type4_representation,
                                                             type6_representation,
                                                             next_id_generator)
        self.____type6_representation = Type6Representation(6,
                                                            type1_representation,
                                                            self,
                                                            type3_representation,
                                                            type4_representation,
                                                            type5_representation,
                                                            next_id_generator)
        self.____type3_representation = Type3Representation(type1_representation,
                                                            self,
                                                            type4_representation,
                                                            type5_representation,
                                                            type6_representation,
                                                            next_id_generator)
        self.____type4_representation1 = Type4Representation(type1_representation,
                                                             self,
                                                             type3_representation,
                                                             type5_representation,
                                                             type6_representation,
                                                             next_id_generator)
        self.____type4_representation2 = Type4Representation(type1_representation,
                                                             self,
                                                             type3_representation,
                                                             type5_representation,
                                                             type6_representation,
                                                             next_id_generator)

    def _get_self_representation(self) -> str:
        return f"""{{
            "type": "tests.model.model.Type2",
            "id": {self._current_id},
            "object": {{
                "_Type2__Y": {{
                    "type": "list",
                    "id": {next(self._next_id_generator)},
                    "array": [1, true, 3]
                }},
                "Z": {{
                    "type": "tuple",
                    "id": {next(self._next_id_generator)},
                    "array": [1, 2, false]
                }},
                "W": {{
                    "type": "set",
                    "id": {next(self._next_id_generator)},
                    "array": [1, 2, 3]
                }},
                "_S": {{
                    "type": "tuple",
                    "id": {next(self._next_id_generator)},
                    "array": [
                        {self.____type5_representation1()}, 
                        {self.____type6_representation()}
                    ]
                }},
                "L": {{
                    "type": "list",
                    "id": {next(self._next_id_generator)},
                    "array": [
                        {self.____type3_representation()}, 
                        {self.____type4_representation1()}
                    ]
                }},
                "_Type2__T": {{
                    "type": "tuple",
                    "id": {next(self._next_id_generator)},
                    "array": [
                        {self.____type4_representation2()}, 
                        {self.____type5_representation2()} 
                    ]
                }},
                "type1": {self._get_type_representation(self.__type1_representation)},
                "type3": {self._get_type_representation(self.__type3_representation)},
                "type4": {self._get_type_representation(self.__type4_representation)},
                "type5": {self._get_type_representation(self.__type5_representation)},
                "type6": {self._get_type_representation(self.__type6_representation)}   
            }}
        }}"""


class Type1Representation(__BaseTypeRepresentation):
    def __init__(self, y: str,
                 next_id_generator: Generator[int, None, None]):
        super().__init__(next_id_generator)
        self.__y = y
        self.____type2_representation = Type2Representation(self,
                                                            None,
                                                            None,
                                                            None,
                                                            None,
                                                            next_id_generator)

    def _get_self_representation(self) -> str:
        return f"""{{
            "type": "tests.model.model.Type1",
            "id": {self._current_id},
            "object": {{
                "_y": "{self.__y}",
                "a": 1,
                "_b": "2",
                "_Type1__type": {self.____type2_representation()},
                "_Type1__c": 3.0
            }}
        }}"""
