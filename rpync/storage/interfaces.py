from zope.interface import Interface, Attribute

class IStorage(Interface):
    """Server storage interface"""

    def createJob(clientName, jobName, timestamp):
        """Create a new job object for storage"""

class IStorageJob(Interface):
    """Server storage job interface"""
    jid = Attribute("""Job ID""")

    def close():
        """Close the job and free any bound resources"""

    def processFile(fileinfo):
        """Process the file defined by file info"""
