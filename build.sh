#!/usr/bin/env bash

cmd="docker build --tag scpc:latest ."
echo $cmd
eval $cmd
