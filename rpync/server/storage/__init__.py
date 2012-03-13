from rpync.common.config             import getConfig
from rpync.common.logger             import getLogger
from rpync.server.storage.base       import BaseStorage
from rpync.server.storage.file       import FileStorage
from rpync.server.storage.interfaces import IStorage

STORAGE_INSTANCE = None

def getStorage():
    global STORAGE_INSTANCE
    if STORAGE_INSTANCE is None:
        raise ValueError, "Storage is not inizialized"
    return STORAGE_INSTANCE

def initStorage():
    global STORAGE_INSTANCE
    if STORAGE_INSTANCE is None:
        getLogger().info("Initializing storage")
        cfg                = getConfig()
        package, classname = cfg.get('storage', 'class').rsplit('.', 1)
        module             = __import__(package, fromlist=[classname])
        storageClass       = getattr(module, classname)
        if not IStorage.implementedBy(storageClass):
            raise ValueError, "'{0}.{1}' does not implement IStorage interface".format(package, classname)
        STORAGE_INSTANCE = storageClass()
