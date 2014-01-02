#!/bin/bash

find . -type f -name "*~" -exec rm -f {} \; # remove gedit temp files
rm -rf datalanche.egg-info dist
python setup.py sdist upload
