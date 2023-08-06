# -*- coding: utf-8 -*-

import subprocess
import sys
import msvcrt

class NoBufferingStream(object):
    def __init__(self, stream):
        self._stream = stream

    def write(self, s):
        self._stream.write(s)
        self._stream.flush()

    def __getattr__(self, attr):
        return getattr(self._stream, attr)


if __name__ == "__main__":
    msvcrt.setvbuf(msvcrt.stdout, None, _IONBF, 0)
    #sys.stdout = NoBufferingStream(sys.stdout)
    #sys.stderr = NoBufferingStream(sys.stderr)
    proc = subprocess.Popen(sys.argv[1:], shell=False, bufsize=1)
    proc.communicate()
