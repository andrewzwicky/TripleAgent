from enum import Enum
from enum import Flag


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


# the methods are intentionally backwards to
# make the order reversed.  This is to maintain
# backwards compatibility and not re-do all the
# existing tests.
class ReverseOrderedEnum(Enum):
    __ge__ = __ge__
    __gt__ = __gt__
    __le__ = __le__
    __lt__ = __lt__


class ReverseOrderedFlag(Flag):
    __ge__ = __ge__
    __gt__ = __gt__
    __le__ = __le__
    __lt__ = __lt__
