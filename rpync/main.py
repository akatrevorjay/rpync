import logging
import sys
import os.path

from ConfigParser import SafeConfigParser as ConfigParser
from optparse     import OptionParser

from rpync.backup import Backup
from rpync.job    import Job

SYS_CONFIG_FILE = '/etc/rpync/main.conf'
USR_CONFIG_FILE = os.path.expanduser('~/.rpync.conf')
DEF_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'default.conf')

def main():

    def init_options():
        opt = OptionParser(usage="usage: %prog [options] [jobs]")
        opt.add_option('-v','--verbose',action='store_true',dest='verbose',default=False,
                       help='be expressive on whats going on.')
        opt.add_option('-q','--quiet',action='store_false',dest='verbose',
                       help='keep the console output to a minimum.')
        opt.add_option('-d','--debug',action='store_true',dest='debug',default=False,
                       help='emit debug messages to file log and to the console if verbose is set.')
        opt.add_option('-c','--config',action='store',type='string',dest='config',
                       default=SYS_CONFIG_FILE,
                       help='Configuration file.')
        opt.add_option('-b','--backup',action='store_true',dest='backup',default=False,
                       help='run the backup jobs. Defaults to all, if no jobs are given.')
        opt.add_option('-p','--purge',action='store_true',dest='purge',default=False,
                       help='run the purge jobs. Defaults to all, if no jobs are given.')
        return opt

    def init_config(config=None):
        files = [DEF_CONFIG_FILE, SYS_CONFIG_FILE, USR_CONFIG_FILE]
        cfg   = ConfigParser()
        if config is not None:
            files.append(config)
        print cfg.read(files)
        return cfg

    def init_logger(config, verbose=False, debug=False):
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
        file_handler   = logging.FileHandler(config.get('global', 'logfile'),'wb')
        file_handler.setLevel(logging.DEBUG if debug else logging.INFO)
        file_handler.setFormatter(file_formatter)
        # Initialize logger
        log = logging.getLogger('rpync')
        log.setLevel(logging.DEBUG)
        log.addHandler(console_handler)
        log.addHandler(file_handler)
        return (log, (console_handler, file_handler))

    def init_jobs(log, config, jobnames):
        log.info("Setting up jobs ...")
        jobs = list()
        for name in jobnames:
            log.info("Job: {0}".format(name))
            jobs.append(Job(name, log, config))
        return tuple(jobs)

    try:
        parser           = init_options()
        options,jobnames = parser.parse_args()
        config           = init_config(options.config)
        log,handlers     = init_logger(config, verbose=options.verbose, debug=options.debug)
    except Exception, e:
        print "Error:", e
        return 1
    try:
        jobs             = init_jobs(log, config, jobnames)
        if options.backup:
            Backup(handlers).run(options, config, *jobs)
        return 0
    except Exception, e:
        log.error(e)
        return 1
