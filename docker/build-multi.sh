#!/bin/sh

TAG=latest
if [ -n "$1" ]; then
    TAG=$1
fi

docker buildx build --platform linux/amd64,linux/arm64 -t gh0st42/coreemu-lab:$TAG --push .
