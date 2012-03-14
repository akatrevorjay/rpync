from optparse import OptionParser

from rpync.common.config import initConfig
from rpync.common.logger import initLogger, getLogger
from rpync.server.server import ServerFactory

from twisted.internet import reactor

PARSER  = None
OPTIONS = None
ARGS    = None

def initOptions():
    global PARSER, OPTIONS, ARGS
    if PARSER is None:
        PARSER = OptionParser(usage="usage: %prog [options]")
        PARSER.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                          help='be expressive on whats going on.')
        PARSER.add_option('-q', '--quiet', action='store_false', dest='verbose',
                          help='keep the console output to a minimum.')
        PARSER.add_option('-d', '--debug', action='store_true', dest='debug', default=False,
                          help='emit debug messages to file log and to the console if verbose is set.')
        PARSER.add_option('-c', '--config', action='store', type='string', dest='config',
                          default=None, help='Configuration file.')
        OPTIONS, ARGS = PARSER.parse_args()

def main():
    try:
        initOptions()
        initConfig('server', OPTIONS.config)
        initLogger(OPTIONS.verbose, OPTIONS.debug)
        log = getLogger()
    except Exception, e:
        print "Error:", e
        raise
        return 1

    try:
        if len(ARGS) > 0:
            raise ValueError, "Invalid arguments: "+args
        reactor.listenTCP(1080, ServerFactory())
        reactor.run()
        return 0
    except Exception, e:
        log.error(e)
        raise
        return 1

