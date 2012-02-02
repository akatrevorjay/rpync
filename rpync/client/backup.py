# backup command

from rpync.common.command import Command

class Backup(Command):
    def __init__(self):
        Command.__init__(self, 'backup')

    def run(self, options, config, *jobs):
        Command.run(self, options, config, *jobs)

