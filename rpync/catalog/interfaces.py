from zope.interface import Interface, Attribute

class ICatalog(Interface):
    """Base interface for all catalogs"""
    def __enter__():
        """Enter a with statement."""
    def __exit__(except_type, except_value, traceback):
        """Exit a with statement"""
    def close():
        """Close the catalog freeing all bound resources."""

class IIndexedCatalog(ICatalog):
    """Catalog wich can be queried. Usually with a database store"""
    def startJob(jobinfo, seqcat=None):
        """Starts a new job in the catalog. Writes to sequential catalog (seqcat) if given.
           Returns an ICatalogJob."""

class ICatalogJob(ICatalog):
    """Catalog job"""
    def addFileInfo(fileinfo, **extra):
        """Adds (appends) a file info to the catalog.
           The keyword arguments are stored in the attribute 'extra'."""

class ISquentialCatalog(ICatalogJob):
    """Catalog in flat sequential store. Usually a file"""
    def __iter__():
        """Return an iterator for this catalog""""
    def setJobInfo(jobinfo):
        """Sets the job info for this catalog. The function can and must only be called once.
           It raises ValueError otherwise."""

