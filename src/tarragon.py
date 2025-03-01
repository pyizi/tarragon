from typing import Any


def to_json(obj: Any) -> str:
    return "{}"


def from_json(json: str) -> Any:
    raise NotImplementedError()


def to_yaml(obj: Any) -> str:
    raise NotImplementedError()


def from_yaml(yaml: str) -> Any:
    raise NotImplementedError()


def to_xml(obj: Any) -> str:
    raise NotImplementedError()


def from_xml(xml: str) -> Any:
    raise NotImplementedError()
