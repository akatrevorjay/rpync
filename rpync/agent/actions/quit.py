from rpync.agent.states  import STATE_NONE
from rpync.common.server import Action

class ActionQuit(Action):
    def __init__(self, server):
        super(ActionQuit, self).__init__('quit', server)

    def doAction(self, options, args):
        self.server.setState(STATE_NONE)
        self.server.transport.loseConnection()
        return False
