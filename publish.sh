#!/bin/bash

rm -rf datalanche.egg-info dist
python setup.py sdist upload
