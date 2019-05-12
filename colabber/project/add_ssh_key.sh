#!/bin/sh

MY_SSH_KEY_FILE_PATH=$1
SSH_FOLDER="/root/.ssh/"
NEW_SSH_KEY_PATH=${SSH_FOLDER}/"id_rsa"
KNOWN_HOSTS_FILE_PATH=${SSH_FOLDER}/"known_hosts"

mkdir -p ${SSH_FOLDER}
touch ${NEW_SSH_KEY_PATH}
cat MY_SSH_KEY_FILE_PATH >> ${NEW_SSH_KEY_PATH}
chmod 600 ${NEW_SSH_KEY_PATH}
touch ${KNOWN_HOSTS_FILE_PATH}
ssh-keyscan github.com >> ${KNOWN_HOSTS_FILE_PATH}
