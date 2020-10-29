import datetime
import os
import json
import logging
import numpy as np

from abc import ABC, abstractmethod


def replace_float32(obj):
    """Utility function to recursively convert float32 entries to float,
    so the object can be converted to JSON."""
    if type(obj) is dict:
        r = {}
        for key,value in obj.items():
            if type(value) is np.float32:
                r[key] = float(value)
            elif type(value) in [dict, list, tuple]:
                r[key] = replace_float32(value)
            else:
                r[key] = value
        return r
    elif type(obj) is list or type(obj) is tuple:
        r = []
        for value in obj:
            if type(value) is np.float32:
                r.append(float(value))
            elif type(value) in [dict, list, tuple]:
                r.append(replace_float32(value))
            else:
                r.append(value)
        return r
    else:
        raise Exception("Not implemented!")


class Memory(ABC):

    @abstractmethod
    def memorize(self, content, id_):
        pass

    @abstractmethod
    def remember(self, id_):
        pass

class CSVMemory(Memory):
    """Simple memory to store data in a single log file in CSV format."""

    def __init__(self, logfile):
        self.logfile = logfile

        # Make sure the logfile exists
        open(self.logfile, 'a').close()

    def memorize(self, content, id_):
        line = self._make_logline(content, id_)

        with open(self.logfile, 'a') as f:
            f.write(line)
        return line

    def remember(self, id_=None, from_date=None, to_date=None):
        if id_ is not None:
            return self._remember_id(id_=id_)

        memories = {}
        with open(self.logfile, 'r') as f:
            for line in f:
                parts = self._parse_logline(line)

                if parts is None:
                    continue
                line_id, timestamp, content = parts

                if from_date is not None and from_date>timestamp:
                    continue
                if to_date is not None and to_date<timestamp:
                    continue

                memories[line_id] = content
        return memories

    def _remember_id(self, id_):
        sid = str(id_)

        with open(self.logfile, 'r') as f:
            for line in f:
                parts = self._parse_logline(line)

                if parts is None:
                    continue

                line_id, timestamp, content = parts
                if line_id==str(sid):
                    return content
        return None

    def _parse_logline(self, line):
        parts = line.strip().split(',', 2)

        if len(parts)<3:
            return None
        return parts[0], datetime.datetime.fromisoformat(parts[1]), json.loads(parts[2])

    def _make_logline(self, results, id_):
        #TODO make this whole thing simpler by using csvwriter
        now = datetime.datetime.now().isoformat()
        return str(id_)+','+now+','+json.dumps(replace_float32(results))+'\n'


import cv2 as cv


class ImageMemory(Memory):
    """Memory to store images in a designated directory."""

    def __init__(self, logdir, extension='png'):
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

    def remember(self, id_, title=None):
        name = self._make_name(id_=id_, title=title)
        filepath = os.path.join(self.dir, name)

        if os.path.isfile(filepath):
            return cv.imread(filepath)
        else:
            logging.warning("Couldn't find image with name '%s'!" % name)
            return None

    def _make_name(self, id_, title):
        if title is not None:
            return f"{id_}_{title}.{self.ext}"
        else:
            return f"{id_}.{self.ext}"

