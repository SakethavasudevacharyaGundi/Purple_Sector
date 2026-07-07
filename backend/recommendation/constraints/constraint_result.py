from dataclasses import dataclass

@dataclass
class ConstraintResult:
    is_valid:bool
    reason:str | None=None
    