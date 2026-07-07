from dataclasses import dataclass


@dataclass(frozen=True)
class TyreProfile:

    min_stint: int

    max_stint: int


TYRE_PROFILES = {

    "SOFT": TyreProfile(
        min_stint=5,
        max_stint=25,
    ),

    "MEDIUM": TyreProfile(
        min_stint=10,
        max_stint=45,
    ),

    "HARD": TyreProfile(
        min_stint=15,
        max_stint=80,
    ),
}