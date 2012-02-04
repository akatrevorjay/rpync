import sys

from getopt import getopt, GetoptError

class Action(object):

    short_options = None
    long_options  = None

    def __init__(self, name, server):
        from rpync.server.protocol import Server
        
        assert isinstance(name,   basestring)
        assert isinstance(server, Server)
        self.server = server
        self.name   = name

    def __call__(self, argv):
        try:
            if self.doAction(None, None):
                self.server.writeOk()
            raise ValueError
        except Exception, e:
            self.server.logDebug("exception raised", exc_info=True)
            self.server.writeError(1)

    def doAction(self, options, args):
        raise NotImplementedError
