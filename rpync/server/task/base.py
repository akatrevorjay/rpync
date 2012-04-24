from rpync.common.protocol import BaseProtocol, BaseClientProtocolFactory
from rpync.server.jobinfo  import JobInfo

from twisted.internet          import reactor
from twisted.internet.protocol import ClientFactory

COMMANDMAP = {
    'abort'  : 'abort',
    'reset'  : 'abort',
    'clear'  : 'abort',
    'backup' : 'backup',
    'close'  : 'close',
    'exclude': 'exclude',
    'exc'    : 'exclude',
    'include': 'include',
    'inc'    : 'include',
    'init'   : 'init',
    'next'   : 'next',
    'quit'   : 'quit',
    'exit'   : 'quit',
    'session': 'session',
    'state'  : 'state',
}

class Task(object):
    def run(self):
        raise NotImplementedError

class RemoteTask(Task):
    def __init__(self, address, port, factory):
        assert isinstance(factory, ClientFactory)
        self.address  = address
        self.port     = port
        self.factory  = factory
        self.protocol = None

    def init(self):
        pass

    def next(self, action, command):
        return False

    def error(self, action, command, error):
        return True

    def done(self):
        pass

    def run(self):
        reactor.connectTCP(self.address, self.port, self.factory)

class AgentTask(RemoteTask):
    def __init__(self, address, port):
        super(AgentTask, self).__init__(address, port, AgentTaskFactory(self))

class AgentTaskProtocol(BaseProtocol):
    CONNECTED, INITIALIZED, RUNNING, FINISHED, ERROR = range(5)

    def __init__(self, factory, pid):
        assert isinstance(factory, AgentTaskFactory)
        BaseProtocol.__init__(self, factory, pid, 'task')
        self.task   = self.factory.task
        self.state  = None
        self.error  = None
        self.sended = (None, None)
        self.result = None

    def connectionMade(self):
        BaseProtocol.connectionMade(self)
        self.task.protocol = self
        self.state         = self.CONNECTED
        try:
            self.task.init()
            self.state = self.INITIALIZED
        except Exception, e:
            if not self.handleError(str(e)):
                self.state = self.INITIALIZED

    def connectionLost(self, reason):
        self.task.done()
        self.task.protocol = None
        self.state         = self.FINISHED
        BaseProtocol.connectionLost(self, reason)

    def handleError(self, error):
        if self.task.error(self.sended[0], self.sended[1], error):
            self.state = self.ERROR
            self.error = error
            self.log.error(self.error)
            self.transport.loseConnection()
            return True
        return False

    def invokeNext(self):
        if self.sended[0] is not None:
            try:
                action  = COMMANDMAP[self.sended[0]]
                command = self.sended[1]
            except KeyError:
                if self.handleError("unknown command: " + self.sended[0]):
                    return
        else:
            action  = None
            command = None
        try:
            if self.task.next(self.sended[0], self.sended[1]):
                self.result = None
            else:
                self.transport.loseConnection()
        except Exception, e:
            self.handleError(str(e))

    def lineReceived(self, line):
        print "<<< " + line
        line = line.strip()
        if self.state == self.INITIALIZED:
            if not line.startswith('rpync-agent'):
                self.state = self.ERROR
                self.log.error("invalid agent greeting: " + line)
                self.transport.loseConnection()
            else:
                self.invokeNext()
                self.state = self.RUNNING
        elif self.state == self.RUNNING:
            if line == 'ok':
                self.invokeNext()
            elif line.startswith('error: '):
                self.handleError(line[len('error: '):])
            else:
                if self.result is None:
                    self.result = list()
                self.result.append(line)
        else:
            self.transport.loseConnection()

    def buildCommand(self, name, *args, **kwargs):
        parts = [str(name)]
        for arg in args:
            arg = str(arg)
            if arg.find(' ') >= 0:
                parts.append("\"{0}\"".format(arg))
            else:
                parts.append(arg)
        for name, value in kwargs.iteritems():
            value = str(value)
            if value.find(' ') >= 0:
                value = "\"{0}\"".format(value)
            if len(name) == 1:
                parts.append("-{0} {1}".format(name, value))
            else:
                parts.append("--{0}={1}".format(name, value))
        return " ".join(parts)

    def sendCommand(self, name, *args, **kwargs):
        if len(args) > 0 or len(kwargs) > 0:
            command = self.buildCommand(name, *args, **kwargs)
        else:
            command = name
            name    = command.split(None, 1)[0]
        self.sended = (name, command)
        print ">>> " + command
        self.transport.write(command + "\r\n")

class AgentTaskFactory(BaseClientProtocolFactory):
    def __init__(self, task):
        assert isinstance(task, AgentTask)
        self.task = task

    def __newProtocol__(self, addr, pid):
        return AgentTaskProtocol(self, pid)

