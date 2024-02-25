#!/bin/zsh
################################################################################
# Copies github credentials inside running container so that it can be used.
################################################################################
FULLIMAGE_NAME="workimg-fintool:v0.1"
CONTAINER_NAME="workenv-fintool"

if [[ -z "${GITHUB_CREDENTIALS}" ]]; then
    echo "You do not have the env variable GITHUB_CREDENTIALS"
    echo "Define the variable with the path to git private key"
    exit 1
fi

docker exec -it ${CONTAINER_NAME} mkdir -p /root/.ssh
docker exec -it ${CONTAINER_NAME} bash -c "echo '# Github config' > /root/.ssh/config"
docker exec -it ${CONTAINER_NAME} bash -c "echo 'Host github.com' >> /root/.ssh/config"
docker exec -it ${CONTAINER_NAME} bash -c "echo '  IdentityFile /root/.ssh/id_rsa' >> /root/.ssh/config"

gitname="$(git config user.name)"
gitmail="$(git config user.email)"
git config --local user.name "$gitname"
git config --local user.email "$gitmail"
git config --local core.editor "vim"

docker cp ${GITHUB_CREDENTIALS} ${CONTAINER_NAME}:/root/.ssh/id_rsa

################################################################################
