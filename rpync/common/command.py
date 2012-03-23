from rpync.common.server import RE_NAME

from twisted.protocols.basic import LineReceiver

class Command(object):
    def __init__(self, name):
        assert isinstance(name, basestring)
        if RE_NAME.match(name) is None:
            raise ValueError, "Invalid command name: " + name
        self.name = name

class CommandProtocol(LineReceiver):
    def __init__(self, callback):
        self.sended   = None
        self.success  = None
        self.error    = None
        self.result   = None
        self.callback = callback

    def setSuccess(self):
        self.success = True
        self.error   = None
        self.transport.loseConnection()
        if callback is not None:
            callback(self)

    def setError(self, msg):
        self.success = False
        self.error   = msg
        self.transport.loseConnection()
        if callback is not None:
            callback(self)

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
        if self.error is None:
            self.result  = list()
            self.success = None
            if len(args) > 0 or len(kwargs) > 0:
                command = self.buildCommand(name, *args, **kwargs)
            else:
                command = name
                name    = command.split(None, 1)[0]
            self.sended = (name, command)
            self.transport.write(command + "\r\n")

    def lineReceived(self, line):
        line = line.strip()
        if self.success is None:
            if self.sended is None:
                if not line.startswith('rpync-agent'):
                    self.setError("unknown greeting by agent")
            elif line == 'ok':
                self.setSuccess()
            elif line.startswith('error:'):
                self.setError(line[len('error: '):])
            else:
                self.result.append(line)

