from enum import Enum
from enum import Flag


def __enum_ge__(self, other):
    if self.__class__ is other.__class__:
        return self.value >= other.value
    return NotImplemented


def __enum_gt__(self, other):
    if self.__class__ is other.__class__:
        return self.value > other.value
    return NotImplemented


def __enum_le__(self, other):
    if self.__class__ is other.__class__:
        return self.value <= other.value
    return NotImplemented


def __enum_lt__(self, other):
    if self.__class__ is other.__class__:
        return self.value < other.value
    return NotImplemented


# the methods are intentionally backwards to
# make the order reversed.  This is to maintain
# backwards compatibility and not re-do all the
# existing tests.
class ReverseOrderedEnum(Enum):
    __ge__ = __enum_le__
    __gt__ = __enum_lt__
    __le__ = __enum_ge__
    __lt__ = __enum_gt__


class ReverseOrderedFlag(Flag):
    __ge__ = __enum_le__
    __gt__ = __enum_lt__
    __le__ = __enum_ge__
    __lt__ = __enum_gt__


# These are set up to be ordered based on name rather than value
# so that newly inserted values don't mess up the order
# because new enum values must be put at the end.
def __ge__stringify__(self, other):
    if self.__class__ is other.__class__:
        try:
            return self.alpha_sort() >= other.alpha_sort()
        except AttributeError:
            return self.stringify() >= other.stringify()
    return NotImplemented


def __gt__stringify__(self, other):
    if self.__class__ is other.__class__:
        try:
            return self.alpha_sort() > other.alpha_sort()
        except AttributeError:
            return self.stringify() > other.stringify()
    return NotImplemented


def __le__stringify__(self, other):
    if self.__class__ is other.__class__:
        try:
            return self.alpha_sort() <= other.alpha_sort()
        except AttributeError:
            return self.stringify() <= other.stringify()
    return NotImplemented


def __lt__stringify__(self, other):
    if self.__class__ is other.__class__:
        try:
            return self.alpha_sort() < other.alpha_sort()
        except AttributeError:
            return self.stringify() < other.stringify()
    return NotImplemented


class OrderedStringifyEnum(Enum):
    __ge__ = __ge__stringify__
    __gt__ = __gt__stringify__
    __le__ = __le__stringify__
    __lt__ = __lt__stringify__
