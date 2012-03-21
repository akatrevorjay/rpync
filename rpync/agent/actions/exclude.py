from rpync.agent.states  import STATE_INIT
from rpync.common.server import Action, ActionError

class ActionExclude(Action):
    def __init__(self, server):
        super(ActionExclude, self).__init__('exclude', server)

    def doAction(self, options, args):
        if self.server.getState() != STATE_INIT:
            raise ActionError, "invalid state for action exclude: {0}".format(self.server.getState())
        if len(args) != 1:
            raise ActionError, "usage: exclude <exclude_pattern>"
        try:
            self.server.session.addExclude(args[0])
        except ValueError, e:
            raise ActionError, "invalid exclude pattern: " + str(e)
        return True
