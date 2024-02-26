#!/bin/zsh
################################################################################
# Launches the container from the image.
################################################################################
FULLIMAGE_NAME="workimg-fintool:v0.1"
CONTAINER_NAME="workenv-fintool"

args=(

    -it
    # runs the container in interactive mode

    --rm
    # will delete the container after it is stopped

    -p 8888:8888 #-p 8000:8000
    # Publishes the ports so that it can be accessed by the host.
    # Order: <host_port>:<cont_port>

    -v $(pwd)/..:/root/app
    # Mounts the path of the host into the path in the container.
    # Note that in some OS, permissions are not adapted correctly.

)

docker run "${args[@]}" --name ${CONTAINER_NAME} ${FULLIMAGE_NAME}

################################################################################
