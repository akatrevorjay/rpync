import rpync

from rpync.common.server       import BaseServer, BaseServerFactory
from rpync.server.actions      import *
from rpync.server.clientconfig import initClientConfigs
from rpync.server.jobconfig    import initJobConfigs
from rpync.server.storage      import initStorage, getStorage

class Server(BaseServer):
    actions = dict()

    def __init__(self, factory, pid):
        assert isinstance(factory, ServerFactory)
        BaseServer.__init__(self, factory, pid)
        self.storage = self.factory.storage
        self.setAction(ActionBackup(self))
        self.setAction(ActionQuit(self), 'exit')

    def getGreeting(self):
        return "rpync-server ({0})\r\n".format(rpync.__version__)

class ServerFactory(BaseServerFactory):
    def __newProtocol__(self, addr, pid):
        return Server(self, pid)

    def startFactory(self):
        BaseServerFactory.startFactory(self)
        # Initialize
        initJobConfigs()
        initClientConfigs()
        initStorage()
        self.storage = getStorage()

