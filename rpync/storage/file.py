import os
import os.path

from stat import *

from rpync.storage.base import BaseStorage, BaseStorageJob

DIR_ACCESS  = 0750
FILE_ACCESS = 0750

class FileStorage(BaseStorage):
    def __init__(self, section):
        super(FileStorage, self).__init__(section)
        self.basedir = os.path.realpath(self.config.get(self.section, 'basedir'))
        if not os.path.isdir(self.basedir):
            msg = "invalid storage directory: " + self.basedir
            self.log.error(msg)
            raise ValueError, msg
        if not self.validAccess(self.basedir):
            msg = "insufficient or malformed access on storage directory"
            self.log.error(msg)
            raise ValueError, msg
        self.pooldir = os.path.join(self.basedir, 'pool')
        self.jobsdir = os.path.join(self.basedir, 'jobs')
        for path in (self.pooldir, self.jobsdir):
            if not os.path.exists(path):
                os.mkdir(path, DIR_ACCESS)
            elif not self.validAccess(path):
                msg = "insufficient or malformed access on: " + path
                self.log.error(msg)
                raise ValueError, msg

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

    def createJob(self, clientName, jobName):
        return FileStorageJob(self, clientName, jobName)

class FileStorageJob(BaseStorageJob):
    def __init__(self, storage, clientName, jobName):
        assert isinstance(storage, FileStorage)
        super(FileStorageJob, self).__init__(storage)
        self.clientName = clientName
        self.jobName    = jobName

