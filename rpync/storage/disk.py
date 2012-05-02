import logging
import os
import os.path

from stat import *
from time import strftime, strptime

from rpync.common.fileinfo import FileInfo
from rpync.storage.base    import BaseStorage, BaseStorageJob

DIR_ACCESS  = 0750
FILE_ACCESS = 0750
TIME_FORMAT = '%Y%m%d-%H%M%S-%Z'

class DiskStorage(BaseStorage):
    def __init__(self, section):
        super(DiskStorage, self).__init__(section)
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
        return DiskStorageJob(self, clientName, jobName, timestamp)

class DiskStorageJob(BaseStorageJob):
    def __init__(self, storage, clientName, jobName, timestamp):
        assert isinstance(storage, DiskStorage)
        super(DiskStorageJob, self).__init__(storage)
        self.success    = False
        self.clientName = clientName
        self.jobName    = jobName
        self.jobTime    = strftime(TIME_FORMAT, timestamp)
        self.timestamp  = timestamp
        self.jobDir     = os.path.join(self.storage.stagejobsdir, self.clientName,\
                                       self.jobName, self.jobTime)
        self.jobLinks   = self.getJobLinks()
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

    def getJobLinks(self):
        path = os.path.join(self.storage.jobsdir, self.clientName, self.jobName)
        if os.path.exists(path):
            joblist = list()
            for name in os.listdir(path):
                jobdir = os.path.join(path, name)
                if os.path.isdir(jobdir):
                    try:
                        strptime(TIME_FORMAT, name)
                        joblist.append(jobdir)
                    except ValueError:
                        continue
            joblist.sort()
            return joblist if len(joblist) > 0 else None
        return None

    def close(self):
        if os.path.exists(self.jobDir):
            try:
                os.rmdir(self.jobDir)
            except OSError, e:
                msg = "unable to remove job directory '{0}': {1}". format(self.jobDir, str(e))
                self.log.error(msg)
        super(DiskStorageJob, self).close()

    def findFile(self, fileinfo):
        if self.jobLinks and fileinfo.type == FileInfo.T_FILE:
            pass
        return None

    def processFile(self, fileinfo):
        self.log.info("file: "+os.path.join(fileinfo.path, fileinfo.name))
        if fileinfo.file.type == FileInfo.T_FILE:
            filepath = os.path.join(self.jobDir, fileinfo.file.path, fileinfo.file.name)
            if not os.path.isdir(os.path.join(self.jobDir, fileinfo.file.path)):
                msg = "destination directory does not exist: "+fileinfo.file.path
                self.log.error(msg)
                raise ValueError, msg
            linkfile = self.findFile(fileinfo)
            if linkfile is not None:
                os.link(linkfile, filepath)


