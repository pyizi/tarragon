import json
from typing import Any


class __DictRepresentor:
    def __init__(self, root_obj: Any | None):
        self.__root_obj = root_obj
        self.__init_state()

    @property
    def next_virtual_id(self) -> int:
        result = self.__next_virtual_id
        self.__next_virtual_id += 1
        return result

    def run(self) -> int | float | bool | str | list | dict | None:
        result = self.__get_representation(self.__root_obj)
        self.__init_state()
        return result

    def __init_state(self):
        self.__real_to_virtual_id = {}
        self.__next_virtual_id = 0

    def __get_representation(self, obj: Any | None) -> int | float | bool | str | list | dict | None:
        obj_type = type(obj)
        if obj is None:
            return None
        elif obj_type in [int, float, bool, str]:
            return obj

        real_obj_id = id(obj)
        if real_obj_id in self.__real_to_virtual_id:
            return {
                "ref_id": self.__real_to_virtual_id[real_obj_id],
            }
        else:
            virtual_obj_id = self.next_virtual_id

            self.__real_to_virtual_id[real_obj_id] = virtual_obj_id

            if obj_type in [list, tuple, set]:
                array = []
                for item in obj:
                    array.append(self.__get_representation(item))
                return {
                    "type": obj_type.__name__,
                    "id": virtual_obj_id,
                    "array": array
                }
            elif obj_type is dict:
                items = []
                for key, value in obj.items():
                    items.append({
                        "key": self.__get_representation(key),
                        "value": self.__get_representation(value)
                    })
                return {
                    "type": obj_type.__name__,
                    "id": virtual_obj_id,
                    "items": items
                }
            else:
                # If custom class
                fields = {}
                for key, value in vars(obj).items():
                    fields[key] = self.__get_representation(value)
                return {
                    "type": obj_type.__module__ + "." + obj_type.__name__,
                    "id": virtual_obj_id,
                    "object": fields
                }


def to_json(obj: Any) -> str:
    return json.dumps(__DictRepresentor(obj).run())


def from_json(json: str) -> Any:
    raise NotImplementedError()


def to_yaml(obj: Any) -> str:
    raise NotImplementedError()


def from_yaml(yaml: str) -> Any:
    raise NotImplementedError()


def to_xml(obj: Any) -> str:
    raise NotImplementedError()


def from_xml(xml: str) -> Any:
    raise NotImplementedError()
