import rpync

from rpync.common.server       import BaseServer, BaseServerFactory
from rpync.server.actions      import *
from rpync.server.clientconfig import initClientConfigs
from rpync.server.jobconfig    import initJobConfigs
from rpync.server.storage      import initStorage, getStorage

class Server(BaseServer):
    actions = dict()

    def __init__(self, factory, cid):
        assert isinstance(factory, ServerFactory)
        BaseServer.__init__(self, factory, cid)
        self.storage         = self.factory.storage
        self.actions['quit'] = ActionQuit('quit', self)
        self.actions['exit'] = ActionQuit('exit', self)

    def getAction(self, name):
        return self.actions[name]

    def getGreeting(self):
        return "rpync-server ({0})\r\n".format(rpync.__version__)

class ServerFactory(BaseServerFactory):
    def __newServer__(self, addr):
        return Server(self, self.counter)

    def startFactory(self):
        BaseServerFactory.startFactory(self)
        # Initialize
        initJobConfigs()
        initClientConfigs()
        initStorage()
        self.storage = getStorage()

