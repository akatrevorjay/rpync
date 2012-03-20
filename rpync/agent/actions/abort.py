from rpync.agent.states  import *
from rpync.common.server import Action

class ActionAbort(Action):
    def doAction(self, options, args):
        self.server.setState(STATE_NONE)
        return True
