import sys
import os
import subprocess
import re


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


import pyscreenshot as ImageGrab

def take_screenshot(resolution=None):
    im = ImageGrab.grab() # Note that you can also screenshot any given bounding box only
    
    if resolution is not None:
        im = im.resize(resolution)

    #im.save(path)
    return path


class ScreenShard(Shard):

    name = "screenshot"

    def __init__(self, resolution=None, **memory_kwargs):
        self.memory = ImageMemory(**memory_kwargs)
        self.resolution = resolution

    def reflect(self, rays):
        self.state = take_screenshot(self.resolution)
        return self.state
