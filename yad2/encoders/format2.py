import struct
import os
import io
import sys
import logging


class Format2:

    def __init__(self, st):
        self.logger = logging.getLogger('root')
        self.st = io.BytesIO(st)
        self.logger.debug("in " + str(len(st)))

    def decode(self):
        output = io.BytesIO()
        while 1:
            try:
                rcmd = self.st.read(1)
                cmd = struct.unpack('B', rcmd)[0]
                if cmd == 0:
                    count = struct.unpack('B', self.st.read(1))[0]
                    for i in range(0, count):
                        output.write(rcmd)
                else:
                    output.write(rcmd)
            except Exception as e:
                break
        output.seek(0)
        self.logger.debug("out " + str(len(output.read())))
        output.seek(0)
        return bytes(output.read())
