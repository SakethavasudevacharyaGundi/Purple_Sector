from abc import ABC, abstractmethod

class BaseFeature(ABC):
    @abstractmethod
    def extract(self,race_state, driver_state)->dict:
        pass