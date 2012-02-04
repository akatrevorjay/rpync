from rpync.server.actions.base import Action

class ActionQuit(Action):
    def doAction(self, options, args):
        self.server.transport.loseConnection()
        return False
