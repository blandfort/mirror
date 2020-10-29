# Path settings
MIRRORLOG = 'logs/mirror.log'
EMOTIONLOG = 'logs/emotions.log'
WINDOWLOG = 'logs/windows.log'
SCREENSHOT_DIR = 'logs/screenshots/'
CAMSHOT_DIR = 'logs/cam/'

# Logging behavior
TIMESTEP = 1.  # How often we log (in seconds)
SCREENSHOT_RESOLUTION = (1000,500)
# How often we take screenshots and cam captures, based on detected emotions
SCREENSHOT_FREQUENCIES = {'neutral': 50, 'other': 2}
CAM_FREQUENCIES = {'neutral': 20, 'other': 1}

# Hardware settings
DEVICE = 'cpu'
