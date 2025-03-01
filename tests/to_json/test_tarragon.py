import json
from typing import Any

import assertpy
from frozendict import frozendict

import tarragon
from tests.model.foo.bar.model_too import Type5, Type6
from tests.model.foo.model import Type4
from tests.model.model import Type1
from tests.to_json.model_expected import type1, type4, type5, type6


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

    actual_json = tarragon.to_json({Type5(): "67", Type6(uid): Type4(), 1: Type5()})
    expected_json = f"""{{
        "type": "dict",
        "items": [
            {{
                "key": {type5()},
                "value": "67"
            }},
            {{
                "key": {type6(uid)},
                "value": {type4()}
            }},
            {{
                "key": 1,
                "value": {type5()}
            }}
        ]
    }}"""

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


def test_list_to_json():
    actual_json = tarragon.to_json([Type5(), Type4()])
    expected_json = f"[{type5()}, {type4()}]"

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


def test_tuple_to_json():
    actual_json = tarragon.to_json((Type5(), Type4()))
    expected_json = f"""{{
                "type": "tuple",
                "array": [{type5()}, {type4()}]
            }}"""

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


def test_set_to_json():
    actual_json = tarragon.to_json({Type5(), Type4()})
    expected_json = f"""{{
                "type": "set",
                "array": [{type5()}, {type4()}]
            }}"""

    assertpy.assert_that(SetsAndDictsFixer.fix(json.loads(actual_json))).is_equal_to(
        SetsAndDictsFixer.fix(json.loads(expected_json)))


def test_object_to_json():
    y = "1"

    actual_json = tarragon.to_json(Type1(y))
    expected_json = type1(y)

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
