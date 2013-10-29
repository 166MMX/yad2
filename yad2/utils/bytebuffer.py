#!/usr/bin/env python
import struct
import os
import io
import sys
import traceback
import logging


class ByteBuffer:

    def __init__(self, stream):
        self.logger = logging.getLogger('root')
        self.stream = io.BytesIO(stream)
        self.counter = 0

    def length(self):
        return len(self.readall())

    def readall(self):
        self.stream.seek(0)
        res = self.stream.read()
        self.stream.seek(0)
        return res

    def getShort(self):
        self.counter += 2
        return self.stream.read(2)

    def get(self, position=-111111111):
        if position == -111111111:
            self.counter += 1
            return self.stream.read(1)
        else:
            cur = int(self.stream.tell())
            if cur + position < 0:
                position = 0

            self.stream.seek(position)
            x = self.stream.read(1)
            self.stream.seek(cur)
            return x

    def tell(self):
        return int(self.stream.tell())

    def seek(self, position):
        self.stream.seek(position)

    def put(self, content):
        return self.stream.write(content)

    def read(self):
        return self.stream.read()
