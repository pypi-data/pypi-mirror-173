import json
from decimal import Decimal
from os import environ
from typing import Callable, Dict, Type, TypeVar, Union, overload

PARSE_MAP: Dict[Type, Callable] = {
    list: json.loads,
    dict: json.loads,
    int: json.loads,
    float: json.loads,
    str: str,
    Decimal: Decimal,
    bool: lambda value: json.loads(value.lower()),
}
ParseableType = TypeVar("ParseableType", list, dict, int, float, str, Decimal, bool)


class Empty:
    pass


empty = Empty()


@overload
def env(
    name: str, *, expected_type: Type[list], default: Union[list, Empty] = empty
) -> list:
    ...


@overload
def env(
    name: str, *, expected_type: Type[dict], default: Union[dict, Empty] = empty
) -> dict:
    ...


@overload
def env(
    name: str, *, expected_type: Type[bool], default: Union[bool, Empty] = empty
) -> bool:
    ...


@overload
def env(
    name: str, *, expected_type: Type[int], default: Union[int, Empty] = empty
) -> int:
    ...


@overload
def env(
    name: str, *, expected_type: Type[float], default: Union[float, Empty] = empty
) -> float:
    ...


@overload
def env(
    name: str, *, expected_type: Type[Decimal], default: Union[Decimal, Empty] = empty
) -> Decimal:
    ...


@overload
def env(
    name: str, *, expected_type: Type[str] = str, default: Union[str, Empty] = empty
) -> str:
    ...


def env(
    name,
    *,
    expected_type=str,
    default=empty,
):
    """
    Returns the environment variable for the given `name` after parsing it to
    the `expected_type`.

    If an environment variable does not exist the `default` value is returned if
    provided. If no `default` is provided it raises KeyError.

    :param name: str
        The name of the environment variable
    :param expected_type: ParseableType
        The data type the environment variable should be parsed to.
    :param default: ParseableType
        The default value to use in case the environment variable doesn't exist.
        This value is not parsed.
    :return: ParseableType
        The parsed environment variable or the default value if not found.
    :raises:
        KeyError:
    """
    parser = PARSE_MAP[expected_type]
    try:
        value = environ[name]
    except KeyError:
        if isinstance(default, Empty):
            raise
        return default
    else:
        return parser(value)
