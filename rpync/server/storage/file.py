import os
import os.path

from stat import *

from rpync.server.storage.base import BaseStorage, SECTION

DIR_ACCESS  = 0750
FILE_ACCESS = 0750

class FileStorage(BaseStorage):
    def __init__(self):
        super(FileStorage, self).__init__()
        self.basedir = os.path.realpath(self.config.get(SECTION, 'basedir'))
        if not os.path.isdir(self.basedir):
            raise ValueError, "Invalid storage directory: " + self.basedir
        if not self.validAccess(self.basedir):
            raise ValueError, "Insufficient or malformed access on storage directory"
        self.pooldir = os.path.join(self.basedir, 'pool')
        self.jobsdir = os.path.join(self.basedir, 'jobs')
        for path in (self.pooldir, self.jobsdir):
            if not os.path.exists(path):
                os.mkdir(path, DIR_ACCESS)
            elif not self.validAccess(path):
                raise ValueError, "Insufficient or malformed access on: " + path

    def validAccess(self, path):
        if os.path.exists(path):
            statinfo  = os.stat(path)
            mode      = statinfo[ST_MODE]
            validMode = False
            if S_ISDIR(mode):
                validMode = mode & 0777 == DIR_ACCESS
            elif S_ISREG(mode):
                validMode = mode & 0777 == FILE_ACCESS
            return validMode and os.access(path, os.R_OK | os.W_OK | os.X_OK)
        return False

