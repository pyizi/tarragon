import json

import assertpy
import pytest

import tarragon
from tests.model.frozen_dataclass.foo.bar.model_too import Type5, Type6
from tests.model.frozen_dataclass.foo.model import Type4
from tests.model.frozen_dataclass.model import Type1
from tests.to_json.common import Hook
from tests.to_json.custom_types.model_expected import ModelRepresentation, ModelType


@pytest.fixture(scope='function')
def model_representation():
    return ModelRepresentation(ModelType.FROZEN_DATACLASS)


def test_to_json_dict_of_frozen_dataclass(model_representation):
    uid = 7

    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type6_object = Type6(uid, None, None, None, type4_object, type5_object)
    object.__setattr__(type5_object, "type4", type4_object)
    object.__setattr__(type5_object, "type6", type6_object)
    object.__setattr__(type4_object, "type6", type6_object)
    hook = Hook()
    dct = {type5_object: "67", type6_object: type4_object, 1: type5_object, hook: hook}
    hook.ref = dct
    actual_json = tarragon.to_json(dct)

    type5_representation = model_representation.create_type5(None, None, None, None, None)
    type4_representation = model_representation.create_type4(None, None, None, type5_representation, None)
    type6_representation = model_representation.create_type6(uid, None, None, None, type4_representation,
                                                             type5_representation)
    type4_representation._Type4__type6_representation = type6_representation
    type5_representation._Type5__type4_representation = type4_representation
    type5_representation._Type5__type6_representation = type6_representation
    current_id = model_representation.get_next_id()
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
                    "type": "tests.to_json.common.Hook",
                    "id": {model_representation.get_next_id()},
                    "object": {{
                        "ref": {{
                            "ref_id": {current_id}
                        }}
                    }}
                }},
                "value": {{
                    "ref_id": {model_representation.get_next_id() - 1}
                }}
            }}
        ]
    }}"""

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_to_json_list_of_frozen_dataclass(model_representation):
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    object.__setattr__(type5_object, "type4", type4_object)
    lst = [type5_object, type4_object]
    lst.append(lst)
    actual_json = tarragon.to_json(lst)

    type5_representation = model_representation.create_type5(None, None, None, None, None)
    type4_representation = model_representation.create_type4(None, None, None, type5_representation, None)
    type5_representation._Type5__type4_representation = type4_representation
    current_id = model_representation.get_next_id()
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


def test_to_json_tuple_of_frozen_dataclass(model_representation):
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    object.__setattr__(type5_object, "type4", type4_object)
    hook = Hook()
    tpl = (type5_object, type4_object, hook)
    hook.ref = tpl
    actual_json = tarragon.to_json(tpl)

    type5_representation = model_representation.create_type5(None, None, None, None, None)
    type4_representation = model_representation.create_type4(None, None, None, type5_representation, None)
    type5_representation._Type5__type4_representation = type4_representation
    current_id = model_representation.get_next_id()
    expected_json = f"""{{
        "type": "tuple",
        "id": {current_id},
        "array": [
            {type5_representation()}, 
            {type4_representation()}, 
            {{
                "type": "tests.to_json.common.Hook",
                "id": {model_representation.get_next_id()},
                "object": {{
                    "ref": {{
                        "ref_id": {current_id}
                    }}
                }}
            }}
        ]
    }}"""

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))


def test_to_json_frozen_dataclass(model_representation):
    y = "1"

    actual_json = tarragon.to_json(Type1(y))
    expected_json = model_representation.create_type1(y)()

    assertpy.assert_that(json.loads(actual_json)).is_equal_to(json.loads(expected_json))
