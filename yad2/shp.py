import struct
import os
import Image, ImageDraw
import ImageEnhance
import glob
import random
import io
import hashlib 
import sys
import logging
from construct import *
from pyx import *
from format2 import Format2
from format80 import Format80
from pal import Pal
from sprite import Sprite

class Shp:

    class Header:
    
        def __init__(self, header):
            h = io.BytesIO(header)
            self.flags = struct.unpack('H', h.read(2))[0]
            self.slices = struct.unpack('B', h.read(1))[0]
            self.width = struct.unpack('H', h.read(2))[0]
            self.height = struct.unpack('B', h.read(1))[0]
            self.filesize = struct.unpack('H', h.read(2))[0]
            self.datasize = struct.unpack('H', h.read(2))[0]
    
    class Data:
        
        def __init__(self, header, data, palette):
            self.logger = logging.getLogger('root')
            self.header = header
            self.data = io.BytesIO(data)
            self.palette = palette
    
        def decode(self):
            houseID=0

            image = Image.new("L", (self.header.width, self.header.height), 255)
            image.putpalette(self.palette)
            draw = ImageDraw.Draw(image)
            draw.rectangle( [(0,0),(self.header.width, self.header.height)], fill=16 )
            points = []
    
            lookup = self.header.flags & 0b00000001
            nocomp = (self.header.flags & 0b00000010) >> 1
            vllt = (self.header.flags & 0b00000100) >> 2
    
            self.logger.info("lookup " + str(lookup) + ", nocomp " + str(nocomp) + ", vllt " + str(vllt) + ", slices " + str(self.header.slices) + ", size " + str(self.header.width)+"x"+str(self.header.height) + ", points " + str(self.header.width*self.header.height) + ", fs " + str(self.header.filesize) + ", ds " + str(self.header.datasize))
            
            lookup_table = []
            if lookup == 1:
                if vllt == 1:
                    raise "NOT IMPLEMENTED"
                if vllt == 0:
                    for i in xrange(16):
                        lookup_table.append(struct.unpack('B', self.data.read(1))[0])
    
            if nocomp == 0:
                points = Format2(Format80(self.data.read()).decode()).decode()
            if nocomp == 1:
                points = Format2(self.data.read()).decode()
    
            index = 0
            for index, pixel in enumerate(points):
                color = struct.unpack('B', pixel)[0]
                if index > self.header.width*self.header.height -1:
                    break
                if len(lookup_table) > 0:
                    color = lookup_table[color] + houseID
                image.putpixel((index%self.header.width, int(index/self.header.width)), color)
            return (image, index)

    def __init__(self, filename):
        self.logger = logging.getLogger('root')
        self.filename = filename
        self.filesize = os.path.getsize(self.filename)
        self.palette = Pal(filename="output/IBM.PAL").read()
        self.offsetsize = self.find_offset()

    def find_offset(self):
        f = open(self.filename,"rb")
        offset = 2
        f.seek(4)
        if struct.unpack('B', f.read(1))[0] == 0:
            offset = 4
        self.logger.debug("index offset of %s bytes" % offset)
        f.close
        return offset

    def extract(self):
        f = open(self.filename,"rb")
        numoffsets = struct.unpack('H', f.read(2))[0]+1
        self.logger.info("Images found " + str(numoffsets-1))
        offsets = []

        for i in range(0, numoffsets):
            if self.offsetsize == 2:
                offsets.append(struct.unpack('H', f.read(2))[0]+2)
            elif self.offsetsize == 4:
                offsets.append(struct.unpack('I', f.read(4))[0]+2)

        for i in range(0, len(offsets)-1):
            length = offsets[i+1]-offsets[i]
            f.seek(offsets[i])
            head = Shp.Header(f.read(10))
            data = Shp.Data(head, f.read(head.filesize), self.palette)
            image, size = data.decode()

            s = Sprite(image)
            s.write(drr = "shp/%s" % os.path.splitext(os.path.basename(self.filename))[0].lower(), outname = '%d' % i)

        self.logger.info("Images extracted " + str(len(offsets)-1))
        f.close()
