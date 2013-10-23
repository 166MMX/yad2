import Image
import os
import hashlib
import logging

class Sprite:
    
    def __init__(self, image):
        self.logger = logging.getLogger('root')
        self.image = image
        self.brigthen()
        self.zoom()

    def brigthen(self):
        self.image = self.image.convert('RGB').point(lambda p: p * 4.0)
        True

    def zoom(self, factor = 2):
        self.image = self.image.resize((self.image.size[0]*factor,self.image.size[1]*factor))

    def write(self, outname='', dir=''):
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
        self.image.save("tmp/" + dir + outname, format= 'PNG')
