#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if test "$(uname)" = "Darwin"
then
    cmd="docker run --rm -it -v $DIR:/scpc scpc:latest python crawl.py"
else
    USER_ID=$(id -u)
    GROUP_ID=$(id -g)
    cmd="docker run --rm -it --user "$USER_ID:$GROUP_ID" -v $DIR:/scpc scpc:latest python crawl.py"
fi

echo $cmd
eval $cmd
