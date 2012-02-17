import os
import os.path

from rpync.common.config import getConfig, ConfigParser
from rpync.common.logger import getLogger

CLIENT_CONFIGS = None

class ClientConfig(ConfigParser):
    def __init__(self, name):
        global CLIENT_CONFIGS
        if CLIENT_CONFIGS is None:
            raise ValueError, "Client configurations are not inizialized"
        super(ClientConfig, self).__init__()
        if name in CLIENT_CONFIGS and isinstance(CLIENT_CONFIGS[name], ClientConfig):
            raise ValueError, "Duplicate client configuration: "+name
        self.name = name
        self.__init_config__()

    def __init_config__(self):
        clientdir  = getConfig().get('global', 'clientdir')
        clientfile = os.path.join(clientdir, self.name+".conf")
        self.read(clientfile)

def getClientConfig(name):
    global CLIENT_CONFIGS
    if CLIENT_CONFIGS is None:
        raise ValueError, "Client configurations are not inizialized"
    config = CLIENT_CONFIGS[name]
    if config == name:
        config               = ClientConfig(name)
        CLIENT_CONFIGS[name] = config
    return config

def initClientConfigs():
    global CLIENT_CONFIGS
    if CLIENT_CONFIGS is None:
        log            = getLogger()
        cfg            = getConfig()
        clientdir      = getConfig().get('global', 'clientdir')
        CLIENT_CONFIGS = dict()
        if os.path.isdir(clientdir):
            for entry in os.listdir(clientdir):
                name, ext = os.path.splitext(entry)
                filename  = os.path.join(clientdir, entry)
                if os.path.isfile(filename) and ext == '.conf':
                    CLIENT_CONFIGS[name] = name
        else:
            log.error("Client directory doesn't exist: {0}".format(clientdir))

