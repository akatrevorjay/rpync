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

    def __make_ext__(self, path, basepath, fullpath, stat, platform):
        raise NotImplementedError

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
        stat      = os.lstat(fullpath)
        self.info = {
            u'platform' : unicode(platform),
            u'file'     : {
                u'name' : unicode(os.path.basename(path)),
                u'path' : unicode(os.path.dirname(path)),
                u'atime': unicode(strftime(TIME_FORMAT, localtime(stat[ST_ATIME]))),
                u'mtime': unicode(strftime(TIME_FORMAT, localtime(stat[ST_MTIME]))),
                u'ctime': unicode(strftime(TIME_FORMAT, localtime(stat[ST_CTIME]))),
            },
        }
        mode = stat[ST_MODE]
        if S_ISDIR(mode):
            self.info['file'][u'type'] = u'DIR'
        elif S_ISCHR(mode):
            self.info['file'][u'type'] = u'CHR'
        elif S_ISBLK(mode):
            self.info['file'][u'type'] = u'BLK'
        elif S_ISREG(mode):
            self.info['file'][u'type'] = u'REG'
            self.info['file'][u'size'] = stat[ST_SIZE]
        elif S_ISFIFO(mode):
            self.info['file'][u'type'] = u'FIF'
        elif S_ISLNK(mode):
            self.info['file'][u'type'] = u'LNK'
            self.info['file'][u'link'] = os.readlink(fullpath)
        elif S_ISSOCK(mode):
            self.info['file'][u'type'] = u'SOC'
        self.__make_ext__(path, basepath, fullpath, stat, platform)

    def __setinfo__(self, info):
        try:
            assert isinstance(info, dict)
            assert 'platform' in info
            assert 'file'     in info
            fileinfo = info['file']
            assert 'name'  in fileinfo
            assert 'path'  in fileinfo
            assert 'atime' in fileinfo
            assert 'ctime' in fileinfo
            assert 'mtime' in fileinfo
            assert 'type'  in fileinfo
            if fileinfo['type'] == 'REG':
                assert 'size'  in fileinfo
            if fileinfo['type'] == 'LNK':
                assert 'link'  in fileinfo
        except AssertionError,e:
            raise ValueError, "Invalid file information"
        self.info = info

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

