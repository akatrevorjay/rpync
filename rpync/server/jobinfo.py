from rpync.server.clientconfig import getClientConfig
from rpync.server.jobconfig    import getJobConfig

class JobInfo(object):
    def __init__(self, clientName, jobName):
        self.clientName   = clientName
        self.jobName      = jobName
        self.clientConfig = getClientConfig(clientName)
        self.jobSection   = "job:"+jobName
        self.jobConfig    = None
        if not self.clientConfig.has_section(self.jobSection):
            msg = "unknown job '{0}' for client '{1}' ".format(self.jobName, self.clientName)
            raise ValueError, msg
        self.includes = set()
        self.excludes = set()
        self.address  = self.clientConfig.get('client', 'address')
        self.port     = 1081
        if self.clientConfig.has_option(self.jobSection, 'base'):
            self.jobConfig = getJobConfig(self.clientConfig.get(self.jobSection, 'base'))
            if self.jobConfig.has_option('job', 'includes'):
                self.includes.update(self.jobConfig.getlist('job', 'includes'))
            if self.jobConfig.has_option('job', 'excludes'):
                self.excludes.update(self.jobConfig.getlist('job', 'excludes'))
        if self.clientConfig.has_option(self.jobSection, 'includes'):
            self.includes.update(self.clientConfig.getlist(self.jobSection, 'includes'))
        if self.clientConfig.has_option(self.jobSection, 'excludes'):
            self.excludes.update(self.clientConfig.getlist(self.jobSection, 'excludes'))
        if self.clientConfig.has_option('client', 'port'):
            self.port = self.clientConfig.getint('client', 'port')
        self.includes = tuple(self.includes)
        self.excludes = tuple(self.excludes)

