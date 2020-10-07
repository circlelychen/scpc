#!/usr/bin/env bash

cmd="docker run --rm -it -v $(pwd)/crawl.py:/scpc/crawl.py scpc:latest python crawl.py"
echo $cmd
eval $cmd
