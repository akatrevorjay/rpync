from rpync.agent.states  import STATE_RUNNING
from rpync.common.server import Action

class ActionBackup(Action):
    def __init__(self, server):
        super(ActionBackup, self).__init__('backup', server)

    def doAction(self, options, args):
        self.server.setState(STATE_RUNNING)
        return True
