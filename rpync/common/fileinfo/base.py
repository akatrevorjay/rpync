import os
import os.path

from stat import *

class Fileinfo(object):
    def __init__(self, path, basepath, platform):
        assert isinstance(path, basestring)
        if basepath is not None:
            assert os.path.isdir(basepath)
            assert os.path.isabs(basepath)
            basepath = os.path.normpath(basepath)
            fullpath = os.path.join(basepath, path)
        else:
            assert os.path.isabs(path)
            fullpath = path
            basepath = '/'
            path     = os.path.relpath(path, basepath)
        assert os.path.lexists(fullpath)
        self.path     = path
        self.basepath = basepath
        self.fullpath = fullpath
        self.stat     = os.lstat(self.fullpath)
        self.info     = {
            'platform': 'Linux',
            'file'    : {
                'name': os.path.basename(path),
                'path': os.path.dirname(path),
            },
        }
        mode = self.stat[ST_MODE]
        if S_ISDIR(mode):
            self.info['file']['type'] = 'DIR'
        elif S_ISCHR(mode):
            self.info['file']['type'] = 'CHR'
        elif S_ISBLK(mode):
            self.info['file']['type'] = 'BLK'
        elif S_ISREG(mode):
            self.info['file']['type'] = 'REG'
            self.info['file']['size'] = self.stat[ST_SIZE]
        elif S_ISFIFO(mode):
            self.info['file']['type'] = 'FIF'
        elif S_ISLNK(mode):
            self.info['file']['type'] = 'LNK'
            self.info['file']['link'] = os.readlink(self.fullpath)
        elif S_ISSOCK(mode):
            self.info['file']['type'] = 'SOC'

