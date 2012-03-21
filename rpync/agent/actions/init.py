from rpync.agent.states  import STATE_INIT
from rpync.common.server import Action

class ActionInit(Action):
    def __init__(self, server):
        super(ActionInit, self).__init__('init', server)

    def doAction(self, options, args):
        self.server.setState(STATE_INIT)
        return True
