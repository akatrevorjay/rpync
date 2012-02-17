import json
import os
import os.path

from stat import *
from time import localtime, strftime

TIME_FORMAT = '%Y%m%d-%H%M%S-%Z'

class FileInfo(object):

    class Branch(object):
        def __init__(self, branch):
            assert isinstance(branch, dict)
            self._branch = branch
        def __getattr__(self, name):
            try:
                value = self._branch[name]
                if isinstance(value, dict):
                    return Branch(value)
                return value
            except KeyError, e:
                raise AttributeError, "Unknown attribute: "+name

    def __make__(self, path, basepath, platform):
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
            u'platform' : unicode(platform),
            u'file'     : {
                u'name' : unicode(os.path.basename(path)),
                u'path' : unicode(os.path.dirname(path)),
                u'atime': unicode(strftime(TIME_FORMAT, localtime(self.stat[ST_ATIME]))),
                u'mtime': unicode(strftime(TIME_FORMAT, localtime(self.stat[ST_MTIME]))),
                u'ctime': unicode(strftime(TIME_FORMAT, localtime(self.stat[ST_CTIME]))),
            },
        }
        mode = self.stat[ST_MODE]
        if S_ISDIR(mode):
            self.info['file'][u'type'] = u'DIR'
        elif S_ISCHR(mode):
            self.info['file'][u'type'] = u'CHR'
        elif S_ISBLK(mode):
            self.info['file'][u'type'] = u'BLK'
        elif S_ISREG(mode):
            self.info['file'][u'type'] = u'REG'
            self.info['file'][u'size'] = self.stat[ST_SIZE]
        elif S_ISFIFO(mode):
            self.info['file'][u'type'] = u'FIF'
        elif S_ISLNK(mode):
            self.info['file'][u'type'] = u'LNK'
            self.info['file'][u'link'] = os.readlink(self.fullpath)
        elif S_ISSOCK(mode):
            self.info['file'][u'type'] = u'SOC'

    def __setinfo__(self, info):
        assert isinstance(info, dict)

    def __str__(self):
        return str(self.info)

    def __getattr__(self, name):
        try:
            value = self.info[name]
            if isinstance(value, dict):
                return FileInfo.Branch(value)
            return value
        except KeyError, e:
            raise AttributeError, "Unknown attribute: "+name

    def dump(self, fp, *args, **kwargs):
        json.dump(self.info, fp, *args, **kwargs)

    def dumps(self, *args, **kwargs):
        return json.dumps(self.info, *args, **kwargs)

