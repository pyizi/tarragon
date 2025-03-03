def __get_ref(type_id: int | None) -> str:
    return "null" if type_id is None else f'{{ "ref_id": {type_id} }}'


def type6(uid, type1_id, type2_id, type3_id, type4_id, type5_id, next_id=0) -> str:
    """After this method next_id will be = next_id + 1"""

    return f"""{{
    "type": "tests.model.foo.bar.model_too.Type6",
    "id": {next_id},
    "object": {{
        "uid": {uid},
        "_name": "say my name",
        "type1": {__get_ref(type1_id)},
        "type2": {__get_ref(type2_id)},
        "type3": {__get_ref(type3_id)},
        "type4": {__get_ref(type4_id)},
        "type5": {__get_ref(type5_id)}
    }}
}}"""


def type5(type1_id, type2_id, type3_id, type4_id, type6_id, next_id=0) -> str:
    """After this method next_id will be = next_id + 2"""

    return f"""{{
    "type": "tests.model.foo.bar.model_too.Type5",
    "id": {next_id},
    "object": {{
        "_Type5__type6": {type6(12, type1_id, type2_id, type3_id, type4_id, next_id, next_id + 1)},
        "type1": {__get_ref(type1_id)},
        "type2": {__get_ref(type2_id)},
        "type3": {__get_ref(type3_id)},
        "type4": {__get_ref(type4_id)},
        "type6": {__get_ref(type6_id)}
    }}
}}"""


def type4(type1_id, type2_id, type3_id, type5_id, type6_id, next_id=0) -> str:
    """After this method next_id will be = next_id + 8"""

    return f"""{{
    "type": "tests.model.foo.model.Type4",
    "id": {next_id},
    "object": {{
        "x": 7,
        "y": {{
            "type": "dict",
            "id": {next_id + 1},
            "items": [
                {{
                    "key": "a",
                    "value": "a"
                }},
                {{
                    "key": "b",
                    "value": {type5(type1_id, type2_id, type3_id, next_id, type6_id, next_id + 2)}
                }},
                {{
                    "key": "c",
                    "value": "c"
                }}
            ]
        }},
        "z": {{
            "type": "tuple",
            "id": {next_id + 4},
            "array": [1, 2, 3]
        }},
        "w": {{
            "type": "set",
            "id": {next_id + 5},
            "array": [
                1, 
                {type6(123, type1_id, type2_id, type3_id, next_id, type5_id, next_id + 6)}, 
                3
            ]
        }},
        "lst": {{
            "type": "list",
            "id": {next_id + 7},
            "array": [0, 1, 2]
        }},
        "type1": {__get_ref(type1_id)},
        "type2": {__get_ref(type2_id)},
        "type3": {__get_ref(type3_id)},
        "type5": {__get_ref(type5_id)},
        "type6": {__get_ref(type6_id)}
    }}
}}"""


def type3(type1_id, type2_id, type4_id, type5_id, type6_id, next_id=0) -> str:
    """After this method next_id will be = next_id + 15"""

    return f"""{{
    "type": "tests.model.foo.model.Type3",
    "id": {next_id},
    "object": {{
        "_type5": {type5(type1_id, type2_id, next_id, type4_id, type6_id, next_id + 1)},
        "_Type3__dct": {{
            "type": "dict",
            "id": {next_id + 3},
            "items": [
                {{
                    "key": {type5(type1_id, type2_id, next_id, type4_id, type6_id, next_id + 4)},
                    "value": "3"
                }},
                {{
                    "key": {type6(7, type1_id, type2_id, next_id, type4_id, type5_id, next_id + 6)},
                    "value": {type4(type1_id, type2_id, next_id, type5_id, type6_id, next_id + 7)}
                }}
            ]
        }},
        "y": 45,
        "_tui": 43,
        "o": 321,
        "type1": {__get_ref(type1_id)},
        "type2": {__get_ref(type2_id)},
        "type4": {__get_ref(type4_id)},
        "type5": {__get_ref(type5_id)},
        "type6": {__get_ref(type6_id)}        
    }}
}}"""


def type2(type1_id, type3_id, type4_id, type5_id, type6_id, next_id=0) -> str:
    """After this method next_id will be = next_id + 43"""

    return f"""{{
    "type": "tests.model.model.Type2",
    "id": {next_id},
    "object": {{
        "_Type2__Y": {{
            "type": "list",
            "id": {next_id + 1},
            "array": [1, true, 3]
        }},
        "Z": {{
            "type": "tuple",
            "id": {next_id + 2},
            "array": [1, 2, false]
        }},
        "W": {{
            "type": "set",
            "id": {next_id + 3},
            "array": [1, 2, 3]
        }},
        "_S": {{
            "type": "set",
            "id": {next_id + 4},            
            "array": [
                {type5(type1_id, next_id, type3_id, type4_id, type6_id, next_id + 5)}, 
                {type6(6, type1_id, next_id, type3_id, type4_id, type5_id, next_id + 7)}
            ]
        }},
        "L": {{
            "type": "list",
            "id": {next_id + 8},
            "array": [
                {type3(type1_id, next_id, type4_id, type5_id, type6_id, next_id + 9)}, 
                {type4(type1_id, next_id, type3_id, type5_id, type6_id, next_id + 24)}
            ]
        }},
        "_Type2__T": {{
            "type": "tuple",
            "id": {next_id + 32},
            "array": [
                {type4(type1_id, next_id, type3_id, type5_id, type6_id, next_id + 33)}, 
                {type5(type1_id, next_id, type3_id, type4_id, type6_id, next_id + 41)} 
            ]
        }},
        "type1": {__get_ref(type1_id)},
        "type3": {__get_ref(type3_id)},
        "type4": {__get_ref(type4_id)},
        "type5": {__get_ref(type5_id)},
        "type6": {__get_ref(type6_id)}   
    }}
}}"""


def type1(y: str, next_id=0) -> str:
    """After this method next_id will be = next_id + 44"""

    return f"""{{
    "type": "tests.model.model.Type1",
    "id": {next_id},
    "object": {{
        "_y": "{y}",
        "a": 1,
        "_b": "2",
        "_Type1__type": {type2(next_id, None, None, None, None, next_id + 1)},
        "_Type1__c": 3.0
    }}
}}"""
