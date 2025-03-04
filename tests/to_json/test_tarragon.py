import base64
import json

import assertpy
import dill

import tarragon
from tests.model.foo.bar.model_too import Type5, Type6
from tests.model.foo.model import Type4
from tests.model.model import Type1
from tests.to_json.model_expected import Type1Representation, next_id, Type5Representation, Type4Representation, \
    Type6Representation


class Hook:
    def __init__(self, ref=None):
        self.ref = ref


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

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


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

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


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

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_frozenset_to_json():
    hook = Hook()
    st = frozenset([hook])
    hook.ref = st

    actual_json = tarragon.to_json(st)
    expected_json = f"""{{
        "type": "frozenset",
        "id": 0,
        "array": [
            {{
                "type": "tests.to_json.test_tarragon.Hook",
                "id": 1,
                "object": {{
                    "ref": {{
                        "ref_id": 0
                    }}
                }}
            }}
        ]
    }}"""

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_set_to_json():
    st = set()
    hook = Hook(st)
    st.add(hook)

    actual_json = tarragon.to_json(st)
    expected_json = f"""{{
        "type": "set",
        "id": 0,
        "array": [
            {{
                "type": "tests.to_json.test_tarragon.Hook",
                "id": 1,
                "object": {{
                    "ref": {{
                        "ref_id": 0
                    }}
                }}
            }}
        ]
    }}"""

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_type_object_to_json():
    y = "1"

    actual_json = tarragon.to_json(Type1(y))
    expected_json = Type1Representation(y, next_id())()

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_complex_to_json():
    obj = complex(1, 2)

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.complex", 
        "id": 0, 
        "base64": "{base64.b64encode(dill.dumps(obj)).decode("ascii")}"
    }}'''

    with assertpy.soft_assertions():
        json_loads = json.loads(actual_json)
        assertpy.assert_that(json_loads).is_equal_to(json.loads(expected_json))

        actual_obj: complex = dill.loads(base64.b64decode(json_loads["base64"].encode("ascii")))
        assertpy.assert_that(actual_obj).is_equal_to(obj)
        assertpy.assert_that(actual_obj.imag).is_equal_to(obj.imag)
        assertpy.assert_that(actual_obj.real).is_equal_to(obj.real)


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


def test_exception_to_json():
    exc = Exception("test")

    actual_json = tarragon.to_json(exc)
    expected_json = f'''{{
        "type": "builtins.Exception", 
        "id": 0, 
        "base64": "{base64.b64encode(dill.dumps(exc)).decode("ascii")}"
    }}'''

    with assertpy.soft_assertions():
        json_loads = json.loads(actual_json)
        assertpy.assert_that(json_loads).is_equal_to(json.loads(expected_json))

        actual_exc = dill.loads(base64.b64decode(json_loads["base64"].encode("ascii")))
        assertpy.assert_that(actual_exc.args).is_equal_to(exc.args)


def test_class_to_json():
    raise NotImplementedError()


def test_generator_to_json():
    def get42():
        yield 42

    generator = get42()

    assertpy.assert_that(tarragon.to_json).raises(TypeError).when_called_with(generator).is_equal_to(
        "cannot pickle 'generator' object")


def test_function_to_json():
    def get42():
        return 42

    actual_json = tarragon.to_json(get42)
    expected_json = f'''{{
        "type": "builtins.function", 
        "id": 0, 
        "base64": "{base64.b64encode(dill.dumps(get42)).decode("ascii")}"
    }}'''

    with assertpy.soft_assertions():
        json_loads = json.loads(actual_json)
        assertpy.assert_that(json_loads).is_equal_to(json.loads(expected_json))

        actual_get42 = dill.loads(base64.b64decode(json_loads["base64"].encode("ascii")))
        assertpy.assert_that(actual_get42()).is_equal_to(42)


def test_iter_to_json():
    lst = [1, 2, 3]
    obj = iter(lst)
    next(obj)

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.list_iterator", 
        "id": 0, 
        "base64": "{base64.b64encode(dill.dumps(obj)).decode("ascii")}"
    }}'''

    with assertpy.soft_assertions():
        json_loads = json.loads(actual_json)
        assertpy.assert_that(json_loads).is_equal_to(json.loads(expected_json))

        actual_obj = dill.loads(base64.b64decode(json_loads["base64"].encode("ascii")))
        assertpy.assert_that(list(actual_obj)).is_equal_to([2, 3])
        assertpy.assert_that(list(actual_obj)).is_empty()


def test_range_to_json():
    obj = range(3)

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.range", 
        "id": 0, 
        "base64": "{base64.b64encode(dill.dumps(obj)).decode("ascii")}"
    }}'''

    with assertpy.soft_assertions():
        json_loads = json.loads(actual_json)
        assertpy.assert_that(json_loads).is_equal_to(json.loads(expected_json))

        actual_obj = dill.loads(base64.b64decode(json_loads["base64"].encode("ascii")))
        assertpy.assert_that(actual_obj).is_equal_to(range(3))
        assertpy.assert_that(list(actual_obj)).is_equal_to([0, 1, 2])
        assertpy.assert_that(list(actual_obj)).is_equal_to([0, 1, 2])


def test_map_to_json():
    obj = map(lambda x: x ** 2, [1, 2, 3])
    next(obj)

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.map", 
        "id": 0, 
        "base64": "{base64.b64encode(dill.dumps(obj)).decode("ascii")}"
    }}'''

    with assertpy.soft_assertions():
        json_loads = json.loads(actual_json)
        assertpy.assert_that(json_loads).is_equal_to(json.loads(expected_json))

        actual_obj = dill.loads(base64.b64decode(json_loads["base64"].encode("ascii")))
        assertpy.assert_that(list(actual_obj)).is_equal_to([4, 9])
        assertpy.assert_that(list(actual_obj)).is_empty()


def test_object_to_json():
    obj = object()

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.object", 
        "id": 0, 
        "base64": "{base64.b64encode(dill.dumps(obj)).decode("ascii")}"
    }}'''

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_bytes_to_json():
    obj = b"123"

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.bytes", 
        "id": 0, 
        "base64": "{base64.b64encode(obj).decode("ascii")}"
    }}'''

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_bytearray_to_json():
    obj = bytearray(b"123")

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.bytearray", 
        "id": 0, 
        "base64": "{base64.b64encode(obj).decode("ascii")}"
    }}'''

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_memoryview_to_json():
    obj = memoryview(b"123")

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.memoryview", 
        "id": 0, 
        "base64": "{base64.b64encode(obj).decode("ascii")}"
    }}'''

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))
