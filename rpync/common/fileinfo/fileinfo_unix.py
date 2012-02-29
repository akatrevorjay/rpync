import grp
import pwd

from stat import *
from rpync.common.fileinfo.base import FileInfo

class FileInfoUnix(FileInfo):
    def __make_ext__(self, path, basepath, fullpath, stat, platform):
        self.info[u'unix'] = {
            u'inode': stat[ST_INO],
            u'links': stat[ST_NLINK],
            u'uid'  : stat[ST_UID],
            u'gid'  : stat[ST_GID],
            u'user' : unicode(pwd.getpwuid(stat[ST_UID]).pw_name),
            u'group': unicode(grp.getgrgid(stat[ST_GID]).gr_name),
        }

    def __setinfo__(self, info):
        try:
            assert isinstance(info, dict)
            assert 'unix' in info
            unixinfo = info['unix']
            assert 'inode' in unixinfo
            assert 'links' in unixinfo
            assert 'uid'   in unixinfo
            assert 'gid'   in unixinfo
            assert 'user'  in unixinfo
            assert 'group' in unixinfo
        except AssertionError,e:
            raise ValueError, "Invalid file information"
        super(FileInfoUnix, self).__setinfo__(info)


