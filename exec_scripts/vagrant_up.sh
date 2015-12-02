#!/usr/bin/env bash

PROJECT_PATH=/root/hubops
DATAPATH=$PROJECT_PATH/data/

function init_check {
    if [ -f $DATAPATH/Vagrantfile ]
    then
        exit 0
    else
        if cd $DATAPATH && vagrant init > /dev/null
            then exit 1
        fi
    fi
}

function box_pull {
    add_output=$(vagrant box add $1 --machine-readable --provider $2)
    exit_code=$?
    if echo $add_output | grep BoxAddShortNotFound > /dev/null
    then
        exit 1      # Box not found remotely
    elif echo $add_output | grep UIExpectsTTY > /dev/null
    then
        exit 2      # TTY required
    elif echo $add_output | grep BoxAlreadyExists > /dev/null
    then
        exit 3     # Box already exists
    elif echo $add_output | grep BoxAddNoMatchingProvider > /dev/null
    then
        exit 4      # Box does not support the specified provider
    elif [ $exit_code = 0 ]
    then
        exit 0      # Box has been added
    else
        exit 404
    fi
}

case $1 in
    c_init) init_check ;;
    box_pull) box_pull $2 $3 ;;
esac