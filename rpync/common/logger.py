import logging

from rpync.common.config import getConfig, getConfigType

LOG          = None
LOG_BASE     = None
LOG_HANDLERS = None

def getLogger(*args):
    global LOG
    if LOG is None:
        raise ValueError, "Logger is not initialized"
    if len(args) > 0:
        names = [LOG_BASE]
        names.extend(args)
        return logging.getLogger(".".join(names))
    return LOG

def initLogger(verbose=False, debug=False):
    global LOG, LOG_BASE, LOG_HANDLER
    if LOG is None:
        cfg      = getConfig()
        LOG_BASE = "rpync."+getConfigType()
        # Set up console formatter and handler
        console_formatter = logging.Formatter("%(name)s %(levelname)s: %(message)s")
        console_handler   = logging.StreamHandler()
        if verbose:
            console_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        else:
            console_handler.setLevel(logging.ERROR)
        console_handler.setFormatter(console_formatter)
        # Set up file formatter and handler
        file_formatter = logging.Formatter("[%(asctime)s] %(name)s %(levelname)s: %(message)s")
        file_handler   = logging.FileHandler(cfg.get('global', 'logfile'),'wb')
        file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        file_handler.setFormatter(file_formatter)
        # Initialize logger
        LOG          = logging.getLogger(LOG_BASE)
        LOG_HANDLERS = (console_handler, file_handler)
        LOG.setLevel(logging.DEBUG)
        LOG.addHandler(console_handler)
        LOG.addHandler(file_handler)

