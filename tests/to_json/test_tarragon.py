import json
from typing import Any

import assertpy
from frozendict import frozendict

import tarragon
from tests.model.foo.bar.model_too import Type5, Type6
from tests.model.foo.model import Type4
from tests.model.model import Type1
from tests.to_json.model_expected import Type1Representation, next_id, Type5Representation, Type4Representation, \
    Type6Representation


class Hook:
    def __init__(self, ref=None):
        self.ref = ref


# FIXME вероятно можно будет удалить, т.к dict соблюдает порядок, а set-ов больше у меня не осталось (почти)
class SetsAndDictsFixer:
    @classmethod
    def __dive_to_list(cls, lst: list[Any]):
        for i, item in enumerate(lst):
            if type(item) is list:
                cls.__dive_to_list(item)
                lst[i] = tuple(item)
            elif type(item) is dict:
                cls.__fix_sets_and_dicts(item)
                lst[i] = frozendict(item)

    @classmethod
    def __fix_sets_and_dicts(cls, dct: dict[str, Any]):
        for key, value in dct.items():
            if type(value) is dict:
                cls.__fix_sets_and_dicts(value)
                dct[key] = frozendict(value)
            elif type(value) is list:
                cls.__dive_to_list(value)
                dct[key] = tuple(value)
            elif key == "type":
                if value == "set":
                    cls.__dive_to_list(dct["array"])
                    dct["array"] = tuple(dct["array"])
                    dct["array"] = frozenset(dct["array"])
                elif value == "dict":
                    cls.__dive_to_list(dct["items"])
                    dct["items"] = tuple(dct["items"])
                    dct["items"] = frozenset(dct["items"])

    @classmethod
    def fix(cls, obj: dict[str, Any] | list[Any]) -> frozendict[str, Any] | tuple[Any]:
        if isinstance(obj, dict):
            cls.__fix_sets_and_dicts(obj)
            return frozendict(obj)
        elif isinstance(obj, list):
            cls.__dive_to_list(obj)
            return tuple(obj)
        else:
            raise ValueError(f"obj={obj} is not a dict/list")


def test_dict_to_json():
    uid = 7

    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type6_object = Type6(uid, None, None, None, type4_object, type5_object)
    type5_object.type4 = type4_object
    type5_object.type6 = type6_object
    type4_object.type6 = type6_object
    hook = Hook()
    dct = {type5_object: "67", type6_object: type4_object, 1: type5_object, hook: hook}
    hook.ref = dct
    actual_json = tarragon.to_json(dct)

    next_id_generator = next_id()
    type5_representation = Type5Representation(None, None, None, None, None,
                                               next_id_generator)
    type4_representation = Type4Representation(None, None, None, type5_representation, None,
                                               next_id_generator)
    type6_representation = Type6Representation(uid, None, None, None, type4_representation, type5_representation,
                                               next_id_generator)
    type4_representation._Type4Representation__type6_representation = type6_representation
    type5_representation._Type5Representation__type4_representation = type4_representation
    type5_representation._Type5Representation__type6_representation = type6_representation
    current_id = next(next_id_generator)
    expected_json = f"""{{
        "type": "dict",
        "id": {current_id},
        "items": [
            {{
                "key": {type5_representation()},
                "value": "67"
            }},
            {{
                "key": {type6_representation()},
                "value": {type4_representation()}
            }},
            {{
                "key": 1,
                "value": {type5_representation()}
            }},
            {{
                "key": {{
                    "type": "tests.to_json.test_tarragon.Hook",
                    "id": {next(next_id_generator)},
                    "object": {{
                        "ref": {{
                            "ref_id": {current_id}
                        }}
                    }}
                }},
                "value": {{
                    "ref_id": {next(next_id_generator) - 1}
                }}
            }}
        ]
    }}"""

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


def test_list_to_json():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type5_object.type4 = type4_object
    lst = [type5_object, type4_object]
    lst.append(lst)
    actual_json = tarragon.to_json(lst)

    next_id_generator = next_id()
    type5_representation = Type5Representation(None, None, None, None, None,
                                               next_id_generator)
    type4_representation = Type4Representation(None, None, None, type5_representation, None,
                                               next_id_generator)
    type5_representation._Type5Representation__type4_representation = type4_representation
    current_id = next(next_id_generator)
    expected_json = f"""{{
        "type": "list",
        "id": {current_id},
        "array": [
            {type5_representation()}, 
            {type4_representation()}, 
            {{
                "ref_id": {current_id}
            }}
        ]
    }}"""

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


def test_tuple_to_json():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type5_object.type4 = type4_object
    hook = Hook()
    tpl = (type5_object, type4_object, hook)
    hook.ref = tpl
    actual_json = tarragon.to_json(tpl)

    next_id_generator = next_id()
    type5_representation = Type5Representation(None, None, None, None, None,
                                               next_id_generator)
    type4_representation = Type4Representation(None, None, None, type5_representation, None,
                                               next_id_generator)
    type5_representation._Type5Representation__type4_representation = type4_representation
    current_id = next(next_id_generator)
    expected_json = f"""{{
        "type": "tuple",
        "id": {current_id},
        "array": [
            {type5_representation()}, 
            {type4_representation()}, 
            {{
                "type": "tests.to_json.test_tarragon.Hook",
                "id": {next(next_id_generator)},
                "object": {{
                    "ref": {{
                        "ref_id": {current_id}
                    }}
                }}
            }}
        ]
    }}"""

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


# FIXME тут видимо будут проблемы из-за неупорядоченности set
def test_set_to_json():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type5_object.type4 = type4_object
    st = {type5_object, type4_object}
    hook = Hook(st)
    st.add(hook)
    actual_json = tarragon.to_json(st)

    next_id_generator = next_id()
    type5_representation = Type5Representation(None, None, None, None, None,
                                               next_id_generator)
    type4_representation = Type4Representation(None, None, None, type5_representation, None,
                                               next_id_generator)
    type5_representation._Type5Representation__type4_representation = type4_representation
    current_id = next(next_id_generator)
    expected_json = f"""{{
        "type": "set",
        "id": {current_id},
        "array": [
            {type5_representation()}, 
            {type4_representation()}, 
            {{
                "type": "tests.to_json.test_tarragon.Hook",
                "id": {next(next_id_generator)},
                "object": {{
                    "ref": {{
                        "ref_id": {current_id}
                    }}
                }}
            }}
        ]
    }}"""

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


def test_object_to_json():
    y = "1"

    actual_json = tarragon.to_json(Type1(y))
    expected_json = Type1Representation(y, next_id())()

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


def test_int_to_json():
    value = 1

    actual_json = tarragon.to_json(value)
    expected_json = f"{value}"

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_float_to_json():
    value = 1.1

    actual_json = tarragon.to_json(value)
    expected_json = f"{value}"

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_bool_to_json():
    actual_json = tarragon.to_json(True)
    expected_json = "true"

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_str_to_json():
    value = "hello"

    actual_json = tarragon.to_json(value)
    expected_json = f"\"{value}\""

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_None_to_json():
    actual_json = tarragon.to_json(None)
    expected_json = "null"

    assertpy.assert_that(actual_json).is_equal_to(expected_json)
