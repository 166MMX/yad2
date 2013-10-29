import struct
import os
import io


class Pal:

    def __init__(self, **kwargs):
        if 'filename' in kwargs.keys():
            f = open(kwargs['filename'], "rb")
            self.stream = io.BytesIO(f.read())
            f.close()
        if 'inline' in kwargs.keys():
            self.stream = io.BytesIO(kwargs['inline'])

    def read(self):
        out = []
        try:
            while 1:
                out.append(struct.unpack('B', self.stream.read(1))[0])
        except:
            pass
        return out
