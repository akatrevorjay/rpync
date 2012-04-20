from rpync.common.config             import getConfig, ConfigParser
from rpync.common.logger             import getLogger
from rpync.server.storage.base       import BaseStorage
from rpync.server.storage.file       import FileStorage
from rpync.server.storage.interfaces import IStorage

STORAGE_INSTANCE = None
SECTION          = 'storage'

def getStorage():
    global STORAGE_INSTANCE
    if STORAGE_INSTANCE is None:
        msg = "storage is not inizialized"
        getLogger().error(msg)
        raise ValueError, msg
    return STORAGE_INSTANCE

def createStorage(config, section):
    assert isinstance(config, ConfigParser)
    package, classname = config.get(section, 'class').rsplit('.', 1)
    module             = __import__(package, fromlist=[classname])
    storageClass       = getattr(module, classname)
    if not IStorage.implementedBy(storageClass):
        msg = "'{0}.{1}' does not implement IStorage interface".format(package, classname)
        getLogger('storage').error(msg)
        raise ValueError, msg
    return storageClass(section)

def initStorage():
    global STORAGE_INSTANCE
    if STORAGE_INSTANCE is None:
        getLogger().info("initializing storage")
        STORAGE_INSTANCE = createStorage(getConfig(), SECTION)

#        config             = getConfig()
#        package, classname = config.get(SECTION, 'class').rsplit('.', 1)
#        module             = __import__(package, fromlist=[classname])
#        storageClass       = getattr(module, classname)
#        if not IStorage.implementedBy(storageClass):
#            raise ValueError, "'{0}.{1}' does not implement IStorage interface".format(package, classname)
#        STORAGE_INSTANCE = storageClass(SECTION)
