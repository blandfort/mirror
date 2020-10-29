from abc import ABC, abstractmethod


class Lens(ABC):

    @abstractmethod
    def show(self, rays):
        pass

