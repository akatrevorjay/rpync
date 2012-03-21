from rpync.agent.states  import STATE_NONE
from rpync.common.server import Action

class ActionAbort(Action):
    def __init__(self, server):
        super(ActionAbort, self).__init__('abort', server)

    def doAction(self, options, args):
        self.server.setState(STATE_NONE)
        return True
