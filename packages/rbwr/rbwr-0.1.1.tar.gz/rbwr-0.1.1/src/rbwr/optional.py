"""
Extension functions for `typing.Optional`
"""

from typing import Callable, Optional, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def map(opt: T, f: Callable[[T], U]) -> Optional[U]:
    """
    Convert an `Optional[T]` to `Optional[U]` via a function of `T -> U`
    """

    return f(opt) if opt is not None else None
