import os.path

from rpync.agent.states  import STATE_RUNNING
from rpync.common        import fileinfo
from rpync.common.server import Action, ActionError

class ActionNext(Action):
    def __init__(self, server):
        super(ActionNext, self).__init__('next', server)

    def doAction(self, options, args):
        if self.server.getState() != STATE_RUNNING:
            raise ActionError, "invalid state for action next: {0}".format(self.server.getState())
        basedir, walker = self.server.session.getWalker()
        try:
            return self.doWalk(*self.server.session.getWalker())
        except StopIteration:
            try:
                return self.doWalk(*self.server.session.nextWalker())
            except StopIteration:
                self.server.transport.write("finished\r\n")
                return True

    def doWalk(self, basedir, walker):
        excludes          = self.server.session.getExcludes()
        base, dirs, files = walker.next()
        self.server.transport.write("basedir: {0}\r\n".format(basedir))
        for names in (dirs, files):
            for name in names:
                include = True
                path    = os.path.join(base, name)
                for value, pattern in excludes:
                    if pattern.match(path):
                        names.remove(name)
                        include = False
                        break
                if include:
                    info = fileinfo.make(path)
                    self.server.transport.write("fileinfo: {0}\r\n".format(info.dumps()))
        return True

