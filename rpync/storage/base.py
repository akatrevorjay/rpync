import threading

from zope.interface import implements

from rpync.common.config      import getConfig
from rpync.common.logger      import getLogger
from rpync.storage.interfaces import IStorage, IStorageJob

counter     = 0L
counterLock = threading.Lock()

class BaseStorage(object):
    implements(IStorage)

    def __init__(self, section):
        self.config  = getConfig()
        self.section = section
        self.log     = getLogger('storage')
        self.joblist = list()
        if not self.config.has_section(self.section):
            msg = "unknown section: "+section
            self.log.error(msg)
            raise ValueError, msg

    def __enter__(self):
        return self

    def __exit__(except_type, except_value, traceback):
        try:
            self.close()
            return False
        except Exception:
            if except_type is None:
                raise

    def newJobId(self):
        global counter, counterLock
        with counterLock:
            counter += 1
            return counter

    def createJob(self, clientName, jobName):
        raise NotImplementedError

    def close(self):
        while len(self.joblist) > 0:
            self.joblist[0].close()

class BaseStorageJob(object):
    implements(IStorageJob)

    def __init__(self, storage):
        assert isinstance(storage, BaseStorage)
        self.storage = storage
        self.jid     = self.storage.newJobId()
        self.log     = getLogger('storage', str(self.jid))

    def __enter__(self):
        return self

    def __exit__(except_type, except_value, traceback):
        try:
            self.close()
            return False
        except Exception:
            if except_type is None:
                raise

    def processFile(self, fileinfo):
        raise NotImplementedError

    def close(self):
        if self.storage is not None:
            del self.storage.joblist[self.storage.joblist.index(self)]
            self.storage = None

