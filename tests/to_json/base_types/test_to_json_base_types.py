import base64
import json

import dill
from assertpy import assertpy

import tarragon
from tests.to_json.common import Hook


def test_to_json_frozenset():
    hook = Hook()
    st = frozenset([hook])
    hook.ref = st

    actual_json = tarragon.to_json(st)
    expected_json = f"""{{
        "type": "frozenset",
        "id": 0,
        "array": [
            {{
                "type": "tests.to_json.common.Hook",
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


def test_to_json_set():
    st = set()
    hook = Hook(st)
    st.add(hook)

    actual_json = tarragon.to_json(st)
    expected_json = f"""{{
        "type": "set",
        "id": 0,
        "array": [
            {{
                "type": "tests.to_json.common.Hook",
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


def test_to_json_complex():
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


def test_to_json_int():
    value = 1

    actual_json = tarragon.to_json(value)
    expected_json = f"{value}"

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_to_json_float():
    value = 1.1

    actual_json = tarragon.to_json(value)
    expected_json = f"{value}"

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_to_json_bool():
    actual_json = tarragon.to_json(True)
    expected_json = "true"

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_to_json_str():
    value = "hello"

    actual_json = tarragon.to_json(value)
    expected_json = f"\"{value}\""

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_to_json_None():
    actual_json = tarragon.to_json(None)
    expected_json = "null"

    assertpy.assert_that(actual_json).is_equal_to(expected_json)


def test_to_json_exception():
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


def test_to_json_class():
    class A:
        """doc: class A"""
        pass

    actual_json = tarragon.to_json(A)
    actual_dict = json.loads(actual_json)

    actual_dict["object"]["__dict__"]["base64"] = None
    actual_dict["object"]["__weakref__"]["base64"] = None

    expected_json = f"""{{
      "type": "builtins.type",
      "id": 0,
      "object": {{
        "__module__": "tests.to_json.base_types.test_to_json_base_types",
        "__dict__": {{
          "type": "builtins.getset_descriptor",
          "id": 1,
          "base64": null
        }},
        "__weakref__": {{
          "type": "builtins.getset_descriptor",
          "id": 2,
          "base64": null
        }},
        "__doc__": "doc: class A"
      }}
    }}"""
    expected_dict = json.loads(expected_json)

    assertpy.assert_that(actual_dict).is_equal_to(expected_dict)


def test_to_json_generator():
    def get42():
        yield 42

    generator = get42()

    # FIXME dill doesn't support serializing generators, so for now it's like this:
    assertpy.assert_that(tarragon.to_json).raises(TypeError).when_called_with(generator).is_equal_to(
        "cannot pickle 'generator' object")


def test_to_json_function():
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


def test_to_json_iter():
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


def test_to_json_range():
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


def test_to_json_map():
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


def test_to_json_object():
    obj = object()

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.object", 
        "id": 0, 
        "base64": "{base64.b64encode(dill.dumps(obj)).decode("ascii")}"
    }}'''

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_to_json_bytes():
    obj = b"123"

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.bytes", 
        "id": 0, 
        "base64": "{base64.b64encode(obj).decode("ascii")}"
    }}'''

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_to_json_bytearray():
    obj = bytearray(b"123")

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.bytearray", 
        "id": 0, 
        "base64": "{base64.b64encode(obj).decode("ascii")}"
    }}'''

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_to_json_memoryview():
    obj = memoryview(b"123")

    actual_json = tarragon.to_json(obj)
    expected_json = f'''{{
        "type": "builtins.memoryview", 
        "id": 0, 
        "base64": "{base64.b64encode(obj).decode("ascii")}"
    }}'''

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))
