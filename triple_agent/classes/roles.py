from enum import Enum, auto

# TODO: add civilian instead of NoRole
class Roles(Enum):
    NoRole = 0
    Spy = auto()
    Ambassador = auto()
    DoubleAgents = auto()
    SeductionTarget = auto()
    Staff = auto()


ROLE_COLORS_TO_ENUM = {
    (178, 204, 178): Roles.Staff,
    (0, 255, 255): Roles.DoubleAgents,
    (0, 0, 255): Roles.SeductionTarget,
    (255, 0, 255): Roles.Ambassador,
    (0, 255, 0): Roles.Spy,
}
