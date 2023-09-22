import bisect

class SortedList(list):
    """
    A list with insort.
    """

    def insort(self, value):
        bisect.insort(self, value)
