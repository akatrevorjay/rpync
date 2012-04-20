import os
import os.path

from rpync.common.config import getConfig, ConfigParser
from rpync.common.logger import getLogger

CLIENT_CONFIGS = None

class ClientConfig(ConfigParser):
    def __init__(self, name):
        global CLIENT_CONFIGS
        if CLIENT_CONFIGS is None:
            msg = "client configurations are not inizialized"
            getLogger().error(msg)
            raise ValueError, msg
        ConfigParser.__init__(self)
        if name in CLIENT_CONFIGS and isinstance(CLIENT_CONFIGS[name], ClientConfig):
            msg = "duplicate client configuration: "+name
            getLogger().error(msg)
            raise ValueError, msg
        self.name = name
        self.__init_config__()

    def __init_config__(self):
        clientdir  = getConfig().get('global', 'clientdir')
        clientfile = os.path.join(clientdir, self.name+".conf")
        getLogger().info("loading client configuration: " + self.name)
        self.read(clientfile)
        if not (self.has_section('client') and self.has_option('client', 'address')):
            msg = "invalid job configuration"
            getLogger().error(msg)
            raise ValueError, msg

def getClientConfig(name):
    global CLIENT_CONFIGS
    if CLIENT_CONFIGS is None:
        msg = "client configurations are not inizialized"
        getLogger().error(msg)
        raise ValueError, msg
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
        log.info("initializing client configurations")
        clientdir      = getConfig().get('global', 'clientdir')
        CLIENT_CONFIGS = dict()
        if os.path.isdir(clientdir):
            for entry in os.listdir(clientdir):
                name, ext = os.path.splitext(entry)
                filename  = os.path.join(clientdir, entry)
                if os.path.isfile(filename) and ext == '.conf':
                    CLIENT_CONFIGS[name] = name
        else:
            log.error("client directory doesn't exist: {0}".format(clientdir))

