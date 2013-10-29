import random
import logging
import copy


class Map:

    def __init__(self, seed=392):
        self.logger = logging.getLogger('root')
        random.seed(seed)
        fmap = [0 for x in xrange(64 * 64)]
        memory = []
        around = [0, -1, 1, -16, 16, -17, 17, -15, 15, -2, 2, -32, 32, -4, 4, -64, 64, -30, 30, -34, 34]
        offsetTable = [
            [[0, 0, 4, 0], [4, 0, 4, 4], [0, 0, 0, 4], [0, 4, 4, 4], [0, 0, 0, 2], [0, 2, 0, 4], [0, 0, 2, 0], [2, 0, 4, 0], [4, 0, 4, 2], [4, 2, 4, 4], [0, 4, 2, 4],
             [2, 4, 4, 4], [0, 0, 4, 4], [2, 0, 2, 2], [0, 0, 2, 2], [4, 0, 2, 2], [0, 2, 2, 2], [2, 2, 4, 2], [2, 2, 0, 4], [2, 2, 4, 4], [2, 2, 2, 4]],
            [[0, 0, 4, 0], [4, 0, 4, 4], [0, 0, 0, 4], [0, 4, 4, 4], [0, 0, 0, 2], [0, 2, 0, 4], [0, 0, 2, 0], [2, 0, 4, 0], [4, 0, 4, 2], [4, 2, 4, 4], [0, 4, 2, 4],
             [2, 4, 4, 4], [4, 0, 0, 4], [2, 0, 2, 2], [0, 0, 2, 2], [4, 0, 2, 2], [0, 2, 2, 2], [2, 2, 4, 2], [2, 2, 0, 4], [2, 2, 4, 4], [2, 2, 2, 4]]]

        # Place random data on a 4x4 grid.
        for x in xrange(16):
            for y in xrange(17):
                v = self.randint() & 0xF
                if v > 0xA:
                    v = 0xA
                memory.append(v)

        i = (self.randint() & 0xF) + 1
        while i != 0:
            i -= 1
            base = self.randint()
            for j in range(0, len(around)):
                index = min(max(0, base + around[j]), 271)
                memory[index] = (memory[index] + (self.randint() & 0xF)) & 0xF

        i = (self.randint() & 0x3) + 1
        while i != 0:
            i -= 1
            base = self.randint()
            for j in range(0, len(around)):
                index = min(max(0, base + around[j]), 271)
                memory[index] = self.randint() & 0x3

        for j in xrange(16):
            for i in xrange(16):
                c = self.packxy(i * 4, j * 4)
                fmap[c] = memory[j * 16 + i]

        # Average around the 4x4 grid.
        for j in xrange(16):
            for i in xrange(16):
                for k in xrange(21):
                    offsets = offsetTable[(i + 1) % 2][k]
                    packed1 = self.packxy(i * 4 + offsets[0], j * 4 + offsets[1])
                    packed2 = self.packxy(i * 4 + offsets[2], j * 4 + offsets[3])
                    packed = (packed1 + packed2) / 2

                    packed1 = self.packxy((i * 4 + offsets[0]) & 0x3F, j * 4 + offsets[1])
                    packed2 = self.packxy((i * 4 + offsets[2]) & 0x3F, j * 4 + offsets[3])
                    if packed >= 4096 or packed1 >= 4096 or packed2 >= 4096:
                        # print packed1, packed2, packed
                        break

                    fmap[packed] = (fmap[packed1] + fmap[packed2] + 1) / 2

        currentRow = [0 for x in xrange(64)]

        self._debug(fmap)

        # Average each tile with its neighbours.
        for j in xrange(64):
            previousRow = copy.deepcopy(currentRow)
            for i in xrange(64):
                currentRow[i] = fmap[j * 64 + i]

            neighbours = [0 for x in xrange(9)]
            for i in xrange(64):
                total = 0
                neighbours[0] = currentRow[i] if (i == 0 or j == 0) else previousRow[i - 1]
                neighbours[1] = currentRow[i] if (j == 0) else previousRow[i]
                neighbours[2] = currentRow[i] if (i == 63 or j == 0) else previousRow[i + 1]
                neighbours[3] = currentRow[i] if (i == 0) else currentRow[i - 1]
                neighbours[4] = currentRow[i]
                neighbours[5] = currentRow[i] if (i == 63) else currentRow[i + 1]
                neighbours[6] = currentRow[i] if (i == 0 or j == 63) else fmap[j * 64 + i + 63]
                neighbours[7] = currentRow[i] if (j == 63) else fmap[j * 64 + i + 64]
                neighbours[8] = currentRow[i] if (i == 63 or j == 63) else fmap[j * 64 + i + 65]

                for k in xrange(9):
                    total += neighbours[k]
                fmap[j * 64 + i] = total / 9

        # Filter each tile to determine its final type.
        spriteID1 = self.randint() & 0xF
        if (spriteID1 < 0x8):
            spriteID1 = 0x8
        if (spriteID1 > 0xC):
            spriteID1 = 0xC

        spriteID2 = (self.randint() & 0x3) - 1
        if (spriteID2 > spriteID1 - 3):
            spriteID2 = spriteID1 - 3

        LST_NORMAL_SAND = 0
        LST_PARTIAL_ROCK = 1
        LST_ENTIRELY_DUNE = 2
        LST_PARTIAL_DUNE = 3
        LST_ENTIRELY_ROCK = 4
        LST_MOSTLY_ROCK = 5
        LST_ENTIRELY_MOUNTAIN = 6
        LST_PARTIAL_MOUNTAIN = 7
        LST_SPICE = 8
        LST_THICK_SPICE = 9

        for i in xrange(0, 4096):
            spriteID = fmap[i]

            if (spriteID > spriteID1 + 4):
                spriteID = LST_ENTIRELY_MOUNTAIN
            elif (spriteID >= spriteID1):
                spriteID = LST_ENTIRELY_ROCK
            elif (spriteID <= spriteID2):
                spriteID = LST_ENTIRELY_DUNE
            else:
                spriteID = LST_NORMAL_SAND

            fmap[i] = spriteID

        self._debug(fmap)

        # Make everything smoother and use the right sprite indexes.
        currentRow = [0 for x in xrange(64)]

        for j in xrange(64):
            previousRow = copy.deepcopy(currentRow)
            for i in xrange(64):
                currentRow[i] = fmap[j * 64 + i]

            for i in xrange(64):
                current = fmap[j * 64 + i]
                up = current if (j == 0) else previousRow[i]
                left = current if (i == 63) else currentRow[i + 1]
                down = current if (j == 63) else fmap[j * 64 + 64 + i]
                right = current if (i == 0) else currentRow[i - 1]
                spriteID = 0

                if (up == current):
                    spriteID |= 1
                if (left == current):
                    spriteID |= 2
                if (down == current):
                    spriteID |= 4
                if (right == current):
                    spriteID |= 8

                if current == LST_NORMAL_SAND:
                    spriteID = 0
                elif current == LST_ENTIRELY_ROCK:
                    if up == LST_ENTIRELY_MOUNTAIN:
                        spriteID |= 1
                    if left == LST_ENTIRELY_MOUNTAIN:
                        spriteID |= 2
                    if down == LST_ENTIRELY_MOUNTAIN:
                        spriteID |= 4
                    if right == LST_ENTIRELY_MOUNTAIN:
                        spriteID |= 8
                    spriteID += 1
                elif current == LST_ENTIRELY_DUNE:
                    spriteID += 17
                elif current == LST_ENTIRELY_MOUNTAIN:
                    spriteID += 33
                elif current == LST_SPICE:
                    if up == LST_THICK_SPICE:
                        spriteID |= 1
                    if left == LST_THICK_SPICE:
                        spriteID |= 2
                    if down == LST_THICK_SPICE:
                        spriteID |= 4
                    if right == LST_THICK_SPICE:
                        spriteID |= 8
                    spriteID += 49
                elif current == LST_THICK_SPICE:
                    spriteID += 65

                fmap[j * 64 + i] = spriteID

        self.fmap = fmap

    def _debug(self, m):
        self.logger.debug("+++")
        for y in xrange(64):
            row = ''
            for x in xrange(64):
                row += "{0:02d}".format(m[64 * y + x])
            self.logger.debug(row)

    def packxy(self, x, y):
        return (y << 6) | x

    def randint(self):
        return random.randint(0, 255)

    def read(self):
        return self.fmap
