from abc import ABC, abstractmethod


class Memory(ABC):

    @abstractmethod
    def memorize(self, content, id_):
        pass

    @abstractmethod
    def remember(self, id_):
        pass
