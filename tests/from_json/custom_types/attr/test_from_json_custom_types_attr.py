import copy

import assertpy

import tarragon
from tests.common import Hook
from tests.model.attr.foo.bar.model_too import Type5, Type6
from tests.model.attr.foo.model import Type4
from tests.model.attr.model import Type1


# TODO write tests for check "types_substitution"

def test_from_json_dict_of_attr():
    uid = 7

    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type6_object = Type6(uid, None, None, None, type4_object, type5_object)
    type5_object.type4 = type4_object
    type5_object.type6 = type6_object
    type4_object.type6 = type6_object
    type5_object_copy = copy.deepcopy(type5_object)
    hook = Hook()
    expected = {type5_object: "67",
                type6_object: type4_object,
                1: type5_object,
                hook: hook,
                2: type5_object_copy}
    hook.ref = expected

    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_not_same_as(expected)
        assertpy.assert_that(actual).is_equal_to(expected)

        actual_items = {type(item).__name__: item for item in actual}
        assertpy.assert_that(actual_items["Hook"].ref).is_same_as(actual)

        assertpy.assert_that(next(iter(actual))).is_same_as(actual[1])

        assertpy.assert_that(actual[2]).is_equal_to(actual[1])
        assertpy.assert_that(actual[2]).is_not_same_as(actual[1])


def test_from_json_list_of_attr():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type5_object.type4 = type4_object
    type5_object_copy = copy.deepcopy(type5_object)
    expected = [type5_object, type4_object, type5_object, type5_object_copy]
    expected.append(expected)

    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_not_same_as(expected)
        assertpy.assert_that(actual).is_equal_to(expected)
        assertpy.assert_that(actual[4]).is_same_as(actual)

        assertpy.assert_that(actual[0]).is_same_as(actual[2])

        assertpy.assert_that(actual[3]).is_equal_to(actual[2])
        assertpy.assert_that(actual[3]).is_not_same_as(actual[2])


def test_from_json_tuple_of_attr():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type5_object.type4 = type4_object
    type5_object_copy = copy.deepcopy(type5_object)
    hook = Hook()
    expected = (type5_object, type4_object, hook, type5_object, type5_object_copy)
    hook.ref = expected

    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_not_same_as(expected)
        assertpy.assert_that(actual).is_equal_to(expected)
        assertpy.assert_that(actual[2].ref).is_same_as(actual)

        assertpy.assert_that(actual[0]).is_same_as(actual[3])

        assertpy.assert_that(actual[4]).is_equal_to(actual[3])
        assertpy.assert_that(actual[4]).is_not_same_as(actual[3])


def test_from_json_attr():
    y = "1"

    expected = Type1(y)
    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_not_same_as(expected)
        assertpy.assert_that(actual).is_equal_to(expected)

        assertpy.assert_that(actual._Type1__type.type1).is_same_as(actual)

        assertpy.assert_that(actual._Type1__type.L[1]).is_same_as(actual._Type1__type._Type2__T[0])

        assertpy.assert_that(actual._Type1__type._S[0]).is_equal_to(actual._Type1__type._Type2__T[1])
        assertpy.assert_that(actual._Type1__type._S[0]).is_not_same_as(actual._Type1__type._Type2__T[1])


def test_from_json_set_of_attr():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type5_object.type4 = type4_object
    type5_object_copy = copy.deepcopy(type5_object)
    expected = {type5_object, type4_object, type5_object_copy}
    hook = Hook(expected)
    expected.add(hook)

    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_not_same_as(expected)
        assertpy.assert_that(actual).is_equal_to(expected)
        assertpy.assert_that(actual).contains_only(type4_object, type5_object, hook)

        actual_items = {type(item).__name__: item for item in actual}
        assertpy.assert_that(actual_items["Hook"].ref).is_same_as(actual)

        assertpy.assert_that(actual_items["Type5"].type4).is_equal_to(actual_items["Type4"])
        assertpy.assert_that(actual_items["Type5"].type4).is_not_same_as(actual_items["Type4"])
        assertpy.assert_that(actual_items["Type4"].type5).is_equal_to(actual_items["Type5"])
        assertpy.assert_that(actual_items["Type4"].type5).is_not_same_as(actual_items["Type5"])


def test_from_json_frozenset_of_attr():
    type5_object = Type5(None, None, None, None, None)
    type4_object = Type4(None, None, None, type5_object, None)
    type5_object.type4 = type4_object
    type5_object_copy = copy.deepcopy(type5_object)
    hook = Hook()
    expected = frozenset([type5_object, type4_object, type5_object_copy, hook])
    hook.ref = expected

    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_not_same_as(expected)
        assertpy.assert_that(actual).is_equal_to(expected)
        assertpy.assert_that(actual).contains_only(type4_object, type5_object, hook)

        actual_items = {type(item).__name__: item for item in actual}
        assertpy.assert_that(actual_items["Hook"].ref).is_same_as(actual)

        assertpy.assert_that(actual_items["Type5"].type4).is_equal_to(actual_items["Type4"])
        assertpy.assert_that(actual_items["Type5"].type4).is_not_same_as(actual_items["Type4"])
        assertpy.assert_that(actual_items["Type4"].type5).is_equal_to(actual_items["Type5"])
        assertpy.assert_that(actual_items["Type4"].type5).is_not_same_as(actual_items["Type5"])
