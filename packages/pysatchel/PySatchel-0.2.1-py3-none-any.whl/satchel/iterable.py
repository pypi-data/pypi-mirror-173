from typing import Generator, Iterable, Literal, TypeVar

T = TypeVar("T")


def chunk(
    lst: list[T],
    n: int,
    mode: Literal["length", "count"] = "length",
    as_list: bool = False,
) -> Iterable[list[T]]:
    """_summary_

    Parameters
    ----------
    lst : Iterable[T]
        Iterable to be operated on.
    n : int
        Sets the length of chunks for `mode="length"` or number of chunks for `mode="count"`.
    mode : &quot;length&quot; | &quot;count&quot;, optional
        Split the iterable in to chunk of length `n` or `n` chunks, by default `"length"`
    as_list : bool, optional
        Return a generator or a fully resolved list of chunks, by default `False`

    Returns
    -------
    Iterable[list[T]]
        When `as_list=True` returns a list of chunks. `as_list=False` returns a
        generator


    Raises
    ------
    ValueError
        If `n<=0`
    ValueError
        If `mode` is not `"length"` or `"count"`

    Examples
    --------
    >>> import satchel import chunk

    >>> some_list = [1, 2, 3, 4, 5]
    >>> chunk(some_list, 2, "length", True)
    [[1, 2], [3, 4], [5]]

    >>> chunk(some_list, 2, "count", True)
    [[1, 2, 3], [3, 5]]
    """
    length = {"length": n, "count": -(len(lst) // -n)}.get(mode, None)
    if length is None:
        raise ValueError(f"Invalid mode: {mode}. Accepted values: ('length', 'count').")

    if n <= 0:
        raise ValueError("`n` must be greater than 0.")
    chunked: list[list[T]] | Generator[list[T], None, None] = (
        lst[i : i + length] for i in range(0, len(lst), length)
    )
    if as_list:
        chunked = list(chunked)
    return chunked
