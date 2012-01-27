# backup command

from command import Command

class Backup(Command):
    def __init__(self, log_handlers):
        Command.__init__(self, 'backup', log_handlers)

    def run(self, options, config, *jobs):
        Command.run(self, options, config, *jobs)

