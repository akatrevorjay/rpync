import json

from platform                            import system
from rpync.common.fileinfo.base          import FileInfo, TIME_FORMAT
from rpync.common.fileinfo.fileinfo_unix import FileInfoUnix

SUPPORTED_PLATFORMS = {
    'Unix' : FileInfoUnix,
    'Linux': FileInfoUnix,
}

def make(path, basepath=None):
    platform = system()
    try:
        fileinfo = SUPPORTED_PLATFORMS[platform]()
        fileinfo.__make__(path, basepath, platform)
        return fileinfo
    except KeyError, e:
        raise IOError, "Unsupported platform: " + platform

def __loadinfo__(value):
    try:
        platform = value[u'platform']
    except KeyError, e:
        raise ValueError, "Missing platform attribute"
    try:
        fileinfo = SUPPORTED_PLATFORMS[platform]()
        fileinfo.__setinfo__(value)
        return fileinfo
    except KeyError, e:
        raise IOError, "Unsupported platform: " + platform

def load(fp, *args, **kwargs):
    return __loadinfo__(json.load(fp, *args, **kwargs))

def loads(value, *args, **kwargs):
    return __loadinfo__(json.loads(value, *args, **kwargs))

