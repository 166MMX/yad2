## yad2 (Yet Another Dune 2)

The goal here is to play with python, and specifically proper testing in python. I'm not going to implement anything complete here. Most likely it will end up being just a bunch of PAK file parsers and such. 

For a real Dune 2 experience (more or *less* true to the original, and/or abandoned) see them projects
* Dune Legacy, C++, http://sourceforge.net/projects/dunelegacy/develop
* OpenDUNE, C, https://github.com/OpenDUNE/OpenDUNE
* Dune Dynasty, C, http://sourceforge.net/p/dunedynasty/dunedynasty/ci/master/tree/
* OpenRA, https://github.com/OpenRA/OpenRA
* Dune 2 The Maker, http://dune2themaker.fundynamic.com/

### Usage

```bash
virtualenv .
source bin/activate
pip install -r requirements.txt
```

```bash
./unpack.sh
```

#### Engine
```
./run.py --config config.ini
```

#### Extractors
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

