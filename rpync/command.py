# command base class

import logging

class Command(object):
    def __init__(self, name, log_handlers):
        self.log  = self.__init_log__(name, log_handlers)
        self.name = name

    def __init_log__(self, log_name, log_handlers):
        return logging.getLogger('rpync.'+log_name)

    def run(self, options, config, *jobs):
        self.log.info("Starting {0} ...".format(self.name))

