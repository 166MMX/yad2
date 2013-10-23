#!/usr/bin/env python
import struct
import os
import io
import sys
import traceback
import logging

from bytebuffer import ByteBuffer

#http://eob.wikispaces.com/Format+80
#https://github.com/ultraq/redhorizon/blob/3661d8fc36c37a6b97ee4754dc19e0534291d46d/Projects/Red%20Horizon%20-%20Filetypes/Java/redhorizon/utilities/codecs/Format80.java

class Format80:

    def __init__(self, st):
        self.logger = logging.getLogger('root')
        self.st = st

    def decode(self):
        source = ByteBuffer(self.st)
        destination = ByteBuffer("")
        self.logger.debug("in "+str(source.length()))
        copypos = 0
        count = 0 
        cmds=0
        while 1:
            try:
                cmds+=1
                cmd = struct.unpack('B', source.get())[0]
                
                if ( cmd & 0x80 ) == 0: # b7 = 0
                    #command 1
                    count = (cmd >> 4) + 3;
                    copyposa = (((cmd & 0x0f) << 8) | (struct.unpack('B', source.get())[0] & 0xff))
                    copypos = destination.tell() - copyposa
                    self.logger.debug('(' + "{0:08b}".format(cmd) + ',1,'+str(count) + ","+str(copypos) + ")")
                    while count > 0:
                        count-=1
                        destination.put(destination.get(copypos))
                        copypos+=1
                else: # b7 = 1
                    count = cmd & 0x3f
                    if ( cmd & 0x40 ) == 0: # b6 = 0
                        if count == 0: # finished
                            break
                        #command 2
                        self.logger.debug('(' + "{0:08b}".format(cmd) + ',2,'+str(count) + ")")
                        while count > 0:
                            count-=1
                            destination.put(source.get())
                    else: # b6 = 1
                        if count < 0x3e:
                            # command 3
                            count += 3;
                            copypos = struct.unpack('H', source.getShort())[0] & 0xffff;
                            self.logger.debug('(' + "{0:08b}".format(cmd) + ',3,'+str(count) + ")")
                            while count > 0:
                                count-=1
                                destination.put(destination.get(copypos))
                                copypos+=1
                        elif count == 0x3e:
                            # command 4
                            count = struct.unpack('H', source.getShort())[0] & 0xffff;
                            fill = source.get();
                            self.logger.debug('(' + "{0:08b}".format(cmd) + ',4,'+str(count) + ")")
                            while count > 0:
                                destination.put(fill)
                                count-=1
                        else:
                            # command 5
                            count = struct.unpack('H', source.getShort())[0] & 0xffff;
                            copypos = struct.unpack('H', source.getShort())[0] & 0xffff;
                            self.logger.debug('(' + "{0:08b}".format(cmd) + ',5,'+str(count) + ")")
                            while count > 0:
                                destination.put(destination.get(copypos))
                                count-=1
                                copypos+=1
            except Exception:
                print "FORMAT80 Exception"
                print traceback.format_exc()
                break
        points = destination.readall()
        self.logger.debug("in cmds "+str(cmds))
        self.logger.debug("in reads "+str(source.counter))
        self.logger.debug("out "+str(len(points)))
        return points
