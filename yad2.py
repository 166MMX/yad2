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

TILE_SIZE = config.getint('tile', 'size')
TILE_SPACE = config.getint('tile', 'space')
WINDOW_WIDTH = config.getint('window', 'width')
WINDOW_HEIGHT = config.getint('window', 'height')
VIEWPORT_WIDTH = 300
VIEWPORT_HEIGHT = 200

SEED = config.getint('map', 'seed')

TILE_SCALE=TILE_SIZE/16.0
XTILES=int(VIEWPORT_WIDTH/TILE_SIZE)
YTILES=int(VIEWPORT_HEIGHT/TILE_SIZE)

pyglet.resource.path = ['tmp/']
pyglet.resource.reindex()

class Viewport:

    def __init__(self, m, x=0, y=0, posx=0, posy=0):
        self.logger = logging.getLogger('root')
        self.x = x
        self.y = y
        self.w = int(self.x/TILE_SIZE)
        self.h = int(self.y/TILE_SIZE)
        self.source = m.read()
        self.tiles = []
        for i in range (0,81):
            self.tiles.append(pyglet.resource.image("icn/icon/ICM_ICONGROUP_LANDSCAPE/%d.png" % i))

    def move(self, x, y):
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
        for i in range(self.w, self.w + XTILES):
            g = []
            for j in xrange(self.w, self.w + YTILES):
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

    def draw(self,xx,yy,x,y):
        sprites = []
        for x,y,v in self.move(x,y).points():
            sprites.append(pyglet.sprite.Sprite(self.tiles[v],x=x*TILE_SIZE+x*TILE_SPACE, y=VIEWPORT_HEIGHT-(y*TILE_SIZE+y*TILE_SPACE+TILE_SIZE)))
        for sprite in sprites:
            sprite.scale = TILE_SCALE
            sprite.draw()

class App:

    def __init__(self):
        self.logger = logging.getLogger('root')
        self.m = Map(SEED)
        self.x = 0
        self.y = 0
        self.viewport = Viewport(self.m, VIEWPORT_WIDTH, VIEWPORT_HEIGHT, 60, 80)
        self.interface = Interface()

    def refresh(self, x=0, y=0):
        window.clear()
        self.interface.draw(0,0)
        self.viewport.draw(60,60,x,y)

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
        #pyglet.clock.schedule_interval(self.move, 1.0/128.0)
        pyglet.clock.set_fps_limit(32)

    def move(self, dt):
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

class Interface:

    def __init__(self):
        pass

    def draw(self, x,y):
        iface = pyglet.resource.image("cps/screen/0.png")
        s=pyglet.sprite.Sprite(iface, x=0, y=0)
        s.scale = 3
        s.draw()

    
#fps = pyglet.clock.ClockDisplay()
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT)

app = App()
el = EventLoop()
el.run()
