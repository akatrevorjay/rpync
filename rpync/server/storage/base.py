from zope.interface import implements

from rpync.common.config             import getConfig
from rpync.common.logger             import getLogger
from rpync.server.storage.interfaces import IStorage

SECTION = 'storage'

class BaseStorage(object):
    implements(IStorage)

    def __init__(self):
        self.config = getConfig()
        self.log    = getLogger('storage')
