import sys

from getopt import getopt, GetoptError

class Action(object):

    short_options = ""
    long_options  = []

    def __new__(cls, name, server):
        instance = super(Action, cls).__new__(cls)
        for varname in ('short_options', 'long_options'):
            if hasattr(cls, varname):
                setattr(instance, varname, getattr(cls, varname))
        return instance

    def __init__(self, name, server):
        from rpync.server.protocol import Server
        
        assert isinstance(name,   basestring)
        assert isinstance(server, Server)
        self.server = server
        self.name   = name

    def __call__(self, argv):
        try:
            options, args = getopt(argv[1:], self.short_options, self.long_options)
            if self.doAction(options, args):
                self.server.writeOk()
        except GetoptError, e:
            self.server.writeError(4, action=self.name, message=str(e))
        except Exception, e:
            self.server.logDebug("exception raised", exc_info=True)
            self.server.writeError(1)

    def doAction(self, options, args):
        raise NotImplementedError
