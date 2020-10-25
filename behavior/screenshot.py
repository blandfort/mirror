# Simple script that takes a screenshot upon load
import pyscreenshot as ImageGrab

def take_screenshot(path, resolution=None):
    im = ImageGrab.grab() # Note that you can also screenshot any given bounding box only
    
    if resolution is not None:
        im = im.resize(resolution)

    im.save(path)
