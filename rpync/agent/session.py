import os.path
import re

from rpync.common.server import ActionError

class SessionError(ActionError):
    pass

class Session(object):
    def __init__(self):
        self._includes = list()
        self._excludes = list()
        self._basedir  = None
        self._walker   = None

    def addInclude(self, include):
        include = str(include)
        if not os.path.exists(include):
            raise ValueError, "non existing path: " + include
        if not os.path.isdir(include):
            raise ValueError, "include is not a path: " + include
        if not os.path.isabs(include):
            raise ValueError, "include is not an absolute path: " + include
        include = os.path.normpath(include)
        self._includes.append(include)

    def getIncludes(self):
        return self._includes

    def addExclude(self, exclude):
        exclude = str(exclude)
        try:
            regex = re.compile(exclude)
        except re.error, e:
            raise ValueError, str(e)
        self._excludes.append((exclude, regex))

    def getExcludes(self):
        return self._excludes

    def getWalker(self):
        if self._basedir is None:
            raise ValueError, "session is not committed"
        if self._walker is None:
            return self.nextWalker()
        return self._walker

    def nextWalker(self):
        if self._basedir is None:
            raise ValueError, "session is not committed"
        basedir      = self._basedir.next()
        walker       = os.walk(basedir)
        self._walker = (basedir, walker)
        return self._walker

    def commit(self):
        if len(self._includes) == 0:
            raise SessionError, "no includes specified"
        includes = list()
        for include in self._includes:
            for prefix in includes:
                if include.startswith(prefix):
                    include = prefix
                    break
            if include not in includes:
                includes.append(include)
        includes.sort()
        self._includes = tuple(includes)
        self._excludes = tuple(self._excludes)
        self._basedir  = iter(self._includes)
        self._walker   = None

