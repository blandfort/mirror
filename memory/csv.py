import datetime
import json
import numpy as np

from .base import Memory


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

    def remember(self, ids=None, from_date=None, to_date=None):
        if ids is not None:
            return self._remember_ids(ids=ids)

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

    def _remember_ids(self, ids):
        sids = set([str(id_) for id_ in ids])

        memories = {}
        with open(self.logfile, 'r') as f:
            for line in f:
                parts = self._parse_logline(line)

                if parts is None:
                    continue

                line_id, timestamp, content = parts
                if line_id in sids:
                    memories[line_id] = content
        return {id_: memories[id_] if id_ in memories else None for id_ in sids}

    def _parse_logline(self, line):
        parts = line.strip().split(',', 2)

        if len(parts)<3:
            return None
        return parts[0], datetime.datetime.fromisoformat(parts[1]), json.loads(parts[2])

    def _make_logline(self, results, id_):
        #TODO make this whole thing simpler by using csvwriter
        now = datetime.datetime.now().isoformat()
        return str(id_)+','+now+','+json.dumps(replace_float32(results))+'\n'


