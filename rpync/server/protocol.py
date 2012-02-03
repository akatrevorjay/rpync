from rpync.common.logger import getLogger

from twisted.internet.protocol import Factory
from twisted.protocols.basic   import LineReceiver

class Server(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.config  = self.factory.config
        self.log     = getLogger('protocol')

    def connectionMade(self):
        pass

    def connectionLost(self, reason):
        pass

    def lineReceived(self, line):
        self.transport.loseConnection()

    def rawDataReceived(self, data):
        pass

class ServerFactory(Factory):
    def __init__(self, config):
        self.config = config

    def buildProtocol(self, addr):
        return Server(self)
