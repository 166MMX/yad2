import random
import struct
import os
import logging
from array import array
import Image
import io
from pal import Pal
from yad2.utils import Sprite

group_names = ["ICM_ICONGROUP_ROCK_CRATERS",
               "ICM_ICONGROUP_SAND_CRATERS",
               "ICM_ICONGROUP_FLY_MACHINES_CRASH",
               "ICM_ICONGROUP_SAND_DEAD_BODIES",
               "ICM_ICONGROUP_SAND_TRACKS",
               "ICM_ICONGROUP_WALLS",
               "ICM_ICONGROUP_FOG_OF_WAR",
               "ICM_ICONGROUP_CONCRETE_SLAB",
               "ICM_ICONGROUP_LANDSCAPE",
               "ICM_ICONGROUP_SPICE_BLOOM",
               "ICM_ICONGROUP_HOUSE_PALACE",
               "ICM_ICONGROUP_LIGHT_VEHICLE_FACTORY",
               "ICM_ICONGROUP_HEAVY_VEHICLE_FACTORY",
               "ICM_ICONGROUP_HI_TECH_FACTORY",
               "ICM_ICONGROUP_IX_RESEARCH",
               "ICM_ICONGROUP_WOR_TROOPER_FACILITY",
               "ICM_ICONGROUP_CONSTRUCTION_YARD",
               "ICM_ICONGROUP_INFANTRY_BARRACKS",
               "ICM_ICONGROUP_WINDTRAP_POWER",
               "ICM_ICONGROUP_STARPORT_FACILITY",
               "ICM_ICONGROUP_SPICE_REFINERY",
               "ICM_ICONGROUP_VEHICLE_REPAIR_CENTRE",
               "ICM_ICONGROUP_BASE_DEFENSE_TURRET",
               "ICM_ICONGROUP_BASE_ROCKET_TURRET",
               "ICM_ICONGROUP_SPICE_STORAGE_SILO",
               "ICM_ICONGROUP_RADAR_OUTPOST",
               "ICM_ICONGROUP_EOF"]


