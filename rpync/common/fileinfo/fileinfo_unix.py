import grp
import pwd

from stat import *
from rpync.common.fileinfo.base import Fileinfo

class FileinfoUnix(Fileinfo):
    def __init__(self, path, basepath, platform='Unix'):
        super(FileinfoUnix, self).__init__(path, basepath, platform)
        self.info['unix'] = {
            'inode': self.stat[ST_INO],
            'links': self.stat[ST_NLINK],
            'uid'  : self.stat[ST_UID],
            'gid'  : self.stat[ST_GID],
            'user' : pwd.getpwuid(self.stat[ST_UID]).pw_name,
            'group': grp.getgrgid(self.stat[ST_GID]).gr_name,
        }



