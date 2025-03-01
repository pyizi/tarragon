def type6(uid) -> str:
    return f"""{{
    "type": "tests.model.foo.bar.model_too.Type6",
    "object": {{
        "uid": {uid},
        "_name": "say my name"
    }}
}}"""


def type5() -> str:
    return f"""{{
    "type": "tests.model.foo.bar.model_too.Type5",
    "object": {{
        "_Type5__type6": {type6(12)}
    }}
}}"""


def type4() -> str:
    return f"""{{
    "type": "tests.model.foo.model.Type4",
    "object": {{
        "x": 7,
        "y": {{
            "type": "dict",
            "items": [
                {{
                    "key": "a",
                    "value": "a"
                }},
                {{
                    "key": "b",
                    "value": {type5()}
                }},
                {{
                    "key": "c",
                    "value": "c"
                }}
            ]
        }},
        "z": {{
            "type": "tuple",
            "array": [1, 2, 3]
        }},
        "w": {{
            "type": "set",
            "array": [
                1, 
                {type6(123)}, 
                3
            ]
        }},
        "lst": [0, 1, 2]
    }}
}}"""


def type3() -> str:
    return f"""{{
    "type": "tests.model.foo.model.Type3",
    "object": {{
        "type5": {type5()},
        "_Type3__dct": {{
            "type": "dict",
            "items": [
                {{
                    "key": {type5()},
                    "value": "3"
                }},
                {{
                    "key": {type6(7)},
                    "value": {type4()}
                }}
            ]
        }}
    }}
}}"""


def type2() -> str:
    return f"""{{
    "type": "tests.model.model.Type2",
    "object": {{
        "_Type2__Y": [1, true, 3],
        "Z": {{
            "type": "tuple",
            "array": [1, 2, false]
        }},
        "W": {{
            "type": "set",
            "array": [1, 2, 3]
        }},
        "_S": {{
            "type": "set",
            "array": [{type5()}, {type6(6)}]
        }},
        "L": [{type3()}, {type4()}],
        "_Type2__T": {{
            "type": "tuple",
            "array": [{type4()}, {type5()}]
        }}
    }}
}}"""


def type1(y: str) -> str:
    return f"""{{
    "type": "tests.model.model.Type1",
    "object": {{
        "_y": "{y}",
        "a": 1,
        "_b": "2",
        "_Type1__type": {type2()},
        "_Type1__c": 3.0
    }}
}}"""