class Icn:

    class Map:

        def __init__(self, filename):
            self.logger = logging.getLogger('root')
            f = open(filename, "rb")
            self.stream = io.BytesIO(f.read())
            self.length = len(self.stream.read())
            self.stream.seek(0)
            f.close()

        def read(self):
            out = []
            ngroups = struct.unpack('H', self.stream.read(2))[0]
            group_indexes = []
            for _ in xrange(ngroups):
                group_indexes.append(
                    struct.unpack('H', self.stream.read(2))[0] * 2)

            group_indexes[len(group_indexes) - 1] = self.length
            groups = []
            count = 0
            for i in xrange(len(group_indexes) - 1):
                self.stream.seek(group_indexes[i])
                size = group_indexes[i + 1] - group_indexes[i]
                self.logger.debug(
                    "group %d start %d end %d size %d" %
                    (i + 1, group_indexes[i], group_indexes[i + 1], size))
                g = []
                try:
                    for s in xrange(size / 2):
                        g.append(struct.unpack('H', self.stream.read(2))[0])
                except:
                    pass
                count += len(g)
                groups.append(g)

            return groups

    class Index:

        def __init__(self, filename):
            self.logger = logging.getLogger('root')
            with open(filename, "rb") as f:
                self.stream = io.BytesIO(f.read())
                self.filesize = len(self.stream.read())
                self.stream.seek(0)
            self.chf = Icn.Index.ChunkFile(self.stream)

        def sset(self):
            return Icn.Index.Chunk(self.chf, 'SSET')

        def rtbl(self):
            rtbl = Icn.Index.Chunk(self.chf, 'RTBL')
            self.logger.debug("rtbl %d" % len(rtbl.readall()))
            return io.BytesIO(rtbl.readall())

        def rpal(self):
            rpal = Icn.Index.Chunk(self.chf, 'RPAL')
            self.logger.debug("rpal %d" % len(rpal.readall()))
            return io.BytesIO(rpal.readall())

        class ChunkFile:

            def __init__(self, stream):
                self.stream = stream
                self.length = len(self.stream.read())
                self.stream.seek(0)

            def read(self, num):
                return self.stream.read(num)

            def tell(self):
                return self.stream.tell()

            def seek(self, pos):
                self.stream.seek(pos)

        class Chunk:

            def __init__(self, chunkfile, stx):
                self.chunkfile = chunkfile
                self.stx = stx
                self.token = self._tokenize(self.stx)
                self.size = self._read_size()

            def _tokenize(self, stx):
                st = array('c', stx[::-1])
                return (
                    Icn.Index.Util.reverse_bytes(
                        ord(st[0]),
                        ord(st[1]),
                        ord(st[2]),
                        ord(st[3]))
                )

            def _rewind_to_chunk(self):
                for offset in xrange(self.chunkfile.length):
                    try:
                        self.chunkfile.seek(offset)
                        if struct.unpack('i', self.chunkfile.read(4))[0] == self.token:
                            return self.chunkfile.tell()
                    except:
                        return 0
                return 0

            def _read_size(self):
                self.chunkfile.seek(self._rewind_to_chunk())
                bytes = []
                for _ in xrange(4):
                    bytes.append(struct.unpack('B', self.chunkfile.read(1))[0])
                return Icn.Index.Util.reverse_bytes(*bytes)

            def location(self):  # data location
                return self._rewind_to_chunk() + 4

            def readall(self):
                cur = self.chunkfile.tell()
                self.chunkfile.seek(self.location())
                r = self.chunkfile.read(self.size)
                self.chunkfile.seek(cur)
                return r

            def seek(self, pos):
                self.chunkfile.seek(pos)

            def read(self, count):
                return self.chunkfile.read(count)

        class Util:

            @staticmethod
            def reverse_bytes(*ar):
                return ar[0] << 24 | ar[1] << 16 | ar[2] << 8 | ar[3]

            @staticmethod
            def reverse_bytes2(*ar):
                return ar[0] | ar[1] << 8 | ar[2] << 16 | ar[3] << 24

            @staticmethod
            def parse(st):
                stream = io.BytesIO(st)
                tp = struct.unpack('H', stream.read(2))[0]
                size = struct.unpack('I', stream.read(4))[0]
                skip = struct.unpack('H', stream.read(2))[0]
                stream.seek(stream.tell() + skip)
                return stream.read(size)

    def __init__(self, filename):
        self.logger = logging.getLogger('root')
        self.groups = Icn.Map("output/ICON.MAP").read()
        self.sset = Icn.Index("output/ICON.ICN").sset()
        self.rtbl = Icn.Index("output/ICON.ICN").rtbl()
        self.rpal = Icn.Index("output/ICON.ICN").rpal()
        self.stream = io.BytesIO(Icn.Index.Util.parse(self.sset.readall()))
        self.length = len(self.stream.read())
        self.stream.seek(0)
        self.width = 8
        self.height = 16

    def extract(self):
        images = []
        for gid, group in enumerate(self.groups):
            images.extend(self.write_group(gid))
        return images

    def write_group(self, gid):
        houseID = 2

        group = self.groups[gid]
        self.logger.debug("%0.02d, %s, len %d, data %s" % (gid + 1, group_names[gid], len(group), str(group)))

        images = []
        for i, spriteID in enumerate(group):
            self.stream.seek(spriteID * self.width * self.height)

            points = []
            for o in xrange(self.width * self.height):
                points.append(struct.unpack('B', self.stream.read(1))[0])

            # read local palette
            self.rtbl.seek(spriteID)
            self.rpal.seek(struct.unpack('B', self.rtbl.read(1))[0] << 4)
            color_filter = []
            for _ in range(0, 16):
                color = struct.unpack('B', self.rpal.read(1))[0]
                if color >= 0x90 and color <= 0x96:
                    color += houseID << 4
                color_filter.append(color)

            self.logger.debug("spriteID %d, color_filter %s" % (spriteID, str(color_filter)))

            colorized_points = [0 for x in xrange(self.width * self.height)]
            j = 0
            while j < self.width * self.height - 1:
                colorized_points[j] = color_filter[points[j] >> 4]
                colorized_points[j + 1] = color_filter[points[j] & 0xF]
                j += 2

            image = Sprite(self.width, self.height)
            for index, pixel in enumerate(colorized_points):
                image.putpixel(index % self.width, index / self.width, pixel)

            if self.width != self.height:
                image.stretch(max(self.width, self.height))

            images.append(("%s/%s" % (group_names[gid], i), image))

        return images
