from rpync.common.logger import getLogger

from twisted.internet.protocol import ClientFactory, Factory
from twisted.protocols.basic   import LineReceiver

class BaseProtocol(LineReceiver):
    def __init__(self, factory, cid):
        assert isinstance(factory, BaseServerProtocolFactory) or isinstance(factory, BaseClientProtocolFactory)
        self.factory = factory
        self.logger  = getLogger()
        self.cid     = cid

    def connectionMade(self):
        self.logInfo("connection established ...")
        self.logInfo("peer: {0}", self.transport.getPeer())

    def connectionLost(self, reason):
        self.logInfo("closing connection ...")
        self.logInfo("reason: {0}", reason.getErrorMessage())
        self.logInfo("connection closed.")

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

class BaseServerProtocolFactory(Factory):
    def __newProtocol__(self, addr):
        raise NotImplementedError

    def buildProtocol(self, addr):
        self.counter += 1L
        return self.__newProtocol__(addr)

    def startFactory(self):
        # Initialize
        self.counter = 0L

class BaseClientProtocolFactory(ClientFactory):
    def __newProtocol__(self, addr):
        raise NotImplementedError

    def buildProtocol(self, addr):
        self.counter += 1L
        return self.__newProtocol__(addr)

    def startFactory(self):
        # Initialize
        self.counter = 0L

