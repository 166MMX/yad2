import struct
import os
import sys
import logging

class Pak:

    def __init__(self, filename):
        self.logger = logging.getLogger('root')
        self.filename = filename
        self.filesize = os.path.getsize(self.filename)
        self.header()
        self.logger.debug("filesize " + str(self.filesize)) 

    def header(self):
        self.files = []
        f = open(self.filename, "rb")
        while 1:
            offset = struct.unpack('I', f.read(4))[0]
            name = ''
            while 1:
                byte = struct.unpack('B', f.read(1))[0]
                if byte == 0: 
                    if struct.unpack('4B', f.read(4))[0] == 0:
                        f.close()
                        return 
                    else:
                        f.seek(f.tell()-4)
                    break
                name += chr(byte)
            self.files.append((name,offset))
    
    def extract(self):
        f = open(self.filename,"rb")
        for i in range(0, len(self.files)):
            if i+1 == len(self.files):
                length = self.filesize - int(self.files[i][1])
            else:
                length = int(self.files[i+1][1]) - int(self.files[i][1])
            f.seek(self.files[i][1])
            fdata = f.read(length)
            f2 = open("output/" + self.files[i][0],"w")
            self.logger.debug(self.filename + " " + self.files[i][0] + " (" + str(self.files[i][1]) + "-" + str(self.files[i][1]+length) + ")") 
            f2.write(fdata)
            f2.close() 
        f.close()
