#!/bin/bash

/usr/bin/yes | pip uninstall PyBBIO 
rm -r build/ dist/
python setup.py install
