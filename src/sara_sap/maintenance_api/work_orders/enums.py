from enum import Enum


class PriorityId(str, Enum):
    L = "L"  # Low
    M = "M"  # Medium
    H = "H"  # High
    U = "U"  # Unprior
    D = "D"  # Done
