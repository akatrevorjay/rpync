from rpync.common.server import Action

class ActionState(Action):
    def __init__(self, server):
        super(ActionState, self).__init__('state', server)

    def doAction(self, options, args):
        self.server.transport.write("state: {0}\r\n".format(self.server.getState()))
        return True
