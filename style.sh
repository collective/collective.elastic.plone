#!/bin/bash
cd src
isort -y
black .
cd ..
./bin/code-analysis

