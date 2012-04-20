import threading

from rpync.common.logger import getLogger

from twisted.internet.protocol import ClientFactory, Factory
from twisted.protocols.basic   import LineReceiver

class BaseProtocol(LineReceiver):
    def __init__(self, factory, pid, *args):
        args = list(args)
        args.append(str(pid))
        assert isinstance(factory, BaseServerProtocolFactory) or isinstance(factory, BaseClientProtocolFactory)
        self.factory = factory
        self.log     = self.createLogger(*args)
        self.pid     = pid

    def createLogger(self, *args):
        return getLogger(*args)

    def connectionMade(self):
        self.logInfo("connection established ...")
        self.logInfo("peer: {0}", self.transport.getPeer())

    def connectionLost(self, reason):
        self.logInfo("closing connection ...")
        self.logInfo("reason: {0}", reason.getErrorMessage())
        self.logInfo("connection closed.")

    def logException(self, message, *args, **kwargs):
        self.log.exception(message.format(*args, **kwargs))

    def logDebug(self, message, *args, **kwargs):
        exc_info = False
        if 'exc_info' in kwargs:
            exc_info = True
            del kwargs['exc_info']
        self.log.debug(message.format(*args, **kwargs), exc_info=exc_info)

    def logInfo(self, message, *args, **kwargs):
        self.log.info(message.format(*args, **kwargs))

    def logWarning(self, message, *args, **kwargs):
        self.log.warning(message.format(*args, **kwargs))

    def logError(self, message, *args, **kwargs):
        self.log.error(message.format(*args, **kwargs))

    def logCritical(self, message, *args, **kwargs):
        self.log.critical(message.format(*args, **kwargs))

counter     = 0L
counterLock = threading.Lock()

class BaseServerProtocolFactory(Factory):
    def __newProtocol__(self, addr, pid):
        raise NotImplementedError

    def buildProtocol(self, addr):
        global counter, counterLock
        with counterLock:
            counter += 1
            pid      = counter
        return self.__newProtocol__(addr, pid)

class BaseClientProtocolFactory(ClientFactory):
    def __newProtocol__(self, addr, pid):
        raise NotImplementedError

    def buildProtocol(self, addr):
        global counter, counterLock
        with counterLock:
            counter += 1
            pid      = counter
        return self.__newProtocol__(addr, pid)

