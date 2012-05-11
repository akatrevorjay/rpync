from zope.interface import Interface, Attribute

class IStorage(Interface):
    """Server storage interface"""
    def __enter__():
        """Enter a with statement."""
    def __exit__(except_type, except_value, traceback):
        """Exit a with statement"""
    def createJob(clientName, jobName, timestamp):
        """Create a new job object for storage"""
    def close():
        """Close the storage and free any bound resources"""

class IStorageJob(Interface):
    """Server storage job interface"""
    jid = Attribute("""Job ID""")

    def __enter__():
        """Enter a with statement."""
    def __exit__(except_type, except_value, traceback):
        """Exit a with statement"""
    def close():
        """Close the job and free any bound resources"""
    def processFile(fileinfo):
        """Process the file defined by file info"""
