import os
import os.path

from rpync.common.config import getConfig, ConfigParser
from rpync.common.logger import getLogger

JOB_CONFIGS = None

class JobConfig(ConfigParser):
    def __init__(self, name):
        global JOB_CONFIGS
        if JOB_CONFIGS is None:
            raise ValueError, "Job configurations are not inizialized"
        super(JobConfig, self).__init__()
        if name in JOB_CONFIGS and isinstance(JOB_CONFIGS[name], JobConfig):
            raise ValueError, "Duplicate job configuration: "+name
        self.name = name
        self.__init_config__()

    def __init_config__(self):
        jobdir  = getConfig().get('global', 'jobdir')
        jobfile = os.path.join(jobdir, self.name+".conf")
        getLogger.info("Loading job configuration: " + self.name)
        self.read(jobfile)

def getJobConfig(name):
    global JOB_CONFIGS
    if JOB_CONFIGS is None:
        raise ValueError, "Job configurations are not inizialized"
    config = JOB_CONFIGS[name]
    if config == name:
        config            = JobConfig(name)
        JOB_CONFIGS[name] = config
    return config

def initJobConfigs():
    global JOB_CONFIGS
    if JOB_CONFIGS is None:
        log         = getLogger()
        cfg         = getConfig()
        log.info("Initializing job configurations")
        jobdir      = getConfig().get('global', 'jobdir')
        JOB_CONFIGS = dict()
        if os.path.isdir(jobdir):
            for entry in os.listdir(jobdir):
                name, ext = os.path.splitext(entry)
                filename  = os.path.join(jobdir, entry)
                if os.path.isfile(filename) and ext == '.conf':
                    JOB_CONFIGS[name] = name
        else:
            log.error("Job directory doesn't exist: {0}".format(jobdir))

