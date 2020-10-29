import json
import logging

from memory import replace_float32
from .base import Lens


class LogLens(Lens):
    """Simple Lens to print Reflections of the Mirror
    with a logger."""

    def __init__(self):
        import logger

    def show(self, rays):
        for name, ray in rays.items():
            if self._printable(ray):
                logging.info(f"Shard '{name}': {json.dumps(replace_float32(ray))}")
            else:
                logging.info(f"Shard '{name}': {str(type(ray))}")

    def _printable(self, ray):
        """For a given Ray, check the type to decide whether to include it in the log."""
        if type(ray) in [str, int, float]:
            return True
        if type(ray) is dict:
            if len(ray)<1:
                return True
            return self._printable(list(ray.values())[0])
        if type(ray) in [list, tuple]:
            if len(ray)<1:
                return True
            return self._printable(ray[0])
        return False
