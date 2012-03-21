from rpync.common.server import Action

class ActionQuit(Action):
    def __init__(self, server):
        super(ActionQuit, self).__init__('quit', server)

    def doAction(self, options, args):
        self.server.transport.loseConnection()
        return False
