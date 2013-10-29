#!/usr/bin/env python
import struct
import os
import io
import sys
import traceback
import logging
from yad2.utils.bytebuffer import ByteBuffer


def xors(s1, s2):
    bd = bytearray()
    for a, b in zip(bytearray(s1), bytearray(s2)):
        bd.append(int(a) ^ int(b))
    return bytes(bd)


class Format40:

    def __init__(self, base, st):
        self.logger = logging.getLogger('root')
        self.st = st
        self.base = base

    def decode(self):
        source = ByteBuffer(self.st)
        base = ByteBuffer(self.base)
        destination = ByteBuffer("")
        self.logger.debug("in " + str(source.length()))
        count = 0
        cmds = 0
        while 1:
            try:
                cmds += 1
                cmd = struct.unpack('B', source.get())[0]

                # b7 = 0
                if (cmd & 0x80) == 0:
                    # print str(cmds) + " " + "{0:08b}".format(cmd)

                    # cmd #1 - small xors base with value
                    if cmd == 0:
                        count = struct.unpack('B', source.get())[0] & 0xff
                        fill = source.get()
                        while count > 0:
                            count -= 1
                            destination.put(xors(base.get(), fill))

                    # cmd #2 - small xors source with base for count
                    else:
                        count = cmd
                        while count > 0:
                            count -= 1
                            destination.put(xors(source.get(), base.get()))
                # b7 = 1
                else:
                    count = cmd & 0x7f

                    # b6-0 = 0
                    if count == 0:
                        count = struct.unpack('H', source.getShort())[0] & 0xffff
                        cmd = count >> 8

                        # b7 of next byte = 0
                        if (cmd & 0x80) == 0:

                            # Finished decoding
                            if count == 0:
                                break

                            # cmd #3 - large copy base to dest for count
                            while count > 0:
                                count -= 1
                                destination.put(base.get())

                        # b7 of next byte = 1
                        else:
                            count &= 0x3fff

                           # cmd #4 - large xors source with base for count
                            if (cmd & 0x40) == 0:
                                while count > 0:
                                    count -= 1
                                    destination.put(xors(source.get(), base.get()))

                            # cmd #5 - large xors base with value
                            else:
                                fill = source.get()
                                while count > 0:
                                    count -= 1
                                    destination.put(xors(base.get(), fill))

                    # b6-0 != 0
                    else:
                        # cmd #6 - small copy base to dest for count
                        while count > 0:
                            count -= 1
                            destination.put(base.get())
            except Exception:
                print "FORMAT40 Exception"
                print traceback.format_exc()
                break
        points = destination.readall()
        self.logger.debug("in cmds " + str(cmds))
        self.logger.debug("in reads " + str(source.counter))
        self.logger.debug("out " + str(len(points)))
        return points
