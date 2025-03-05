import base64
import json
import types
from typing import Any

import dill


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

            if obj_type in [list, tuple, set, frozenset]:
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
                result = {
                    "type": obj_type.__module__ + "." + obj_type.__name__,
                    "id": virtual_obj_id,
                }

                # TODO If it has no "__dict__" then
                #  for "dataclasses" we can use "__dataclass_fields__" and
                #  for "attrs" we can use "__attrs_attrs__"
                if hasattr(obj, "__dict__") and obj_type != types.FunctionType and not isinstance(obj, BaseException):
                    fields = {}
                    for key, value in vars(obj).items():
                        fields[key] = self.__get_representation(value)
                    result["object"] = fields
                else:
                    # Binarization:
                    try:
                        memoryview(obj)
                    except TypeError:
                        # If the type DOES NOT implement the buffer protocol, it must first be processed through dill
                        result["base64"] = base64.b64encode(dill.dumps(obj)).decode("ascii")

                        if obj_type is types.FunctionType and obj.__closure__:
                            # TODO Functions with closures and without closures need to be distinguished.
                            #  Functions without closures can be stored as they are, just in binary form.
                            #  Functions with closures need to be stored along with the information about the values of
                            #  the variables on which the closures are bound, including their "virtual_obj_id" and the
                            #  full path to them in the program code. The thing is, after deserialization, a copy of the
                            #  original state is created. For example, this will result in the scenario where if I had
                            #  two functions bound to the same variable, after restoration this information would be
                            #  lost; there would effectively be two separate variables and their states would be split.
                            #  In classic dill, this is solved by serializing several functions together as a single
                            #  unit, as part of one object. However, in my case everything is broken down into pieces
                            #  and the state must be restored manually. Moreover, even dill does not know what to do
                            #  with problems such as restoring a function whose state should be closed over a global
                            #  variable, for example, or over any variable that was not included in the serialized
                            #  object. I want, upon restoration, to search at the restoration point for the original
                            #  variable on which everything was bound and re-bind the closure to it. And only if that
                            #  variable does not exist in the current scope, then use its copy.
                            #  Well, or this can be done optionally. Most likely, this will result in even primitives
                            #  like "int" having to be stored with a "virtual_obj_id" (along with the type indication).
                            #  This will make the format less readable.
                            pass
                    else:
                        # If the type implements the buffer protocol, then it can be encoded to base64 directly
                        result["base64"] = base64.b64encode(obj).decode("ascii")

                return result


def to_json(obj: Any) -> str:
    return json.dumps(__DictRepresentor(obj).run())


def from_json(json: str) -> Any:
    # TODO
    raise NotImplementedError()


def to_yaml(obj: Any) -> str:
    # TODO instead of "ref_id" in json's implementation should use yaml's refs supporting
    raise NotImplementedError()


def from_yaml(yaml: str) -> Any:
    # TODO
    raise NotImplementedError()


def to_xml(obj: Any) -> str:
    # TODO simple implementation without supporting of xml's configuration
    raise NotImplementedError()


def from_xml(xml: str) -> Any:
    # TODO
    raise NotImplementedError()
