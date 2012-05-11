import threading

from rpync.catalog.interfaces import ICatalog, ICatalogJob, IIndexedCatalog, ISquentialCatalog
from rpync.common.logger      import getLogger

from zope.interface import implements

counter     = 0L
counterLock = threading.Lock()

class BaseCatalog(object):
    implements(ICatalog)

    def __init__(self):
        self.log = getLogger('catalog')

    def __enter__(self):
        return self

    def __exit__(except_type, except_value, traceback):
        try:
            self.close()
            return False
        except Exception:
            if except_type is None:
                raise

    def close(self):
        pass

class BaseIndexedCatalog(BaseCatalog):
    implements(IIndexedCatalog)

    def __init__(self):
        super(BaseIndexedCatalog, self).__init__()
        self.joblist = list()

    def newJobId(self):
        global counter, counterLock
        with counterLock:
            counter += 1
            return counter

    def close(self):
        while len(self.joblist) > 0:
            jid = self.joblist[0].jid
            job = self.joblist[0]
            try:
                self.joblist[0].close()
            except Exception, e:
                msg = "unable to close job '{0}': {1}". format(jid, str(e))
                self.log.error(msg)
            if len(self.joblist) > 0 and self.joblist[0] == job:
                del self.joblist[0]
        super(BaseIndexedCatalog, self).close()

class BaseSquentialCatalog(BaseCatalog):
    implements(ISquentialCatalog)

    def setJobInfo(self, jobinfo):
        raise NotImplementedError

    def addFileInfo(self, fileinfo, **extra):
        raise NotImplementedError

class BaseCatalogJob(object):
    implements(ICatalogJob)

    def __init__(self, catalog):
        assert isinstance(catalog, BaseCatalog)
        self.catalog = catalog
        self.jid     = self.catalog.newJobId()
        self.log     = getLogger('catalog', str(self.jid))

    def addFileInfo(self, fileinfo, **extra):
        raise NotImplementedError

    def close(self):
        if self.storage is not None:
            del self.storage.joblist[self.storage.joblist.index(self)]
            self.storage = None

