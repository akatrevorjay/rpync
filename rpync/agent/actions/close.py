from rpync.agent.states  import STATE_FINISHED
from rpync.common.server import Action

class ActionClose(Action):
    def __init__(self, server):
        super(ActionClose, self).__init__('close', server)

    def doAction(self, options, args):
        self.server.setState(STATE_FINISHED)
        return True
