#!/usr/bin/env bash
rm -rf output/*
rm assets/*
set -o verbose
mv Dune2.exe dune2.zip
unzip -u dune2.zip -d assets
rm assets/XTRE.PAK assets/ATRE.pak
./main.py --type pak --file all
for i in WSA SHP CPS WSA INI PCS VOC PAL; do echo $i; mkdir output/$i; mv output/*.$i output/$i; done
echo "OK"
