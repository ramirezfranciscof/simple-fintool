#!/bin/zsh
################################################################################
# Logs into the container.
#
# `-it`
#     runs the container in interactive mode
#
################################################################################
FULLIMAGE_NAME="workimg-fintool:v0.1"
CONTAINER_NAME="workenv-fintool"

docker exec -it ${CONTAINER_NAME} bash #/bin/sh
################################################################################
