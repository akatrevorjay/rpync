from rpync.server.task.base import Task

class BackupTask(Task):
    def next(self, action, command):
        if action is None:
            self.protocol.sendCommand('init')
            return True
        if action == 'init':
            self.iter = iter(self.jobinfo.includes)
            self.protocol.sendCommand('include', self.iter.next())
            return True
        if action == 'include':
            try:
                include = self.iter.next()
                self.protocol.sendCommand('include', include)
            except StopIteration:
                if len(self.jobinfo.excludes) > 0:
                    self.iter = iter(self.jobinfo.excludes)
                    self.protocol.sendCommand('exclude', self.iter.next())
                else:
                    self.protocol.sendCommand('backup')
            return True
        if action == 'backup':
            self.protocol.sendCommand('quit')
            return False
        return False

