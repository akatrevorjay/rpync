import rpync

from rpync.agent.actions import *
from rpync.common.server import BaseServer, BaseServerFactory

from twisted.internet.protocol import Factory

class Agent(BaseServer):
    actions = dict()

    def __init__(self, factory, cid):
        assert isinstance(factory, AgentFactory)
        BaseServer.__init__(self, factory, cid)
        self.actions['quit'] = ActionQuit('quit', self)
        self.actions['exit'] = ActionQuit('exit', self)

    def getAction(self, name):
        return self.actions[name]

    def getGreeting(self):
        return "rpync-agent ({0})\r\n".format(rpync.__version__)

class AgentFactory(BaseServerFactory):
    def __newServer__(self, addr):
        return Agent(self, self.counter)

