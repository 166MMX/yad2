## yad2 (Yet Another Dune 2)

[![Build Status](https://secure.travis-ci.org/odcinek/yad2.png?branch=master)](http://travis-ci.org/odcinek/yad2)

If you never heard about classic Westwood RTS Dune 2, see overly detailed description at http://dune.wikia.com/wiki/Dune_II_(video_game).

The initial goal here was to play with python - proper testing, good practices, structuring codebase, etc. I'm (probably) not going to implement anything complete, like a working game engine. Most likely it will end up being just a bunch of PAK file extractors and such. 

For a complete Dune 2 experience (more or less true to the original) see them projects
* OpenDUNE, C, https://github.com/OpenDUNE/OpenDUNE
* OpenRA, C#, https://github.com/OpenRA/OpenRA
* Dune 2 The Maker, Java/C++, https://github.com/stefanhendriks/Dune-II---The-Maker
* Dune Legacy, C++, http://sourceforge.net/apps/mediawiki/dunelegacy/
* Dune Dynasty, C, http://dunedynasty.sourceforge.net/

or just use the original 1992 binary with DOSBox http://www.dosbox.com/wiki/GAMES:Dune_2

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
./yad2.py --config config.ini
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

## Thanks
Most of the extractors format code is based on work done by amazing peoples who reverse engineered and documented original Dune 2 binary / file formats.
Here are resources I've been using while implementing yad2.
* https://github.com/ultraq/redhorizon/ by @ultraq
* https://github.com/OpenDUNE/OpenDUNE by @OpenDUNE team
* http://dune2.ben.savoch.net/ by Ben Owen
* http://vladan.bato.net/cnc/ccfiles4.txt by Vladan Bato 
