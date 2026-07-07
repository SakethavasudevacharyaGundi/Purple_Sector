from enum import Enum

class LapRegime(str,Enum):
    GREEN = "GREEN"
    SAFETY_CAR = "SAFETY_CAR"
    RED_FLAG = "RED_FLAG"
    PIT_IN = "PIT_IN"
    PIT_OUT = "PIT_OUT"
    UNKNOWN = "UNKNOWN"