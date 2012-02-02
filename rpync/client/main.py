from optparse import OptionParser

from rpync.client.backup import Backup
from rpync.common.config import initConfig
from rpync.common.logger import initLogger

def main():

    def initOptions():
        opt = OptionParser(usage="usage: %prog [options] [jobs]")
        opt.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False,
                       help='be expressive on whats going on.')
        opt.add_option('-q', '--quiet', action='store_false', dest='verbose',
                       help='keep the console output to a minimum.')
        opt.add_option('-d', '--debug', action='store_true', dest='debug', default=False,
                       help='emit debug messages to file log and to the console if verbose is set.')
        opt.add_option('-c', '--config', action='store', type='string', dest='config',
                       default=None, help='Configuration file.')
        opt.add_option('-b', '--backup', action='store_true', dest='backup', default=False,
                       help='run the backup jobs. Defaults to all, if no jobs are given.')
        opt.add_option('-p', '--purge', action='store_true', dest='purge', default=False,
                       help='run the purge jobs. Defaults to all, if no jobs are given.')
        return opt

    try:
        options,jobnames = initOptions().parse_args()
        config           = initConfig('client', options.config)
        log              = initLogger(options.verbose, options.debug)
    except Exception, e:
        print "Error:", e
        return 1
    try:
        if options.backup:
            Backup().run(options, config, *jobnames)
        return 0
    except Exception, e:
        log.error(e)
        return 1

