import grp
import pwd

from stat import *
from rpync.common.fileinfo.base import Fileinfo

class FileinfoUnix(Fileinfo):
    def __make__(self, path, basepath, platform):
        super(FileinfoUnix, self).__make__(path, basepath, platform)
        self.info[u'unix'] = {
            u'inode': self.stat[ST_INO],
            u'links': self.stat[ST_NLINK],
            u'uid'  : self.stat[ST_UID],
            u'gid'  : self.stat[ST_GID],
            u'user' : unicode(pwd.getpwuid(self.stat[ST_UID]).pw_name),
            u'group': unicode(grp.getgrgid(self.stat[ST_GID]).gr_name),
        }



