#!/usr/bin/env python
import os
import pyglet
import logging
import argparse
from pyglet.window import key
from pyglet import clock
import ConfigParser
from yad2 import * 

parser = argparse.ArgumentParser(description='Dune 2')
parser.add_argument('--config', required=True, help = "shp, pak, pal, wsa, cps, icn")
parser.add_argument('--debug', dest='debug',action='store_true')
parser.set_defaults(debug=False)
args = parser.parse_args()

formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(module)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('root')
logger.setLevel(logging.INFO)
if args.debug:
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

config = ConfigParser.ConfigParser()
config.read(args.config)

SIZE = config.getint('tile', 'size')
SPACE = config.getint('tile', 'space')
WIDTH = config.getint('window', 'width')
HEIGHT = config.getint('window', 'height')
SEED = config.getint('map', 'seed')

SCALE=SIZE/16.0
XTILES=int(WIDTH/SIZE)
YTILES=int(HEIGHT/SIZE)

class Viewport:

    def __init__(self, m, x=0, y=0):
        self.logger = logging.getLogger('root')
        self.x = x
        self.y = y
        self.w = XTILES
        self.h = YTILES
        self.source = m.read()

    def update(self, x, y):
        if self.x + x < 0: x = 0
        if self.x + XTILES + x > 64: x = 0
        if self.y + y < 0: y = 0
        if self.y + YTILES + y > 64: y = 0

        self.x += x
        self.y += y
        d = []
        for xx in xrange(64):
            g = []
            for yy in xrange(64):
                g.append(self.source[64*xx+yy])
            d.append(g)
        result = []
        for i in range(self.x, self.x + XTILES):
            g = []
            for j in xrange(self.y, self.y + YTILES):
                g.append(d[j][i])
            result.append(g)

        self.view = zip(*result)
        return self

    def points(self):
        y = 0
        for row in self.view:
            x=0 
            for value in row:
                yield x,y,value
                x+=1
            y+=1

class App:

    def __init__(self):
        self.logger = logging.getLogger('root')
        self.m = Map(SEED)
        self.x = 0
        self.y = 0
        self.viewport = Viewport(self.m, 0,0)

    def refresh(self, x=0, y=0):
        sprites = []

        for x,y,v in self.viewport.update(x,y).points():
            sprites.append(pyglet.sprite.Sprite(self.tiles[v],x=x*SIZE+x*SPACE, y=HEIGHT-(y*SIZE+y*SPACE+SIZE)))

        window.clear()
        for sprite in sprites:
            sprite.scale = SCALE
            sprite.draw()

    def load(self):
        pyglet.resource.path = ['tmp/icn/09_ICM_ICONGROUP_LANDSCAPE/']
        pyglet.resource.reindex()
        self.tiles = []
        for i in range (0,81):
            self.tiles.append(pyglet.resource.image("%d.png" % i))

class EventLoop(pyglet.app.EventLoop):

    def on_window_close(self, window):
        window.close()
        el.exit()

    def on_exit(self):
        window.close()
        el.exit()

    def on_enter(self):
        app.refresh(0,0)

class Window(pyglet.window.Window):

    def __init__(self, width, height):
        super(Window, self).__init__(vsync = True, width=width, height=height)
        #pyglet.clock.schedule_interval(self.update, 1.0/128.0)
        pyglet.clock.set_fps_limit(32)

    def update(self, dt):
        pass

    def on_draw(self):
        pass
#        pyglet.clock.tick() # Make sure you tick the clock!
#        pyglet.gl.glColor4f(1.0,0,0,1.0)
#        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ('v2i', (10, 15, 30, 35)))
#        fps.draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == key.LEFT:
            app.refresh(-1,0)
        elif symbol == key.RIGHT:
            app.refresh(1,0)
        elif symbol == key.UP:
            app.refresh(0,-1)
        elif symbol == key.DOWN:
            app.refresh(0,1)
        elif symbol == key.ESCAPE:
            window.close()
            el.exit()
    
#fps = pyglet.clock.ClockDisplay()
window = Window(WIDTH, HEIGHT)

app = App()
app.load()
el = EventLoop()
el.run()
