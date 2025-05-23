from abc import ABC, abstractmethod

class Controller(ABC):
    @abstractmethod
    def CreateUser(self):
        pass