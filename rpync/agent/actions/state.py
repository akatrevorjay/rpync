from rpync.agent.states  import *
from rpync.common.server import Action

class ActionState(Action):
    def doAction(self, options, args):
        self.server.transport.write("state: {0}\r\n".format(self.server.getState()))
        return False
