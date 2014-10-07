from pickle import IntType, LongType, FloatType
import logging
import os
import platform
import sys
import tempfile
import urllib2
import zipfile
import re

try:
    import cv2
except ImportError:
    raise ImportError("Cannot load OpenCV(cv2) library which is required by "
                      "simplecv")


# optional libraries
PIL_ENABLED = True
try:
    from PIL import Image as PilImage
    from PIL import ImageFont as pilImageFont
    from PIL import ImageDraw as pilImageDraw
    from PIL import GifImagePlugin

    getheader = GifImagePlugin.getheader
    getdata = GifImagePlugin.getdata
except ImportError:
    try:
        import Image as PilImage
        from GifImagePlugin import getheader, getdata
    except ImportError:
        PIL_ENABLED = False


def convert_camel_case_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


#couple quick typecheck helper functions
def is_number(n):
    """
    Determines if it is a number or not

    Returns: Type
    """
    return type(n) in (IntType, LongType, FloatType)


def is_tuple(n):
    """
    Determines if it is a tuple or not

    Returns: Boolean
    """
    return type(n) == tuple


def reverse_tuple(n):
    """
    Reverses a tuple

    Returns: Tuple
    """
    return tuple(reversed(n))


def test():
    """
    This function is meant to run builtin unittests
    """

    print 'unit test'


def download_and_extract(url):
    """
    This function takes in a url for a zip file, extracts it and returns
    the temporary path it was extracted to
    """
    if url is None:
        logger.warning("Please provide url")
        return None

    tmpdir = tempfile.mkdtemp()
    filename = os.path.basename(url)
    path = tmpdir + "/" + filename
    zdata = urllib2.urlopen(url)

    print "Saving file to disk please wait...."
    with open(path, "wb") as local_file:
        local_file.write(zdata.read())

    zfile = zipfile.ZipFile(path)
    print "Extracting zipfile"
    try:
        zfile.extractall(tmpdir)
    except:
        logger.warning("Couldn't extract zip file")
        return None

    return tmpdir


def int_to_bin(i):
    """Integer to two bytes"""
    i1 = i % 256
    i2 = int(i / 256)
    return chr(i1) + chr(i2)


#Logging system - Global elements

consoleHandler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)s: %(message)s')
consoleHandler.setFormatter(formatter)
logger = logging.getLogger('Main Logger')
logger.addHandler(consoleHandler)

try:
    import IPython

    ipython_version = IPython.__version__
except ImportError:
    ipython_version = None


def on_ipython_notebook():
        try:
            config = get_ipython().config
            return config['IPKernelApp']['parent_appname'] == 'ipython-notebook'
        except:
            return False


#This is used with sys.excepthook to log all uncaught exceptions.
#By default, error messages ARE print to stderr.
def exception_handler(exc_type, exc_value, traceback):
    logger.error("", exc_info=(exc_type, exc_value, traceback))

    #print "Hey!",exc_value
    #exc_value has the most important info about the error.
    #It'd be possible to display only that and hide all the (unfriendly) rest.


sys.excepthook = exception_handler


def ipython_exception_handler(shell, exc_type, exc_value, traceback,
                              tb_offset=0):
    logger.error("", exc_info=(exc_type, exc_value, traceback))


#The two following functions are used internally.
def init_logging(log_level):
    logger.setLevel(log_level)


def read_logging_level(log_level):
    levels_dict = {
        1: logging.DEBUG, "debug": logging.DEBUG,
        2: logging.INFO, "info": logging.INFO,
        3: logging.WARNING, "warning": logging.WARNING,
        4: logging.ERROR, "error": logging.ERROR,
        5: logging.CRITICAL, "critical": logging.CRITICAL
    }

    if isinstance(log_level, str):
        log_level = log_level.lower()

    if log_level in levels_dict:
        return levels_dict[log_level]
    else:
        print "The logging level given is not valid"
        return None


def get_logging_level():
    """
    This function prints the current logging level of the main logger.
    """
    levels_dict = {
        10: "DEBUG",
        20: "INFO",
        30: "WARNING",
        40: "ERROR",
        50: "CRITICAL"
    }

    print "The current logging level is:", levels_dict[
        logger.getEffectiveLevel()]


def set_logging(log_level, myfilename=None):
    """
    This function sets the threshold for the logging system and, if desired,
    directs the messages to a logfile. Level options:

    'DEBUG' or 1
    'INFO' or 2
    'WARNING' or 3
    'ERROR' or 4
    'CRITICAL' or 5

    If the user is on the interactive shell and wants to log to file, a custom
    excepthook is set. By default, if logging to file is not enabled, the way
    errors are displayed on the interactive shell is not changed.
    """

    if myfilename and ipython_version:
        try:
            if ipython_version.startswith("0.10"):
                __IPYTHON__.set_custom_exc((Exception,),
                                           ipython_exception_handler)
            else:
                ip = get_ipython()
                ip.set_custom_exc((Exception,), ipython_exception_handler)
        except NameError:  # In case the interactive shell is not being used
            sys.exc_clear()

    level = read_logging_level(log_level)

    if level and myfilename:
        file_handler = logging.FileHandler(filename=myfilename)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.removeHandler(consoleHandler)  # Console logging is disabled.
        print "Now logging to", myfilename, "with level", log_level
    elif level:
        print "Now logging with level", log_level

    logger.setLevel(level)


def system():
    """

    **SUMMARY**

    Output of this function includes various informations related to system and
    library.

    Main purpose:
    - While submiting a bug, report the output of this function
    - Checking the current version and later upgrading the library based on the
      output

    **RETURNS**

    None

    **EXAMPLE**

      >>> import simplecv
      >>> simplecv.system()


    """
    try:
        import platform

        print "System : ", platform.system()
        print "OS version : ", platform.version()
        print "Python version :", platform.python_version()
        print "Open CV2 version : " + cv2.__version__

        if PIL_ENABLED:
            print "PIL version : ", PilImage.VERSION
        else:
            print "PIL module not installed"

        try:
            import pickle
            print "Pickle Version : " + pickle.__version__
        except:
            print "Pickle module not installed"

    except ImportError:
        print "You need to install Platform to use this function"
        print "to install you can use:"
        print "easy_install platform"
    return


class ScvException(Exception):
    pass


class LazyProperty(object):
    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__

    def __get__(self, obj, klass=None):
        if obj is None:
            return None
        result = obj.__dict__[self.__name__] = self._func(obj)
        return result


def lazyproperty(fn):
    attr_name = '_lazy_' + fn.__name__
    @property
    def _lazyprop(self):
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)
    return _lazyprop


def force_update_lazyproperties(obj):
    for p in dir(obj):
        if p.startswith('_lazy_'):
            delattr(obj, p)


#supported image formats regular expression ignoring case
IMAGE_FORMATS = ('*.[bB][mM][Pp]', '*.[Gg][Ii][Ff]',     '*.[Jj][Pp][Gg]',
                 '*.[jJ][pP][eE]', '*.[jJ][Pp][Ee][Gg]', '*.[pP][nN][gG]',
                 '*.[pP][bB][mM]', '*.[pP][gG][mM]',     '*.[pP][pP][mM]',
                 '*.[tT][iI][fF]', '*.[tT][iI][fF][fF]', '*.[wW][eE][bB][pP]')

LAUNCH_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__)))
SYSTEM = platform.system()
