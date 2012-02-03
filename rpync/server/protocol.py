import rpync

from rpync.common.logger import getLogger

from twisted.internet.protocol import Factory
from twisted.protocols.basic   import LineReceiver

class Server(LineReceiver):
    def __init__(self, factory):
        self.factory = factory
        self.config  = self.factory.config
        self.log     = getLogger('protocol')

    def connectionMade(self):
        self.log.info("Connection established ...")
        self.transport.write("rpync-server ({0})\r\n".format(rpync.version))


    def connectionLost(self, reason):
        pass

    def lineReceived(self, line):
        self.transport.loseConnection()

    def rawDataReceived(self, data):
        pass

class ServerFactory(Factory):
    def __init__(self, config):
        self.config = config
        self.log    = getLogger()

    def buildProtocol(self, addr):
        return Server(self)

    def startFactory(self):
        self.log.info("Version {0}".format(rpync.version))
