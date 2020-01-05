from enum import Flag

# the methods are intentionally backwards to
# make the order reversed.  This is to maintain
# backwards compatibility and not re-do all the
# existing tests.
class ReverseOrderedFlag(Flag):
    # pylint: disable=comparison-with-callable
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented
