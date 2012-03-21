from rpync.agent.states  import STATE_INIT
from rpync.common.server import Action, ActionError

class ActionInclude(Action):
    def __init__(self, server):
        super(ActionInclude, self).__init__('include', server)

    def doAction(self, options, args):
        if self.server.getState() != STATE_INIT:
            raise ActionError, "invalid state for action include: {0}".format(self.server.getState())
        if len(args) != 1:
            raise ActionError, "usage: include <include_pattern>"
        try:
            self.server.session.addInclude(args[0])
        except ValueError, e:
            raise ActionError, "invalid include: " + str(e)
        return True
