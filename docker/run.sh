#!/usr/bin/env bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
IMAGE_TAG=rob530_carla:latest
CONTAINER_NAME=rob530_carla

capabilities_str=\""capabilities=compute,utility,graphics,display\""


DOCKER_OPTIONS=""
DOCKER_OPTIONS+="-it "
DOCKER_OPTIONS+="-e DISPLAY=$DISPLAY "
DOCKER_OPTIONS+="--device /dev/snd "
DOCKER_OPTIONS+="--device /dev/dri "
DOCKER_OPTIONS+="-v /tmp/.X11-unix:/tmp/.X11-unix "
DOCKER_OPTIONS+="-v /usr/share/vulkan/icd.d:/usr/share/vulkan/icd.d "
DOCKER_OPTIONS+="-v $SCRIPT_DIR/../:/home/$(whoami)/src/ "
DOCKER_OPTIONS+="-v $HOME/.Xauthority:/home/$(whoami)/.Xauthority "
DOCKER_OPTIONS+="-v /etc/group:/etc/group:ro "
# DOCKER_OPTIONS+="-v /mnt/:/mnt/hostmnt "
DOCKER_OPTIONS+="--name $CONTAINER_NAME "
DOCKER_OPTIONS+="--privileged "
DOCKER_OPTIONS+="--gpus all "
DOCKER_OPTIONS+="-e NVIDIA_DRIVER_CAPABILITIES=video,compute,utility,graphics,display "
DOCKER_OPTIONS+="--net=rob530-net "
DOCKER_OPTIONS+="--runtime=nvidia "
DOCKER_OPTIONS+="-e SDL_VIDEODRIVER=x11 "
DOCKER_OPTIONS+="-u $(id -u):$(id -g) "
DOCKER_OPTIONS+="--shm-size 32G "
DOCKER_OPTIONS+="--group-add $(id -g) "

for cam in /dev/video*; do
  DOCKER_OPTIONS+="--device=${cam} "
done

echo $CONTAINER_NAME

xhost +

if [ ${1:-""} == "restart" ]; then 
  echo "Restarting Container"
  docker rm -f $CONTAINER_NAME
  
  docker run $DOCKER_OPTIONS $IMAGE_TAG /bin/bash
# https://stackoverflow.com/questions/38576337/how-to-execute-a-bash-command-only-if-a-docker-container-with-a-given-name-does
elif [ ! "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then # If container isn't running
    
    # If it exists, but needs to be started
    if [  "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then

          echo "Resuming Container"
          docker start $CONTAINER_NAME
          docker exec -it $CONTAINER_NAME /entrypoint.sh
    else
      echo "Running Container"
      docker run $DOCKER_OPTIONS $IMAGE_TAG
    fi
else
  echo "Attaching to existing container"
  docker exec -it $CONTAINER_NAME /entrypoint.sh
fi
xhost -