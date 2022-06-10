#! /bin/bash

[ "$#" -eq 1 ] && TAG=$1 || TAG=v2
docker run --env-file env/dev.env -p 5005:5000 sudotouchwoman/wbcd-online-inference:$TAG
