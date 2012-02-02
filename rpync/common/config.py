import os.path

from ConfigParser import SafeConfigParser as ConfigParser

SYS_CONFIG_FILE = None
USR_CONFIG_FILE = os.path.expanduser('~/.rpync.conf')
DEF_CONFIG_PATH = os.path.dirname(__file__)
DEF_CONFIG_FILE = None
CFG             = None
CFG_TYPE        = None

def getConfig():
    global CFG
    if CFG is None:
        raise ValueError, "Configuration is not inizialized"
    return CFG

def getConfigType():
    global CFG_TYPE
    if CFG_TYPE is None:
        raise ValueError, "Configuration is not inizialized"
    return CFG_TYPE

def initConfig(config_type, config_file=None):
    global CFG, CFG_TYPE, DEF_CONFIG_FILE, SYS_CONFIG_FILE
    if CFG is None:
        if config_type in ('agent', 'client', 'server'):
            DEF_CONFIG_FILE = os.path.join(DEF_CONFIG_PATH, "default-{0}.conf".format(config_type))
            SYS_CONFIG_FILE = "/etc/rpync/{0}.conf".format(config_type)
            CFG_TYPE        = config_type
        else:
            raise ValueError
        files = [DEF_CONFIG_FILE, SYS_CONFIG_FILE, USR_CONFIG_FILE]
        CFG   = ConfigParser()
        if config_file is not None:
            files.append(config_file)
        CFG.read(files)
        CFG.set('global', 'type', config_type)
    return CFG

