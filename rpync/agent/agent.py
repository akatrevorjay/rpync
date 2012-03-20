import rpync

from rpync.agent.actions import *
from rpync.agent.session import Session
from rpync.agent.states  import *
from rpync.common.server import ActionError, BaseServer, BaseServerFactory

from twisted.internet.protocol import Factory

class TransitionError(ActionError):
    pass

class Agent(BaseServer):
    actions = dict()

    def __init__(self, factory, cid):
        assert isinstance(factory, AgentFactory)
        BaseServer.__init__(self, factory, cid)
        self.state             = STATE_NONE
        self.actions['abort']  = ActionAbort('abort', self)
        self.actions['commit'] = ActionCommit('commit', self)
        self.actions['exit']   = ActionQuit('exit', self)
        self.actions['init']   = ActionInit('init', self)
        self.actions['quit']   = ActionQuit('exit', self)
        self.actions['state']  = ActionState('state', self)
        self.setState(STATE_NONE)

    def getAction(self, name):
        return self.actions[name]

    def getGreeting(self):
        return "rpync-agent ({0})\r\n".format(rpync.__version__)

    def getState(self):
        return self.state

    def setState(self, state):
        assert state in STATES
        if state not in TRANSITIONS[self.state]:
            raise TransitionError, "invalid transition: {0} -> {1}".format(self.state, state)
        names = ("switch_all2{0}".format(state),
                 "switch_{0}2all".format(self.state),
                 "switch_{0}2{1}".format(self.state, state))
        for name in names:
            if hasattr(self, name):
                getattr(self, name)()
        self.state = state

    def switch_all2none(self):
        self.session = None
        self.error   = None

    def switch_all2init(self):
        self.session = Session()


class AgentFactory(BaseServerFactory):
    def __newServer__(self, addr):
        return Agent(self, self.counter)

