import pyscreenshot as ImageGrab
import numpy as np

from shards import Shard
from memory import ImageMemory


def take_screenshot(resolution=None):
    im = ImageGrab.grab() # Note that you can also screenshot any given bounding box only
    
    if resolution is not None:
        im = im.resize(resolution)

    #im.save(path)

    # Convert to open_cv format
    image = np.array(im.convert('RGB'))[:, :, ::-1]
    return image


class ScreenShard(Shard):

    name = "screenshot"

    def __init__(self, resolution=None, **memory_kwargs):
        self.memory = ImageMemory(**memory_kwargs)
        self.resolution = resolution
        self.state = None

    def reflect(self, rays):
        self.state = take_screenshot(self.resolution)
        return self.state
