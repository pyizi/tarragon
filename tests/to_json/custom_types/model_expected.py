from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Generator


class ModelType(Enum):
    VANILLA = "vanilla"
    DATACLASS = "dataclass"
    FROZEN_DATACLASS = "frozen_dataclass"
    ATTR = "attr"
    FROZEN_ATTR = "frozen_attr"


class ModelRepresentation:
    def __init__(self, model_type: ModelType, start_id: int = 0):
        self.__model_type = model_type
        self.__next_id_generator = self.__next_id(start_id)

    def get_next_id(self) -> int:
        return next(self.__next_id_generator)

    def __next_id(self, start_id: int) -> Generator[int, None, None]:
        while True:
            yield start_id
            start_id += 1

    class _BaseType(ABC):
        def __init__(self, model_type: ModelType, next_id_generator: Generator[int, None, None]):
            self._model_type = model_type
            self.__already_called = False
            self._current_id = None
            self._next_id_generator = next_id_generator

        @staticmethod
        def _get_type_representation(type_representation: ModelRepresentation._BaseType | None) -> str:
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

    def create_type6(self, uid: int,
                     type1_representation: ModelRepresentation.Type1 | None,
                     type2_representation: ModelRepresentation.Type2 | None,
                     type3_representation: ModelRepresentation.Type3 | None,
                     type4_representation: ModelRepresentation.Type4 | None,
                     type5_representation: ModelRepresentation.Type5 | None) -> ModelRepresentation.Type6:
        return ModelRepresentation.Type6(self.__model_type, uid,
                                         type1_representation, type2_representation, type3_representation,
                                         type4_representation, type5_representation,
                                         self.__next_id_generator)

    class Type6(_BaseType):
        def __init__(self, model_type: ModelType,
                     uid: int,
                     type1_representation: ModelRepresentation.Type1 | None,
                     type2_representation: ModelRepresentation.Type2 | None,
                     type3_representation: ModelRepresentation.Type3 | None,
                     type4_representation: ModelRepresentation.Type4 | None,
                     type5_representation: ModelRepresentation.Type5 | None,
                     next_id_generator: Generator[int, None, None]):
            super().__init__(model_type, next_id_generator)
            self.__uid = uid
            self.__type1_representation = type1_representation
            self.__type2_representation = type2_representation
            self.__type3_representation = type3_representation
            self.__type4_representation = type4_representation
            self.__type5_representation = type5_representation

        def _get_self_representation(self) -> str:
            return f"""{{
                "type": "tests.model.{self._model_type.value}.foo.bar.model_too.Type6",
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

    def create_type5(self, type1_representation: ModelRepresentation.Type1 | None,
                     type2_representation: ModelRepresentation.Type2 | None,
                     type3_representation: ModelRepresentation.Type3 | None,
                     type4_representation: ModelRepresentation.Type4 | None,
                     type6_representation: ModelRepresentation.Type6 | None) -> ModelRepresentation.Type5:
        return ModelRepresentation.Type5(self.__model_type, type1_representation, type2_representation,
                                         type3_representation, type4_representation, type6_representation,
                                         self.__next_id_generator)

    class Type5(_BaseType):
        def __init__(self, model_type: ModelType,
                     type1_representation: ModelRepresentation.Type1 | None,
                     type2_representation: ModelRepresentation.Type2 | None,
                     type3_representation: ModelRepresentation.Type3 | None,
                     type4_representation: ModelRepresentation.Type4 | None,
                     type6_representation: ModelRepresentation.Type6 | None,
                     next_id_generator: Generator[int, None, None]):
            super().__init__(model_type, next_id_generator)
            self.__type1_representation = type1_representation
            self.__type2_representation = type2_representation
            self.__type3_representation = type3_representation
            self.__type4_representation = type4_representation
            self.__type6_representation = type6_representation
            self.____type6_representation = ModelRepresentation.Type6(model_type,
                                                                      12,
                                                                      type1_representation,
                                                                      type2_representation,
                                                                      type3_representation,
                                                                      type4_representation,
                                                                      self,
                                                                      next_id_generator)

        def _get_self_representation(self) -> str:
            return f"""{{
                "type": "tests.model.{self._model_type.value}.foo.bar.model_too.Type5",
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

    def create_type4(self, type1_representation: ModelRepresentation.Type1 | None,
                     type2_representation: ModelRepresentation.Type2 | None,
                     type3_representation: ModelRepresentation.Type3 | None,
                     type5_representation: ModelRepresentation.Type5 | None,
                     type6_representation: ModelRepresentation.Type6 | None) -> ModelRepresentation.Type4:
        return ModelRepresentation.Type4(self.__model_type, type1_representation, type2_representation,
                                         type3_representation, type5_representation, type6_representation,
                                         self.__next_id_generator)

    class Type4(_BaseType):
        def __init__(self, model_type: ModelType,
                     type1_representation: ModelRepresentation.Type1 | None,
                     type2_representation: ModelRepresentation.Type2 | None,
                     type3_representation: ModelRepresentation.Type3 | None,
                     type5_representation: ModelRepresentation.Type5 | None,
                     type6_representation: ModelRepresentation.Type6 | None,
                     next_id_generator: Generator[int, None, None]):
            super().__init__(model_type, next_id_generator)
            self.__type1_representation = type1_representation
            self.__type2_representation = type2_representation
            self.__type3_representation = type3_representation
            self.__type5_representation = type5_representation
            self.__type6_representation = type6_representation
            self.____type5_representation = ModelRepresentation.Type5(model_type,
                                                                      type1_representation,
                                                                      type2_representation,
                                                                      type3_representation,
                                                                      self,
                                                                      type6_representation,
                                                                      next_id_generator)
            self.____type6_representation = ModelRepresentation.Type6(model_type,
                                                                      123,
                                                                      type1_representation,
                                                                      type2_representation,
                                                                      type3_representation,
                                                                      self,
                                                                      type5_representation,
                                                                      next_id_generator)

        def _get_self_representation(self) -> str:
            return f"""{{
                "type": "tests.model.{self._model_type.value}.foo.model.Type4",
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

    def create_type3(self, type1_representation: ModelRepresentation.Type1 | None,
                     type2_representation: ModelRepresentation.Type2 | None,
                     type4_representation: ModelRepresentation.Type4 | None,
                     type5_representation: ModelRepresentation.Type5 | None,
                     type6_representation: ModelRepresentation.Type6 | None) -> ModelRepresentation.Type3:
        return ModelRepresentation.Type3(self.__model_type, type1_representation, type2_representation,
                                         type4_representation, type5_representation, type6_representation,
                                         self.__next_id_generator)

    class Type3(_BaseType):
        def __init__(self, model_type: ModelType,
                     type1_representation: ModelRepresentation.Type1 | None,
                     type2_representation: ModelRepresentation.Type2 | None,
                     type4_representation: ModelRepresentation.Type4 | None,
                     type5_representation: ModelRepresentation.Type5 | None,
                     type6_representation: ModelRepresentation.Type6 | None,
                     next_id_generator: Generator[int, None, None]):
            super().__init__(model_type, next_id_generator)
            self.__type1_representation = type1_representation
            self.__type2_representation = type2_representation
            self.__type4_representation = type4_representation
            self.__type5_representation = type5_representation
            self.__type6_representation = type6_representation
            self.____type5_representation1 = ModelRepresentation.Type5(model_type,
                                                                       type1_representation,
                                                                       type2_representation,
                                                                       self,
                                                                       type4_representation,
                                                                       type6_representation,
                                                                       next_id_generator)
            self.____type5_representation2 = ModelRepresentation.Type5(model_type,
                                                                       type1_representation,
                                                                       type2_representation,
                                                                       self,
                                                                       type4_representation,
                                                                       type6_representation,
                                                                       next_id_generator)
            self.____type6_representation = ModelRepresentation.Type6(model_type,
                                                                      7,
                                                                      type1_representation,
                                                                      type2_representation,
                                                                      self,
                                                                      type4_representation,
                                                                      type5_representation,
                                                                      next_id_generator)
            self.____type4_representation = ModelRepresentation.Type4(model_type,
                                                                      type1_representation,
                                                                      type2_representation,
                                                                      self,
                                                                      type5_representation,
                                                                      type6_representation,
                                                                      next_id_generator)

        def _get_self_representation(self) -> str:
            return f"""{{
                "type": "tests.model.{self._model_type.value}.foo.model.Type3",
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

    def create_type2(self, type1_representation: ModelRepresentation.Type1 | None,
                     type3_representation: ModelRepresentation.Type3 | None,
                     type4_representation: ModelRepresentation.Type4 | None,
                     type5_representation: ModelRepresentation.Type5 | None,
                     type6_representation: ModelRepresentation.Type6 | None) -> ModelRepresentation.Type2:
        return ModelRepresentation.Type2(self.__model_type, type1_representation, type3_representation,
                                         type4_representation, type5_representation, type6_representation,
                                         self.__next_id_generator)

    class Type2(_BaseType):
        def __init__(self, model_type: ModelType,
                     type1_representation: ModelRepresentation.Type1 | None,
                     type3_representation: ModelRepresentation.Type3 | None,
                     type4_representation: ModelRepresentation.Type4 | None,
                     type5_representation: ModelRepresentation.Type5 | None,
                     type6_representation: ModelRepresentation.Type6 | None,
                     next_id_generator: Generator[int, None, None]):
            super().__init__(model_type, next_id_generator)
            self.__type1_representation = type1_representation
            self.__type3_representation = type3_representation
            self.__type4_representation = type4_representation
            self.__type5_representation = type5_representation
            self.__type6_representation = type6_representation
            self.____type5_representation1 = ModelRepresentation.Type5(model_type,
                                                                       type1_representation,
                                                                       self,
                                                                       type3_representation,
                                                                       type4_representation,
                                                                       type6_representation,
                                                                       next_id_generator)
            self.____type5_representation2 = ModelRepresentation.Type5(model_type,
                                                                       type1_representation,
                                                                       self,
                                                                       type3_representation,
                                                                       type4_representation,
                                                                       type6_representation,
                                                                       next_id_generator)
            self.____type6_representation = ModelRepresentation.Type6(model_type,
                                                                      6,
                                                                      type1_representation,
                                                                      self,
                                                                      type3_representation,
                                                                      type4_representation,
                                                                      type5_representation,
                                                                      next_id_generator)
            self.____type3_representation = ModelRepresentation.Type3(model_type,
                                                                      type1_representation,
                                                                      self,
                                                                      type4_representation,
                                                                      type5_representation,
                                                                      type6_representation,
                                                                      next_id_generator)
            self.____type4_representation = ModelRepresentation.Type4(model_type,
                                                                      type1_representation,
                                                                      self,
                                                                      type3_representation,
                                                                      type5_representation,
                                                                      type6_representation,
                                                                      next_id_generator)

        def _get_self_representation(self) -> str:
            return f"""{{
                "type": "tests.model.{self._model_type.value}.model.Type2",
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
                            {self.____type4_representation()}
                        ]
                    }},
                    "_Type2__T": {{
                        "type": "tuple",
                        "id": {next(self._next_id_generator)},
                        "array": [
                            {self.____type4_representation()}, 
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

    def create_type1(self, y: str) -> ModelRepresentation.Type1:
        return ModelRepresentation.Type1(self.__model_type,
                                         y,
                                         self.__next_id_generator)

    class Type1(_BaseType):
        def __init__(self, model_type: ModelType,
                     y: str,
                     next_id_generator: Generator[int, None, None]):
            super().__init__(model_type, next_id_generator)
            self.__y = y
            self.____type2_representation = ModelRepresentation.Type2(model_type,
                                                                      self,
                                                                      None,
                                                                      None,
                                                                      None,
                                                                      None,
                                                                      next_id_generator)

        def _get_self_representation(self) -> str:
            return f"""{{
                "type": "tests.model.{self._model_type.value}.model.Type1",
                "id": {self._current_id},
                "object": {{
                    "_y": "{self.__y}",
                    "a": 1,
                    "_b": "2",
                    "_Type1__type": {self.____type2_representation()},
                    "_Type1__c": 3.0
                }}
            }}"""
