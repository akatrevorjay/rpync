from rpync.server.jobinfo   import JobInfo
from rpync.server.task.base import AgentTask
from rpync.storage          import getStorage

class BackupTask(AgentTask):
    def __init__(self, jobinfo):
        assert isinstance(jobinfo, JobInfo)
        self.jobinfo = jobinfo
        super(BackupTask, self).__init__(self.jobinfo.address, self.jobinfo.port)
        self.storage    = None
        self.storageJob = None

    def init(self):
        super(BackupTask, self).init()
        self.storage    = getStorage()
        self.storageJob = self.storage.createJob(self.jobinfo.clientName, self.jobinfo.jobName)

    def done(self):
        if self.storageJob is not None:
            self.storageJob.close()

    def next(self, action, command):
        if action is None:
            self.protocol.sendCommand('init')
            return True
        if action == 'init':
            self.iter = iter(self.jobinfo.includes)
            self.protocol.sendCommand('include', self.iter.next())
            return True
        if action == 'include':
            try:
                include = self.iter.next()
                self.protocol.sendCommand('include', include)
            except StopIteration:
                if len(self.jobinfo.excludes) > 0:
                    self.iter = iter(self.jobinfo.excludes)
                    self.protocol.sendCommand('exclude', self.iter.next())
                else:
                    self.protocol.sendCommand('backup')
            return True
        if action == 'backup':
            self.protocol.sendCommand('quit')
            return False
        return super(BackupTask, self).next(action, command)

