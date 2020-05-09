#!/bin/sh
export HOST_PORT="8000"
export REPO=socnet
if [ $1 ]
then
    HOST_PORT=$1
fi

echo "Going to remove any lingering $REPO-dev container."
docker rm $REPO-dev 2> /dev/null || true
echo "Now running docker to spin up the container."
docker run -it -p $HOST_PORT:8000 -v $PWD:/home/$REPO --rm gcallah/$REPO-dev bash
