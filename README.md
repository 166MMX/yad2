## yad2 (Yet Another Dune 2)

The goal here is to play with python, and specifically proper testing in python. I'm (probably) not going to implement anything complete, like a working game engine. Most likely it will end up being just a bunch of PAK file extractors and such. 

For a real Dune 2 experience (more or *less* true to the original, and/or abandoned) see them projects
* Dune Legacy, C++, http://sourceforge.net/projects/dunelegacy/develop
* OpenDUNE, C, https://github.com/OpenDUNE/OpenDUNE
* Dune Dynasty, C, http://sourceforge.net/p/dunedynasty/dunedynasty/ci/master/tree/
* OpenRA, https://github.com/OpenRA/OpenRA
* Dune 2 The Maker, http://dune2themaker.fundynamic.com/

### Usage

#### Setup

```bash
virtualenv .
source bin/activate
pip install -r requirements.txt
```

#### Engine

Obtain a copy of _Dune2.exe_ (apparently it was never officialy freed, so I'm not including it here), and run
```bash
./unpack.sh
```

Launch simplistic game window / engine
```
./run.py --config config.ini
```

#### Extractors (aka Dune 2 file converters)
Files are extracted to _tmp/_ in PNG format
```
./main.py --type pak --file all # packages
./main.py --type pal --file all # palettes
```
```
./main.py --type cps --file all # splash screens
./main.py --type wsa --file all # animations
./main.py --type shp --file all # shapes
./main.py --type icn --file all # map sprites
```

### Dependencies
* pil and pyx - image manipulation
* pyglet - for display handling, events, etc.
