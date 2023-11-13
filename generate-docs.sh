#!/usr/bin/env bash

lib_version=$(python setup.py --version)
echo "Library Version: $lib_version"

echo "generating docs..."
pdoc -o docs/ -t ./doc/theme --footer-text "duit v$lib_version" --logo-link "https://github.com/cansik/duit/"  duit \!duit.vision

echo "copy additional content..."
mkdir docs/doc
cp -r doc/* docs/doc