import hashlib, os

M = long(2**16)

class BlockChecksum(object):
    def __init__(self, blocksize=512):
        self._file       = None
        self._block      = None
        self._blockcount = 0L
        self._blocksize  = long(blocksize)

    def open(self, filename):
        self.close()
        self._file       = open(filename, 'rb')
        self._block      = None
        self._blockcount = 0L
        self._file.seek(0,os.SEEK_END)
        self._filesize   = self._file.tell()
        self._file.seek(0,os.SEEK_SET)
        return self

    def close(self):
        if self._file is not None:
            self._file.close()
        self._file       = None
        self._block      = None
        self._blockcount = 0

    def _checksum(self, offset, block):
        s = min(len(block), self._blocksize)
        l = long(offset + s - 1)
        a = b = long(0)
        for i in xrange(s):
            a += long(ord(block[i]))
            b += a
        return a, b, (a%M) + M * (b%M)

    def weak_checksum(self, offset=None):
        if self._file is None:
            raise IOError, "Stream is closed"
        if offset is None:
            if self._block is None:
                raise IOError
            return self._checksum(offset, self._block)[2]
        elif offset < self._filesize:
            index = self._file.tell()
            self._file.seek(offset)
            block = self._file.read(self._blocksize)
            self._file.seek(index)
            return self._checksum(offset, block)[2]
        else:
            raise EOFError

    def strong_checksum(self, offset=None):
        if self._file is None:
            raise IOError, "Stream is closed"
        algo = hashlib.new('sha256')
        if offset is None:
            if self._block is None:
                raise IOError
            algo.update(self._block)
        elif offset < self._filesize:
            index = self._file.tell()
            self._file.seek(offset)
            algo.update(self._file.read(self._blocksize))
            self._file.seek(index)
        else:
            raise EOFError
        return algo.hexdigest()

    def read(self):
        if self._file is None:
            raise IOError, "Stream is closed"
        self._block = self._file.read(self._blocksize)
        if len(self._block) > 0:
            offset            = self._blockcount * self._blocksize
            self._blockcount += 1L
            a, b, csum        = self._checksum(offset, self._block)
            return offset, long(len(self._block)), csum
        else:
            return (0L,0L,0L)

    def __iter__(self):
        return self

    def __enter__(self):
        return self

    def __exit__(self, etype, e, traceback):
        if self._file is not None:
            try:
                self.close()
            except Exception:
                pass
        return False

    def next(self):
        try:
            retval = self.read()
            if retval[1] == 0:
                raise StopIteration
            return retval
        except IOError:
            raise StopIteration

class RollingChecksum(BlockChecksum):
    def __init__(self, blocksize=512):
        BlockChecksum.__init__(self, blocksize)
        self._blockoffset = 0L
        self._a = self._b = None
        self._k = self._l = None

    def _rolling_checksum(self):
        def X(i):
            i -= self._blockoffset
            if i < len(self._block[0]):
                return ord(self._block[0][i])
            elif i < len(self._block[0]) + len(self._block[1]):
                return ord(self._block[1][i-self._blocksize])
            else:
                self._block        = (self._block[1], self._file.read(self._blocksize))
                self._blockcount  += 1
                self._blockoffset += self._blocksize
                return X(i+self._blockoffset-self._blocksize)

        if self._l+1L < self._filesize:
            self._l += 1L
            self._a  = (self._a - X(self._k) + X(self._l)) % M
            self._b  = (self._b - (self._l - self._k) * X(self._k) + self._a) % M
            self._k += 1L
            return self._k, self._blocksize, self._a + M * self._b
        return (0L,0L,0L)

    def close(self):
        BlockChecksum.close(self)
        self._blockoffset = 0L
        self._a = self._b = None
        self._k = self._l = None

    def weak_checksum(self, offset=None):
        if self._file is None:
            raise IOError, "Stream is closed"
        if offset is None:
            if self._block is None:
                raise IOError
            return self._a + M * self._b
        else:
            return BlockChecksum.weak_checksum(self, offset)

    def strong_checksum(self, offset=None):
        if self._file is None:
            raise IOError, "Stream is closed"
        if offset is None:
            if self._block is None:
                raise IOError
            k    = self._k - self._blockoffset
            l    = self._l - self._blockoffset
            algo = hashlib.new('sha256')
            if k == 0:
                algo.update(self._block[0])
            elif k == self._blocksize:
                print self._k,k,l
                algo.update(self._block[1])
            else:
                algo.update(self._block[0][k:])
                algo.update(self._block[1][:l+1])
            return algo.hexdigest()
        else:
            return BlockChecksum.strong_checksum(self, offset)

    def read(self):
        if self._file is None:
            raise IOError, "Stream is closed"
        if self._block is None:
            self._block            = (self._file.read(self._blocksize), \
                                      self._file.read(self._blocksize))
            self._blockcount       = 2
            self._blockoffset      = 0L
            self._k                = 0L
            self._l                = min(self._blocksize-1, self._filesize-1)
            self._a, self._b, csum = self._checksum(0L, self._block[0])
            return (0L, long(min(len(self._block[0]), self._blocksize)), csum)
        else:
            return self._rolling_checksum()

