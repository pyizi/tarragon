import json
from typing import Any

import assertpy

import tarragon
from model.foo.bar.model_too import Type5, Type6
from model.foo.model import Type4, Type3
from tests.model.model import Type1, Type2
from tests.to_json.model_expected import type1, type2, type3, type4, type5, type6


class JsonRepresentor:
    @classmethod
    def __get_json_list_representation(cls, lst: list) -> str:
        length = len(lst)
        result = ""
        for i, item in enumerate(lst):
            result += f"{cls.get_json_representation(item)}"
            if i + 1 < length:
                result += ","
        return f"[{result}]"

    @classmethod
    def get_json_representation(cls, obj: Any, *args) -> str:
        obj_type = type(obj)
        if obj_type in [int, float]:
            return f"{obj}"
        elif obj_type is bool:
            return f"{obj}".lower()
        elif obj_type is str:
            return f"\"{obj}\""
        elif obj_type is list:
            return cls.__get_json_list_representation(obj)
        elif obj_type in [tuple, set]:
            array = cls.__get_json_list_representation(obj)
            return f"""{{
                "type": "{obj_type.__name__}",
                "array": {array}
            }}"""
        elif obj_type is dict:
            length = len(obj)
            result = ""
            for i, key, value in enumerate(obj.items()):
                result += f"""{{
                    "key": {cls.get_json_representation(key)},
                    "value": {cls.get_json_representation(value)}
                }}"""
                if i + 1 < length:
                    result += ","
            return f"""{{
                "type": "{obj_type.__name__}",
                "items": [{result}]
            }}"""
        elif obj_type in [Type1, Type2, Type3, Type4, Type5, Type6]:
            # FIXME из-за того, что некоторые типы имеют конструктор с параметрами,
            #  бездумно использовать этот метод нельзя
            #  В основном он годится для примитивов и коллекций с примитивами
            return eval(obj_type.__name__.lower())(*args)
        else:
            raise ValueError(f"Unsupported type: {obj_type}")


def test_dict_to_json():
    uid = 7

    dct = {Type5(): "67", Type6(uid): Type4(), 1: Type5()}
    actual_json = tarragon.to_json(dct)

    length = len(dct)
    result = ""
    for i, (key, value) in enumerate(dct.items()):
        if type(key) is Type6:
            key_representation = JsonRepresentor.get_json_representation(key, uid)
        else:
            key_representation = JsonRepresentor.get_json_representation(key)
        result += f"""{{
            "key": {key_representation},
            "value": {JsonRepresentor.get_json_representation(value)}
        }}"""
        if i + 1 < length:
            result += ","
    expected_json = f"""{{
        "type": "dict",
        "items": [{result}]
    }}"""

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_list_to_json():
    lst = [Type5(), Type4()]

    actual_json = tarragon.to_json(lst)
    expected_json = JsonRepresentor.get_json_representation(lst)

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_tuple_to_json():
    tpl = (Type5(), Type4())

    actual_json = tarragon.to_json(tpl)
    expected_json = JsonRepresentor.get_json_representation(tpl)

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_set_to_json():
    st = {Type5(), Type4()}

    actual_json = tarragon.to_json(st)
    expected_json = JsonRepresentor.get_json_representation(st)

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_object_to_json():
    y = "1"
    actual_json = tarragon.to_json(Type1(y))

    expected_json = type1(y)

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


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
