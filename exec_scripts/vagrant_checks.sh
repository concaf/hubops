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

case $1 in
    c_init) init_check
esac