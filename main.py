#!/usr/bin/env python
import glob
import os
from yad2 import *
import argparse
import logging
from yad2 import Sprite

parser = argparse.ArgumentParser(description='Dune 2')
parser.add_argument('--type', required=True, help="shp, pak, wsa, cps, icn")
parser.add_argument('--file', required=True, help="'all' or filename")
parser.add_argument('--debug', dest='debug', action='store_true')
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

if args.file == "all":
    files = glob.glob("output/*." + args.type.upper()) + glob.glob("assets/*." + args.type.upper())
else:
    files = [args.file]

for file in files:
    logger.info(file)
    if args.type == 'pak':
        p = Pak(file)
        p.extract()
    elif args.type == 'shp' or args.type == 'cps' or args.type == 'wsa' or args.type == 'icn':
        obj = args.type.capitalize()
        for name, sprite in globals()[obj](file).extract():
            sprite.zoom()
            sprite.brigthness()
            dir = os.path.splitext(os.path.basename(file))[0].lower()
            sprite.write(dir="%s/%s" % (args.type, dir), outname=name)
