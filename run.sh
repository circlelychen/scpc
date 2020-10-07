#!/usr/bin/env bash

cmd="docker run --rm -it -v $(pwd):/scpc scpc:latest python crawl.py"
echo $cmd
eval $cmd
