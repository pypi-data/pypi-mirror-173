from collections import defaultdict
from functools import partial
from operator import getitem
from typing import Any, Callable, Hashable, Iterable, Literal, TypeVar, cast

T = TypeVar("T", bound=dict[Any, Any] | list[Any] | tuple[Any])
K = TypeVar("K", bound=Hashable)
R = TypeVar("R")


count = cast(Callable[[list[T]], int], len)

_apply_methods = {"count": count}


def _groupby(it: list[T] | Iterable[T], key: Callable[[T], K]) -> dict[K, list[T]]:
    d: dict[K, list[T]] = defaultdict(list)
    for i in it:
        d[key(i)].append(i)
    return d


def groupapply(
    it: list[T] | Iterable[T],
    key: K | Callable[[T], K] | None = None,
    apply: Literal["count"] | Callable[[list[T]], R] | None = None,
) -> dict[K, R | list[T] | int]:
    """Group values in an iterable by a key function then apply a function to the
    resultant list of values in each group.

    Parameters
    ----------
    it : Iterable[T]
        Iterable of values to be operated on.
    key : K | Callable[[T], K], optional
        Function to generate a key to group on. Should take an argument of the same type
        as elements of `it` and return a hashable value. A value of `None` is the
        identity function `lambda x: x`. A `str` corresponds to `getitem(T, key)`, by
        default `None`
    apply : &quot;count&quot; | Callable[[list[T]], R], optional
        Function to operator on each group. Should take an argument of a list of the
        same type as elements of `it` and return a hashable value. A value of `None` is
        the identity function `lambda x: x`, by default `None`

    Returns
    -------
    dict[K, R | list[T] | int]
        A dictionary with keys matching the return of the key function and values
        matching the return of the apply function.

    Raises
    ------
    ValueError
        If etiher a non-callable or valid apply option is provided.

    Examples
    --------
    >>> import satchel import groupapply

    >>> string = "AAABBAAAACCB"
    >>> groupapply(string, apply="count")
    {'A': 7, 'B': 3, 'C': 2}

    >>> data = [1, 1, 2, 2, 2, 1, 4]
    >>> groupapply(data, key=lambda x: "lower" if x < 3 else "higher", apply="count")
    {'lower': 6, 'higher': 1}

    >>> data = [
        {"label": "a", "val": 1},
        {"label": "a", "val": 10},
        {"label": "a", "val": 4},
        {"label": "b", "val": 6},
        {"label": "b", "val": 3},
    ]

    >>> groupapply(data, lambda d: d["label"], lambda l: sum([d["val"] for d in l]))
    {'a': 15, 'b': 9}

    >>> data = [
        {"label": "a", "val": 1},
        {"label": "a", "val": 1},
        {"label": "a", "val": 1},
        {"label": "b", "val": 2},
        {"label": "b", "val": 2},
    ]
    >>> groupapply(data, "label", "count")
    {'a': 3, 'b': 2}
    """
    if key is None:
        keyfunc: Callable[[T], K] = lambda x: x  # type: ignore
    elif isinstance(key, str):
        keyfunc = cast(Callable[[T], K], partial(lambda x, k: getitem(x, k), k=key))
    elif callable(key):
        keyfunc = key
    else:
        raise ValueError(
            f"Argument `key` must be a callable or a single value that exists in the internal dictionary. {key=}"
        )

    if apply is None:
        applyfunc: Callable[[list[T]], int | R | list[T]] = lambda x: x
    elif isinstance(apply, str) and apply in _apply_methods:
        applyfunc = _apply_methods[apply]
    elif callable(apply):
        applyfunc = apply
    else:
        raise ValueError(
            f"Argument `apply` must be a callable or {list(_apply_methods.keys())}"
        )

    return {k: applyfunc(g) for k, g in _groupby(it, keyfunc).items()}
