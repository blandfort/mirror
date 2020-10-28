import datetime
import os
import json
import numpy as np


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


class CSVMemory:
    """Simple memory to store data in a single log file in CSV format."""

    def __init__(self, logfile):
        self.logfile = logfile

    def memorize(self, content, id_):
        line = self._make_logline(content, id_)

        with open(self.logfile, 'a') as f:
            f.write(line)

    def _make_logline(self, results, id_):
        #TODO make this whole thing simpler by using csvwriter
        now = datetime.datetime.now().isoformat()
        return str(id_)+','+now+','+json.dumps(replace_float32(results))+'\n'


import cv2 as cv

class ImageMemory:
    """Memory to store images in a designated directory."""

    def __init__(self, logdir, extension='png'):
        self.dir = logdir
        self.ext = extension

    def memorize(self, image, id_, title=None):
        name = self._make_name(id_, title)
        image_path = os.path.join(self.dir, name)

        cv.imwrite(image_path, image)
        #TODO if the directory doesn't exist, the writing doesn't work,
        # but this doesn't seem to appear anywhere in the log
        return image_path

    def _make_name(self, id_, title):
        if title is not None:
            return f"{id_}_{title}.{self.ext}"
        else:
            return f"{id_}.{self.ext}"

