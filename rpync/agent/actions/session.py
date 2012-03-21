from rpync.agent.states  import STATE_INIT, STATE_RUNNING, STATE_FINISHED
from rpync.common.server import Action, ActionError

class ActionSession(Action):
    def __init__(self, server):
        super(ActionSession, self).__init__('session', server)

    def doAction(self, options, args):
        if self.server.getState() not in (STATE_INIT, STATE_RUNNING, STATE_FINISHED):
            raise ActionError, "invalid state for action session: {0}".format(self.server.getState())
        for include in self.server.session.getIncludes():
            self.server.transport.write("include: {0}\r\n".format(include))
        for exclude in self.server.session.getExcludes():
            self.server.transport.write("exclude: {0}\r\n".format(exclude))
        return True
