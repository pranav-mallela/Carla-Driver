docker build -t carla:latest -f Dockerfile .

#!/usr/bin/env bash


SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

IMAGE_TAG=rob530_carla:latest

DOCKER_OPTIONS=""
DOCKER_OPTIONS+="-t $IMAGE_TAG "
DOCKER_OPTIONS+="-f $SCRIPT_DIR/container.Dockerfile "
DOCKER_OPTIONS+="--build-arg USER_ID=$(id -u) "
DOCKER_OPTIONS+="--build-arg USER_NAME=$(whoami) "
# DOCKER_OPTIONS+="--progress=plain "

DOCKER_CMD="docker build $DOCKER_OPTIONS $SCRIPT_DIR"
echo $DOCKER_CMD
exec $DOCKER_CMD

rm $SCRIPT_DIR/tmp/ -rf