import logging
import os


class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super().formatException(exc_info)
        return repr(result)

    def format(self, record):
        result = super().format(record)
        if record.exc_text:
            result = result.replace("\n", "")
        return result

logfile = os.environ.get("LOGFILE", None)
if logfile is not None:
    handler = logging.FileHandler(logfile)
else:
    handler = logging.StreamHandler()

formatter = OneLineExceptionFormatter('[%(asctime)s] [%(levelname)s] %(message)s [%(filename)s, line %(lineno)d]')
handler.setFormatter(formatter)

root = logging.getLogger()
root.setLevel(os.environ.get("LOGLEVEL", "INFO"))
root.addHandler(handler)
