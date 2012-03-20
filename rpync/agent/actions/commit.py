from rpync.agent.states  import *
from rpync.common.server import Action

class ActionCommit(Action):
    def doAction(self, options, args):
        self.server.setState(STATE_READY)
        return True
