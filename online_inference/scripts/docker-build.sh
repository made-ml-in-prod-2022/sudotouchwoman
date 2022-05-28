#! /bin/bash

[ "$#" -eq 1 ] && TAG=$1 || TAG=v1
[ "$#" -eq 2 ] && NAME=$2 || NAME=sudotouchwoman/wbcd-online-inference
docker build -t $NAME:$TAG .
