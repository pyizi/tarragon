import assertpy

import tarragon
from tests.common import Hook
from tests.model.frozen_dataclass.foo.bar.model_too import Type5, Type6
from tests.model.frozen_dataclass.foo.model import Type4
from tests.model.frozen_dataclass.model import Type1


def test_from_json_dict_of_frozen_dataclass():
    uid = 7

    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type6_object = Type6(uid, None, None, None, type4_object, type5_object)
    object.__setattr__(type5_object, "type4", type4_object)
    object.__setattr__(type5_object, "type6", type6_object)
    object.__setattr__(type4_object, "type6", type6_object)
    hook = Hook()
    expected = {type5_object: "67", type6_object: type4_object, 1: type5_object, hook: hook}
    hook.ref = expected

    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_list_of_frozen_dataclass():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    object.__setattr__(type5_object, "type4", type4_object)
    expected = [type5_object, type4_object]
    expected.append(expected)

    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_tuple_of_frozen_dataclass():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    object.__setattr__(type5_object, "type4", type4_object)
    hook = Hook()
    expected = (type5_object, type4_object, hook)
    hook.ref = expected

    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_frozen_dataclass():
    y = "1"

    expected = Type1(y)
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)
