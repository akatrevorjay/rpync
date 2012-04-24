import logging
import os
import os.path

from stat import *
from time import strftime

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
        self.jobsdir      = os.path.join(self.basedir,  'jobs')
        self.pooldir      = os.path.join(self.basedir,  'pool')
        self.stagedir     = os.path.realpath(self.config.get(self.section, 'stagedir'))
        self.stagejobsdir = os.path.join(self.stagedir, 'jobs')
        self.stagelogsdir = os.path.join(self.stagedir, 'logs')
        self.stagepooldir = os.path.join(self.stagedir, 'pool')
        for path in (self.jobsdir, self.pooldir, self.stagedir, self.stagejobsdir,\
                     self.stagelogsdir, self.stagepooldir):
            if not os.path.exists(path):
                try:
                    os.mkdir(path, DIR_ACCESS)
                except OSError, e:
                    msg = "unable to create directory '{0}': {1}". format(path, str(e))
                    self.log.error(msg)
                    raise ValueError, msg
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

    def createJob(self, clientName, jobName, timestamp):
        return FileStorageJob(self, clientName, jobName, timestamp)

class FileStorageJob(BaseStorageJob):
    def __init__(self, storage, clientName, jobName, timestamp):
        assert isinstance(storage, FileStorage)
        super(FileStorageJob, self).__init__(storage)
        self.success    = False
        self.clientName = clientName
        self.jobName    = jobName
        self.jobTime    = strftime("%Y%m%d-%H%M%S-%Z", timestamp)
        self.timestamp  = timestamp
        self.jobDir     = os.path.join(self.storage.stagejobsdir, self.clientName,\
                                       self.jobName, self.jobTime)
        self.logName    = "{0}-{1}-{2}.log".format(self.clientName, self.jobName, self.jobTime)

        formatter = logging.Formatter("%(levelname)s: %(message)s")
        handler   = logging.FileHandler(os.path.join(self.storage.stagelogsdir, self.logName),'wb')
        handler.setLevel(logging.INFO)
        handler.setFormatter(formatter)
        self.log.addHandler(handler)
        self.log.info("initializing storage job")
        self.log.info("path: " + self.jobDir[len(self.storage.stagejobsdir)+1:])
        try:
            os.makedirs(self.jobDir, DIR_ACCESS)
        except OSError, e:
            msg = "unable to create job directory '{0}': {1}". format(self.jobDir, str(e))
            self.log.error(msg)
            raise ValueError, msg

    def close(self):
        if os.path.exists(self.jobDir):
            try:
                os.rmdir(self.jobDir)
            except OSError, e:
                msg = "unable to remove job directory '{0}': {1}". format(self.jobDir, str(e))
                self.log.error(msg)
        super(FileStorageJob, self).close()

    def processFile(self, fileinfo):
        self.log.info("file: "+os.path.join(fileinfo.path, fileinfo.name))


