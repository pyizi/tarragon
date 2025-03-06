from assertpy import assertpy

import tarragon


def test_from_json_complex():
    expected = complex(1, 2)
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_int():
    expected = 1
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_float():
    expected = 1.1
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_bool():
    expected = True
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_str():
    expected = "hello"
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_None():
    expected = None
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_exception():
    expected = Exception("test")
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_class():
    class expected:
        """doc: class expected"""
        pass

    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_function():
    def expected():
        return 42

    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_equal_to(expected)

        assertpy.assert_that(actual()).is_equal_to(42)

        assertpy.assert_that(expected()).is_equal_to(42)


def test_from_json_iter():
    ab = ["a", "b"]
    cd = ["c", "d"]
    lst = [cd, ab, cd, ab]
    expected = iter(lst)
    next(expected)

    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_equal_to(expected)

        actual_list = list(actual)
        assertpy.assert_that(actual_list).is_equal_to([ab, cd, ab])
        assertpy.assert_that(id(actual_list[0])).is_equal_to(id(actual_list[2]))
        assertpy.assert_that(id(actual_list[0])).is_not_equal_to(id(actual_list[1]))
        assertpy.assert_that(list(actual)).is_empty()

        expected_list = list(expected)
        assertpy.assert_that(expected_list).is_equal_to([ab, cd, ab])
        assertpy.assert_that(id(actual_list[0])).is_not_equal_to(id(ab))
        assertpy.assert_that(list(expected)).is_empty()


def test_from_json_range():
    expected = range(3)
    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_equal_to(expected)

        assertpy.assert_that(list(actual)).is_equal_to([0, 1, 2])
        assertpy.assert_that(list(actual)).is_equal_to([0, 1, 2])

        assertpy.assert_that(list(expected)).is_equal_to([0, 1, 2])
        assertpy.assert_that(list(expected)).is_equal_to([0, 1, 2])


def test_from_json_map():
    a = [1]
    b = [2]
    expected = map(lambda x: x * 2, [b, a, b, a])
    next(expected)

    actual = tarragon.from_json(tarragon.to_json(expected))

    with assertpy.soft_assertions():
        assertpy.assert_that(actual).is_equal_to(expected)

        actual_list = list(actual)
        assertpy.assert_that(actual_list).is_equal_to([a, b, a])
        assertpy.assert_that(id(actual_list[0])).is_equal_to(id(actual_list[2]))
        assertpy.assert_that(id(actual_list[0])).is_not_equal_to(id(actual_list[1]))
        assertpy.assert_that(list(actual)).is_empty()

        expected_list = list(expected)
        assertpy.assert_that(expected_list).is_equal_to([a, b, a])
        assertpy.assert_that(id(actual_list[0])).is_equal_to(id(a))
        assertpy.assert_that(list(actual)).is_empty()


def test_from_json_object():
    expected = object()
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_bytes():
    expected = b"123"
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_bytearray():
    expected = bytearray(b"123")
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)


def test_from_json_memoryview():
    expected = memoryview(b"123")
    actual = tarragon.from_json(tarragon.to_json(expected))

    assertpy.assert_that(actual).is_equal_to(expected)
