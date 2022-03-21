#!/bin/sh


[ ! -d "goforban" ] && git clone https://github.com/gh0st42/goforban

cd goforban
#GOOS=linux GOARCH=arm64 go build
#GOOS=linux GOARCH=amd64 go build
GOOS=linux go build
file goforban
cd ..