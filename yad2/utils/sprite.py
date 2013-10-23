import Image
import os
import hashlib
import logging
from pal import Pal

class Sprite:
    
    def __init__(self, x, y, lookup = []):
        self.x = x
        self.y = y
        self.lookup = lookup
        self.fraction = 0
        self.logger = logging.getLogger('root')
        self.array = [[0 for x in xrange(y)] for x in xrange(x)]
        self.palette = Pal(filename="output/IBM.PAL").read()

    def putpalette(self, pal):
        self.palette = pal

    def brigthness(self, b = 4.0):
        self.b = b

    def putpixel(self, x, y, color):
        self.array[x][y] = color

    def zoom(self, z = 1):
        self.z = z

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
                self.image.putpixel((x,y), self.array[x][y])

        if dir != '':
            try:
                os.makedirs('tmp/' + dir)    
            except:
                pass
            finally:
                dir += "/"
        if outname == '':
            outname = str(hashlib.md5(str(self.image)).hexdigest())
        outname += ".png"
        self.logger.debug("save tmp/%s%s" % (dir, outname))
        self.image = self.image.convert('RGB').point(lambda p: p * self.b)
        self.image = self.image.resize((self.image.size[0]*self.z,self.image.size[1]*self.z))
        self.image.save("tmp/" + dir + outname, format= 'PNG')
