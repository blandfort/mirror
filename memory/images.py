import os
import logging
import cv2 as cv

from .base import Memory


class ImageMemory(Memory):
    """Memory to store images in a designated directory."""

    def __init__(self, logdir, extension='jpg'):
        self.dir = logdir
        self.ext = extension

        # Make sure the directory exists
        if not os.path.isdir(self.dir):
            logging.info("Creating directory '%s' for storing images ..."%self.dir)
            os.makedirs(self.dir)

    def memorize(self, image, id_, title=None):
        name = self._make_name(id_, title)
        image_path = os.path.join(self.dir, name)

        cv.imwrite(image_path, image)
        return image_path

    def remember(self, ids):
        memories = {}
        for id_ in ids:
            memories[id_] = self._remember_id(id_=id_)
        return memories

    def _remember_id(self, id_, title=None):
        name = self._make_name(id_=id_, title=title)
        filepath = os.path.join(self.dir, name)

        if os.path.isfile(filepath):
            return cv.imread(filepath)
        else:
            logging.warning("Couldn't find image with name '%s'!" % name)
            return None

    def search(self, startswith):
        """Find memories with names starting with a given string."""
        return [name for name in os.listdir(self.dir) if name.startswith(startswith)]

    def _make_name(self, id_, title):
        if title is not None:
            return f"{id_}_{title}.{self.ext}"
        else:
            return f"{id_}.{self.ext}"

