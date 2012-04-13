from rpync.server.clientconfig import ClientConfig
from rpync.server.jobconfig    import getJobConfig

class JobInfo(object):
    def __init__(self, clientconfig, name):
        assert isinstance(clientconfig, ClientConfig)
        section   = "job:"+name
        jobconfig = None
        if not clientconfig.has_section(section):
            raise ValueError, "unknown client job: " + name
        self.includes = set()
        self.excludes = set()
        self.address  = clientconfig.get('client', 'address')
        self.port     = 1081
        if clientconfig.has_option(section, 'base'):
            jobconfig = getJobConfig(clientconfig.get(section, 'base'))
            if jobconfig.has_option('job', 'includes'):
                self.includes.update(jobconfig.getlist('job', 'includes'))
            if jobconfig.has_option('job', 'excludes'):
                self.excludes.update(jobconfig.getlist('job', 'excludes'))
        if clientconfig.has_option(section, 'includes'):
            self.includes.update(clientconfig.getlist(section, 'includes'))
        if clientconfig.has_option(section, 'excludes'):
            self.excludes.update(clientconfig.getlist(section, 'excludes'))
        if clientconfig.has_option('client', 'port'):
            self.port = clientconfig.getint('client', 'port')
        self.includes = tuple(self.includes)
        self.excludes = tuple(self.excludes)

