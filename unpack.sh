#!/usr/bin/env bash
rm -rf output/* assets/* tmp/*
set -o verbose
mv Dune2.exe dune2.zip
unzip -u dune2.zip -d assets
for i in pak cps shp icn wsa; 
do
  echo $i; 
  ./main.py --type $i --file all
done
echo "OK"
