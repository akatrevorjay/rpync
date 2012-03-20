from rpync.agent.states  import *
from rpync.common.server import Action

class ActionInit(Action):
    def doAction(self, options, args):
        self.server.setState(STATE_INIT)
        return True
