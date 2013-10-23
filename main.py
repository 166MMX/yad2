#!/usr/bin/env python
import glob
from yad2 import *
import argparse
import logging

parser = argparse.ArgumentParser(description='Dune 2')
parser.add_argument('--type', required=True, help = "shp, pak, pal, wsa, cps, icn")
parser.add_argument('--file', required=True, help = "'all' or filename")
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

def process(type, file):
    obj = type.capitalize()
    if file == "all":
        files = glob.glob("output/*." + type.upper()) + glob.glob("assets/*." + type.upper())
        for ff in files:
            logger.info(ff)
            p = globals()[obj](ff)
            p.extract()
    else:
        p = globals()[obj](args.file)
        p.extract()
    
if args.type == 'icn':
    i = Icn.Extractor()
    i.writeall()
else:
    process(args.type, args.file)
