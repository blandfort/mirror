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

