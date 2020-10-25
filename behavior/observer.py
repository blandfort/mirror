import sys
import os
import subprocess
import re


def get_active_window_title():
    """Find the title of the currently active window, using xprop.

    Taken from https://stackoverflow.com/a/42404044"""
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id, 'WM_NAME'], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    match = re.match(b"WM_NAME\(\w+\) = (?P<name>.+)$", stdout)
    if match != None:
        return match.group("name").strip(b'"')

    return None


def get_active_window_info():
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


def show_window_properties():
    root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE)
    stdout, stderr = root.communicate()

    m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\w]+)$', stdout)
    if m != None:
        window_id = m.group(1)
        window = subprocess.Popen(['xprop', '-id', window_id], stdout=subprocess.PIPE)
        stdout, stderr = window.communicate()
    else:
        return None

    for line in stdout.split(b'\n'):
        # We are not interest in contents like icons (which would inflate what is displayed)
        if re.match(b"[_A-Z]{5,}.*", line):
            print(line)


if __name__ == "__main__":
    import time

    while(True):
        #show_window_properties()
        #print()
        print(get_active_window_info())

        time.sleep(1)
