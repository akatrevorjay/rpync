from rpync.common.server       import Action, ActionError
from rpync.server.clientconfig import getClientConfig
from rpync.server.jobinfo      import JobInfo
from rpync.server.task         import BackupTask

class ActionBackup(Action):
    def __init__(self, server):
        super(ActionBackup, self).__init__('backup', server)

    def doAction(self, options, args):
        if len(args) != 2:
            raise ActionError, "usage: backup <client> <job>"
        try:
            jobinfo = JobInfo(args[0], args[1])
        except ValueError:
            raise ActionError, "unknown job: " + args[1]
        except KeyError:
            raise ActionError, "unknown client: " + args[0]
        task = BackupTask(jobinfo)
        task.run()
        return True
