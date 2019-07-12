#!/bin/bash

CHALLENGE=$1
IMAGE_NAME=$2

export SSH_STEPS=$(cat common/ssh_steps.txt) 
cat $CHALLENGE/Dockerfile | envsubst | docker build -t $IMAGE_NAME -f - .
