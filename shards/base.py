from abc import ABC, abstractmethod


class Shard(ABC):
    """Shards are components of a Mirror.

    Initialize one to catch and reflect particular Rays of Behavior."""

    def __init__(self):
        self.memory = None
        self.state = None

    @abstractmethod
    def reflect(self, rays: dict):
        """Update and return the current state."""
        pass

    def memorize(self, id_):
        """Memorize the current state."""
        if self.memory is not None and self.state is not None:
            self.memory.memorize(self.state, id_=id_)

    def remember(self, ids):
        if self.memory is not None:
            return self.memory.remember(ids=ids)
        else:
            return None
