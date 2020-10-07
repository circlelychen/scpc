#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cmd="docker run --rm -it -v $DIR:/scpc scpc:latest python crawl.py"
echo $cmd
eval $cmd
