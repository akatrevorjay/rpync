import re
import sys
import rpync

from getopt import getopt, GetoptError

from rpync.common.config   import getConfig
from rpync.common.logger   import getLogger
from rpync.common.protocol import BaseProtocol, BaseServerProtocolFactory

ERRORS = ["ok",
          "server error",
          "invalid action",
          "invalid action: {action}",
          "invalid argument for '{action}': {message}"]
RE_NAME = re.compile(r'^\w+$')

class ActionError(Exception):
    pass

class Action(object):

    short_options = ""
    long_options  = []

    def __new__(cls, *args):
        instance = super(Action, cls).__new__(cls)
        for varname in ('short_options', 'long_options'):
            if hasattr(cls, varname):
                setattr(instance, varname, getattr(cls, varname))
        return instance

    def __init__(self, name, server):
        assert isinstance(name,   basestring) and RE_NAME.match(name)
        assert isinstance(server, BaseServer)
        self.server = server
        self.name   = name

    def __call__(self, argv):
        try:
            options, args = getopt(argv[1:], self.short_options, self.long_options)
            if self.doAction(options, args):
                self.server.writeOk()
        except GetoptError, e:
            self.server.writeError(ERRORS[4], action=self.name, message=str(e))
        except ActionError, e:
            msg = str(e)
            self.server.logError(msg)
            self.server.writeError(msg)
        except Exception, e:
            self.server.logDebug("exception raised", exc_info=True)
            self.server.writeError(ERRORS[1])

    def doAction(self, options, args):
        raise NotImplementedError

class BaseServer(BaseProtocol):
    def __init__(self, factory, cid):
        assert isinstance(factory, BaseServerFactory)
        BaseProtocol.__init__(self, factory, cid)
        self.config   = self.factory.config
        self._actions = dict()

    def hasAction(self, name):
        return name in self._actions

    def getAction(self, name):
        return self._actions[name]

    def setAction(self, action, *aliases):
        assert isinstance(action, Action)
        self._actions[action.name] = action
        for name in aliases:
            if not RE_NAME.match(name):
                raise ValueError, "invalid name: " + name
            self._actions[name] = action

    def getGreeting(self):
        raise NotImplementedError

    def connectionMade(self):
        BaseProtocol.connectionMade(self)
        self.transport.write(self.getGreeting())
        self.logInfo("waiting for input")

    def lineReceived(self, line):
        line = line.strip()
        argv = line.split()
        if len(argv) >= 1:
            action = argv[0]
            try:
                self.logInfo("handling action: {0}", action)
                self.getAction(action)(argv)
            except KeyError:
                self.writeError(ERRORS[3],action=action)
        else:
            self.writeError(ERRORS[2])

    def rawDataReceived(self, data):
        pass

    def writeOk(self):
        self.transport.write("{0}\r\n".format(ERRORS[0]))

    def writeError(self, error, **kwargs):
        message = error.format(**kwargs)
        self.logError(message)
        self.transport.write("error: {0}\r\n".format(message))

class BaseServerFactory(BaseServerProtocolFactory):
    def startFactory(self):
        BaseServerProtocolFactory.startFactory(self)
        # Bootstrap
        self.config = getConfig()
        self.log    = getLogger()
        self.log.info("version {0}".format(rpync.__version__))

