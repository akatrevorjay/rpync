import os.path

from ConfigParser import SafeConfigParser as ConfigParser


class Job(object):
    def __init__(self, name, log, main_config):
        self.name   = name
        self.config = self.__init_config__(log, main_config)

    def __init_config__(self, log, main_config):
        cfg = ConfigParser()
        for section in ('destination', 'commands:local', 'commands:remote'):
            cfg.add_section(section)
            for option in main_config.options(section):
                cfg.set(section, option, main_config.get(section, option))
        jobdir  = main_config.get('global', 'jobdir')
        jobfile = os.path.join(jobdir, self.name+".conf")
        if not os.path.isdir(jobdir):
            raise IOError, "Job directory doesn't exist: {0}".format(jobdir)
        if not os.path.isfile(jobfile):
            raise IOError, "Job file doesn't exist: {0}".format(jobfile)
        log.info("Reading job configuration from: {0}".format(jobfile))
        cfg.read(jobfile)
        return cfg
