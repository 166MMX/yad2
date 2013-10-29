import struct
import os
import Image
import ImageDraw
import ImageEnhance
import glob
import random
import io
import hashlib
import sys
import logging
from construct import *
from pyx import *
from yad2.encoders import Format2, Format80
from yad2.utils import Pal
from yad2.utils import Sprite


class Shp:

    class Chunk:

        class Header:

            def __init__(self, header):
                self.h = io.BytesIO(header)
                self.flags = struct.unpack('H', self.h.read(2))[0]
                self.slices = struct.unpack('B', self.h.read(1))[0]
                self.width = struct.unpack('H', self.h.read(2))[0]
                self.height = struct.unpack('B', self.h.read(1))[0]
                self.filesize = struct.unpack('H', self.h.read(2))[0]
                self.datasize = struct.unpack('H', self.h.read(2))[0]

        class Data:

            def __init__(self, header, data):
                self.logger = logging.getLogger('root')
                self.header = header
                self.data = io.BytesIO(data)
                self.houseID = 0

            def decode(self):
                lookup = self.header.flags & 0b00000001
                nocompression = (self.header.flags & 0b00000010) >> 1
                vllt = (self.header.flags & 0b00000100) >> 2

                self.logger.debug("lookup " + str(lookup) + ", nocompression " + str(nocompression) + ", vllt " + str(vllt) + ", slices " + str(self.header.slices) + ", size " + str(self.header.width) + "x" + str(self.header.height) + ", points " + str(self.header.width * self.header.height) + ", fs " + str(self.header.filesize) + ", ds " + str(self.header.datasize))

                lookup_table = []
                if lookup == 1:
                    if vllt == 1:
                        raise "NOT IMPLEMENTED"
                    if vllt == 0:
                        for i in xrange(16):
                            lookup_table.append(struct.unpack('B', self.data.read(1))[0])

                data = self.data.read()
                if nocompression == 0:
                    data = Format80(data).decode()
                points = Format2(data).decode()

                sprite = Sprite(self.header.width, self.header.height)
                for index, pixel in enumerate(points):
                    color = struct.unpack('B', pixel)[0]
                    if index > self.header.width * self.header.height - 1:
                        break
                    if len(lookup_table) > 0:
                        color = lookup_table[color] + self.houseID
                    sprite.putpixel(index % self.header.width, int(index / self.header.width), color)
                return sprite

    def __init__(self, filename):
        self.logger = logging.getLogger('root')
        self.filename = filename
        self.filesize = os.path.getsize(self.filename)
        self.offset = 2
        with open(self.filename, "rb") as f:
            f.seek(4)
            if struct.unpack('B', f.read(1))[0] == 0:
                self.offset = 4
        self.logger.debug("Index offset of %s bytes" % self.offset)
        self.chunks = self._find_chunks()

    def _find_chunks(self):
        chunks = []
        with open(self.filename, "rb") as f:
            for i in range(0, struct.unpack('H', f.read(2))[0] + 1):
                if self.offset == 2:
                    chunks.append(struct.unpack('H', f.read(2))[0] + 2)
                elif self.offset == 4:
                    chunks.append(struct.unpack('I', f.read(4))[0] + 2)

        self.logger.info("Images found %d" % (len(chunks) - 1))
        return chunks

    def extract(self):
        images = []
        with open(self.filename, "rb") as f:
            for i in range(0, len(self.chunks) - 1):
                length = self.chunks[i + 1] - self.chunks[i]
                f.seek(self.chunks[i])
                head = Shp.Chunk.Header(f.read(10))
                data = Shp.Chunk.Data(head, f.read(head.filesize))
                images.append((str(i), data.decode()))

        self.logger.info("Images extracted %d" % len(images))
        return images
