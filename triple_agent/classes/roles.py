from enum import Enum, auto


class Roles(Enum):
    Civilian = 0
    Spy = auto()
    Ambassador = auto()
    DoubleAgent = auto()
    SeductionTarget = auto()
    Staff = auto()
    SuspectedDoubleAgent = auto()


ROLE_COLORS_TO_ENUM = {
    (178, 204, 178): Roles.Staff,
    (0, 255, 255): Roles.DoubleAgent,
    (0, 0, 255): Roles.SeductionTarget,
    (255, 0, 255): Roles.Ambassador,
    (0, 255, 0): Roles.Spy,
}
