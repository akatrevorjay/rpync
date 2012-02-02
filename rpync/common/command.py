# command base class

from rpync.common.logger import getLogger

class Command(object):
    def __init__(self, name):
        self.log  = getLogger(name)
        self.name = name

    def run(self, options, config, *jobs):
        self.log.info("Starting {0} ...".format(self.name))

