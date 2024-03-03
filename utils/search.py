def bisect_left(array, target, left: int = 0, right: int = None):
    """
    Return the leftmost index of target in iterable.
    """

    if right is None:
        right = len(array)

    while left < right:
        mid = left + (right - left) // 2

        if array[mid] < target:
            left = mid + 1
        else:
            right = mid

    return left
