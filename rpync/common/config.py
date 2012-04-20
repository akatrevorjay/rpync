import os.path
import re
import rpync

from ConfigParser import SafeConfigParser

LIST_PATTERN    = re.compile(r'\s*("[^"]*"|.*?)\s*,')
SYS_CONFIG_FILE = None
USR_CONFIG_FILE = None
DEF_CONFIG_PATH = os.path.dirname(rpync.__file__)
DEF_CONFIG_FILE = None
CFG             = None
CFG_TYPE        = None

class ConfigParser(SafeConfigParser):
    def getlist(self, section, option):
        value = self.get(section, option)
        # Credits to: Armin Ronacher (http://stackoverflow.com/users/19990/armin-ronacher)
        return [x[1:-1] if x[:1] == x[-1:] == '"' else x
            for x in LIST_PATTERN.findall(value.rstrip(',') + ',')]

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
    global CFG, CFG_TYPE, DEF_CONFIG_FILE, DEF_CONFIG_PATH, SYS_CONFIG_FILE, USR_CONFIG_FILE
    if CFG is None:
        if config_type in ('agent', 'client', 'server'):
            DEF_CONFIG_FILE = os.path.join(DEF_CONFIG_PATH, config_type, "default.conf")
            SYS_CONFIG_FILE = "/etc/rpync/{0}.conf".format(config_type)
            USR_CONFIG_FILE = os.path.expanduser("~/.rpync-{0}.conf".format(config_type))
            CFG_TYPE        = config_type
        else:
            raise ValueError
        files = [DEF_CONFIG_FILE, SYS_CONFIG_FILE, USR_CONFIG_FILE]
        CFG   = ConfigParser()
        if config_file is not None:
            files.append(config_file)
        CFG.read(files)
        CFG.set('global', 'type', config_type)

