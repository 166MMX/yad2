import Image
import os
import hashlib
import logging
from pal import Pal


class Sprite:

    def __init__(self, x, y, lookup=[]):
        self.x = x
        self.y = y
        self.lookup = lookup
        self.fraction = 0
        self.logger = logging.getLogger('root')
        self.array = [[0 for x in xrange(self.x)] for x in xrange(self.y)]
        self.palette = Pal(filename="output/IBM.PAL").read()

    def putpalette(self, pal):
        self.palette = pal

    def brigthness(self, b=4.0):
        self.b = b

    def putpixel(self, x, y, color):
        self.array[y][x] = color

    def zoom(self, z=1):
        self.z = z

    def stretch(self, target_size):
        self.array2 = [[0 for x in xrange(target_size)] for x in xrange(target_size)]
        for y in xrange(self.y):
            for x in xrange(self.x):
                self.array2[y][x * 2] = self.array[y][x]
                self.array2[y][x * 2 + 1] = self.array[y][x]
        self.y = target_size
        self.x = target_size
        self.array = self.array2

    def fractionize(self):
        if len(self.lookup) > 0:
            pass
        pass

    def fraction(self, fraction):
        self.fraction = fraction

    def write(self, outname='', dir=''):
        self.image = Image.new("L", (self.x, self.y), 255)
        self.image.putpalette(self.palette)
        self.fractionize()

        for x in xrange(self.x):
            for y in xrange(self.y):
                self.image.putpixel((x, y), self.array[y][x])

        path = "tmp/%s/%s.png" % (dir, outname)
        if dir != '':
            try:
                os.makedirs(os.path.dirname(path))
            except:
                pass

        self.logger.debug("Save %s" % path)
        self.image = self.image.convert('RGB').point(lambda p: p * self.b)
        self.image = self.image.resize((self.image.size[0] * self.z, self.image.size[1] * self.z))
        self.image.save(path, format='PNG')
