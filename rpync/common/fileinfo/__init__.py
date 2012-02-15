from rpync.common.fileinfo.fileinfo_unix import FileinfoUnix

SUPPORTED_PLATFORMS = {'Linux': FileinfoUnix,}

def getFileinfo(path, basepath=None):
    import platform

    system = platform.system()
    try:
        return SUPPORTED_PLATFORMS[system](path, basepath)
    except KeyError, e:
        raise IOError, "Unsupported platform: " + system
