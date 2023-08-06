from collections import OrderedDict
from enum import Enum
from typing import List, Type, TypeVar

from rusty_results import Result, Ok, Err


def parse_str(value: str) -> Result[str, List[str]]:
    if value is not None:
        return Ok(value)
    else:
        return Err(["Cannot parse None as str"])


def parse_int(value: str) -> Result[int, List[str]]:
    try:
        return Ok(int(value))
    except ValueError:
        return Err([f'Cannot parse "{value}" as int'])


TRUE_VALUES = OrderedDict(
    {
        k: None
        for k in [
            "true",
            "t",
            "yes",
            "y",
        ]
    }
)

FALSE_VALUES = OrderedDict(
    {
        k: None
        for k in [
            "false",
            "f",
            "no",
            "n",
        ]
    }
)

ALLOWED_VALUES = list(TRUE_VALUES.keys()) + list(FALSE_VALUES.keys())


def parse_bool(value: str) -> Result[bool, List[str]]:
    l_value = value.strip().lower()
    if l_value in TRUE_VALUES:
        return Ok(True)
    elif l_value in FALSE_VALUES:
        return Ok(False)
    else:
        return Err(
            [f"Unknown value {value}, allowed values are {', '.join(ALLOWED_VALUES)}"]
        )


E = TypeVar("E", bound=Enum)


def parse_enum(value: str, enum_class: Type[E]) -> Result[E, List[str]]:
    u_value = value.strip().upper()
    members = enum_class.__members__
    if u_value in members:
        return Ok(members[u_value])
    else:
        allowed_values = ", ".join(members)
        return Err([f"Unknown value {value}, allowed values are {allowed_values}"])
