from abc import ABC
from abc import abstractmethod
from recommendation.constraints.constraint_result import ConstraintResult

class BaseConstraint(ABC):
    @abstractmethod
    def validate(self, race_state, driver_state, candidate) -> ConstraintResult:
        pass