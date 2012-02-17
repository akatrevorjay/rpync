import logging
import rpync

from rpync.common.config       import getConfig
from rpync.common.logger       import getLogger
from rpync.server.actions      import *
from rpync.server.clientconfig import initClientConfigs
from rpync.server.jobconfig    import initJobConfigs

from twisted.internet.protocol import Factory
from twisted.protocols.basic   import LineReceiver

class Server(LineReceiver):

    _errors  = ["ok",
                "server error",
                "invalid action",
                "invalid action: {action}",
                "invalid argument for '{action}': {message}"]
    _actions = dict()

    def __init__(self, factory, cid):
        assert isinstance(factory, ServerFactory)
        self.factory          = factory
        self.config           = self.factory.config
        self.logger           = getLogger()
        self.cid              = cid
        self._bytes_send      = 0
        self._bytes_received  = 0
        self._actions['quit'] = ActionQuit('quit', self)
        self._actions['exit'] = ActionQuit('exit', self)

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

    def connectionMade(self):
        greeting = "rpync-server ({0})\r\n".format(rpync.__version__)
        self.logInfo("connection established ...")
        self.logInfo("peer: {0}", self.transport.getPeer())
        self.transport.write(greeting)
        self.logInfo("waiting for input")
        self._bytes_send     = len(greeting)
        self._bytes_received = 0

    def connectionLost(self, reason):
        self.logInfo("closing connection ...")
        self.logInfo("reason: {0}", reason.getErrorMessage())
        self.logInfo("send: {0} bytes", self._bytes_send)
        self.logInfo("received: {0} bytes", self._bytes_received)
        self.logInfo("connection closed.")

    def lineReceived(self, line):
        self._bytes_received += (len(line)+2)
        line = line.strip()
        argv = line.split()
        if len(argv) >= 1:
            action = argv[0]
            if action in self._actions:
                self.logInfo("handling action: {0}", action)
                self._actions[action](argv)
            else:
                self.writeError(3,action=action)
        else:
            self.writeError(2)

    def rawDataReceived(self, data):
        pass

    def writeOk(self):
        self.transport.write("{0}\r\n".format(self._errors[0]))

    def writeError(self, errno, **kwargs):
        error = self._errors[errno].format(**kwargs)
        self.logError(error)
        self.transport.write("error ({0}) {1}\r\n".format(errno, error))

class ServerFactory(Factory):
    def buildProtocol(self, addr):
        self.counter += 1L
        return Server(self, self.counter)

    def startFactory(self):
        self.config  = getConfig()
        self.log     = getLogger()
        self.counter = 0L
        self.log.info("version {0}".format(rpync.__version__))
        initJobConfigs()
        initClientConfigs()

