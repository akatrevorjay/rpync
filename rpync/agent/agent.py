import rpync

from rpync.agent.actions import *
from rpync.agent.session import Session
from rpync.agent.states  import *
from rpync.common.server import ActionError, BaseServer, BaseServerFactory

from twisted.internet.protocol import Factory

class TransitionError(ActionError):
    pass

class Agent(BaseServer):
    def __init__(self, factory, cid):
        assert isinstance(factory, AgentFactory)
        BaseServer.__init__(self, factory, cid)
        self._state = STATE_NONE
        self.setAction(ActionAbort(self))
        self.setAction(ActionBackup(self))
        self.setAction(ActionClose(self))
        self.setAction(ActionExclude(self), 'exc')
        self.setAction(ActionInclude(self), 'inc')
        self.setAction(ActionInit(self))
        self.setAction(ActionNext(self))
        self.setAction(ActionQuit(self), 'exit')
        self.setAction(ActionSession(self))
        self.setAction(ActionState(self))
        self.setState(STATE_NONE)

    def getGreeting(self):
        return "rpync-agent ({0})\r\n".format(rpync.__version__)

    def getState(self):
        return self._state

    def setState(self, state):
        self.checkTransition(self._state, state)
        names = ("switch_all2{0}".format(state),
                 "switch_{0}2all".format(self._state),
                 "switch_{0}2{1}".format(self._state, state))
        for name in names:
            if hasattr(self, name):
                getattr(self, name)()
        self._state = state

    def validTransition(self, start=None, end=None):
        assert start is None or start in STATES
        return end in TRANSITIONS[start if start is not None else self._state]

    def checkTransition(self, start=None, end=None):
        if start is None:
            start = self._state
        if not self.validTransition(start, end):
            raise TransitionError, "invalid transition: {0} -> {1}".format(start, end)

    def switch_all2none(self):
        self.session = None
        self.error   = None

    def switch_all2init(self):
        self.session = Session()
        self.error   = None

    def switch_all2running(self):
        reason = self.session.commit()
        if reason is not None:
            raise TransitionError, "invalid session: " + reason

class AgentFactory(BaseServerFactory):
    def __newServer__(self, addr):
        return Agent(self, self.counter)

