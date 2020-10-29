import sys
import os
import subprocess
import re

from shards import Shard
from memory import CSVMemory


class WindowShard(Shard):

    name = "active_window"

    def __init__(self, logfile):
        self.memory = CSVMemory(logfile=logfile)
        self.state = None

    def reflect(self, rays):
        self.state = self._get_active_window_info()
        return self.state

    def _get_active_window_info(self):
        """Find information about the currently active window, using xprop."""
        root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
        stdout, stderr = root.communicate()

        m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
        if m != None:
            window_id = m.group(1)
            window = subprocess.Popen(['xprop', '-id', window_id], stdout=subprocess.PIPE)
            stdout, stderr = window.communicate()
        else:
            return None

        info = {}
        for line in stdout.split(b'\n'):
            match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", line)
            if match is not None:
                info['title'] = match.group("name").strip(b'"').decode('utf-8')

            match = re.match(b"WM_CLASS\(\w+\) = (?P<class>.+)$", line)
            if match is not None:
                info['class'] = match.group("class").decode('utf-8').replace('"', '') #.strip(b'"')

        if len(info):
            return info
        else:
            return None

