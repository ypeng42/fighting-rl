"""
Solution module providing a median function.
"""

from typing import List, Sequence, Union

Number = Union[int, float]


def median(data: Sequence[Number]) -> float:
    """Return the median of a non‑empty sequence of numbers.

    The function works for any sequence (list, tuple, etc.) containing
    numeric values.  If the sequence is empty a ``ValueError`` is raised
    (as required by the tests).  For an even number of elements the
    median is the arithmetic mean of the two central values.

    Parameters
    ----------
    data:
        A sequence of numeric values.

    Returns
    -------
    float
        The median value.
    """
    # Convert to list to allow sorting without modifying the original
    # sequence and to support any generic ``Sequence`` type.
    if not data:
        raise ValueError("median of empty list")

    # Sorting creates a new ordered list; this works for any comparable
    # numbers (ints, floats, Decimals, etc.).
    sorted_data: List[Number] = sorted(data)
    n = len(sorted_data)
    mid = n // 2

    if n % 2:
        # Odd length – the middle element is the median.
        return float(sorted_data[mid])
    else:
        # Even length – average the two middle elements.
        low = sorted_data[mid - 1]
        high = sorted_data[mid]
        return (float(low) + float(high)) / 2.0
