import struct
import os
import Image
import glob
import random
import io
import sys
import math
from construct import *
from pyx import *
from yad2.utils import Pal
from yad2.encoders import Format80
from yad2.utils import Sprite


class Cps:

    def __init__(self, filename):
        self.filename = filename

    def extract(self):
        f = open(self.filename, "rb")
        size = struct.unpack('H', f.read(2))[0] - 2
        unknown = struct.unpack('H', f.read(2))[0]
        isize = struct.unpack('H', f.read(2))[0]
        psize = struct.unpack('I', f.read(4))[0]
        sprite = Sprite(320, 200)
        if psize > 0:
            sprite.putpalette(Pal(inline=f.read(768)).read())

        points = Format80(f.read()).decode()
        for index, pixel in enumerate(points):
            if index >= 320 * 200:
                break
            color = struct.unpack('B', pixel)[0]
            sprite.putpixel(index % 320, int(math.floor(index / 320.0)), color)

        f.close()
        return [("0", sprite)]
