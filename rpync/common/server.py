import sys
import rpync

from getopt import getopt, GetoptError

from rpync.common.config import getConfig
from rpync.common.logger import getLogger

from twisted.internet.protocol import Factory
from twisted.protocols.basic   import LineReceiver

ERRORS = ["ok",
          "server error",
          "invalid action",
          "invalid action: {action}",
          "invalid argument for '{action}': {message}"]

class ActionError(Exception):
    pass

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
        assert isinstance(name,   basestring)
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

class BaseServer(LineReceiver):
    def __init__(self, factory, cid):
        assert isinstance(factory, BaseServerFactory)
        self.factory = factory
        self.config  = self.factory.config
        self.logger  = getLogger()
        self.cid     = cid

    def getAction(self, name):
        raise NotImplementedError

    def getGreeting(self):
        raise NotImplementedError

    def connectionMade(self):
        self.logInfo("connection established ...")
        self.logInfo("peer: {0}", self.transport.getPeer())
        self.transport.write(self.getGreeting())
        self.logInfo("waiting for input")

    def connectionLost(self, reason):
        self.logInfo("closing connection ...")
        self.logInfo("reason: {0}", reason.getErrorMessage())
        self.logInfo("connection closed.")

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

    def logException(self, message, *args, **kwargs):
        self.logger.exception("[{0}] {1}".format(self.cid, message.format(*args, **kwargs)))

    def logDebug(self, message, *args, **kwargs):
        exc_info = False
        if 'exc_info' in kwargs:
            exc_info = True
            del kwargs['exc_info']
        self.logger.debug("[{0}] {1}".format(self.cid, message.format(*args, **kwargs)), exc_info=exc_info)

    def logInfo(self, message, *args, **kwargs):
        self.logger.info("[{0}] {1}".format(self.cid, message.format(*args, **kwargs)))

    def logWarning(self, message, *args, **kwargs):
        self.logger.warning("[{0}] {1}".format(self.cid, message.format(*args, **kwargs)))

    def logError(self, message, *args, **kwargs):
        self.logger.error("[{0}] {1}".format(self.cid, message.format(*args, **kwargs)))

    def logCritical(self, message, *args, **kwargs):
        self.logger.critical("[{0}] {1}".format(self.cid, message.format(*args, **kwargs)))

    def writeOk(self):
        self.transport.write("{0}\r\n".format(ERRORS[0]))

    def writeError(self, error, **kwargs):
        message = error.format(**kwargs)
        self.logError(message)
        self.transport.write("error: {0}\r\n".format(message))

class BaseServerFactory(Factory):
    def __newServer__(self, addr):
        raise NotImplementedError

    def buildProtocol(self, addr):
        self.counter += 1L
        return self.__newServer__(addr)

    def startFactory(self):
        # Bootstrap
        self.config = getConfig()
        self.log    = getLogger()
        self.log.info("version {0}".format(rpync.__version__))
        # Initialize
        self.counter = 0L

