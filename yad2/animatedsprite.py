import Image
import hashlib

class AnimatedSprite:
    
    def __init__(self, timing):
        self.image = image
        self.brigthen()
        self.zoom()

    def brigthen(self):
        self.image = self.image.convert('RGB').point(lambda p: p * 4.0)
        True

    def zoom(self, factor = 4):
        self.image = self.image.resize((self.image.size[0]*factor,self.image.size[1]*factor))

    def frame(self, image):
        pass

    def write(self, outname = ''):
        if outname == '':
            outname = str(hashlib.md5(str(self.image)).hexdigest())
        outname += ".png"
        self.image.save("tmp/" + outname, format= 'PNG')
