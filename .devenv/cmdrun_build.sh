#!/bin/zsh
################################################################################
# Builds the image.
#
# `-f <path>`
#     specifies path for the dockerfile to use.
#
# `../.` (context)
#     so that it has access to the source files in parent dir.
#
################################################################################
FULLIMAGE_NAME="workimg-fintool:v0.1"
CONTAINER_NAME="workenv-fintool"

docker build -f ./Dockerfile -t ${FULLIMAGE_NAME} ../.
################################################################################
