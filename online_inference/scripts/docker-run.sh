#! /bin/bash

docker run --env-file env/dev.env -p 5005:5000 sudotouchwoman/wbcd-online-inference:v1
