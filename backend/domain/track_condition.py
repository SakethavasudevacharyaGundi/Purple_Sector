# backend/domain/track_condition.py

from enum import StrEnum


class TrackCondition(StrEnum):
    UNKNOWN = "UNKNOWN"
    ALL_CLEAR = "ALL_CLEAR"
    YELLOW = "YELLOW"
    SAFETY_CAR = "SAFETY_CAR"
    RED_FLAG = "RED_FLAG"