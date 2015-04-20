#!/usr/bin/env bash

DATA_DIR="$HOME/.local/share"
SCRIPT_DIR=`dirname $0`
if [ $SCRIPT_DIR == '.' ]
    then
        SCRIPT_DIR=`pwd`
fi
cp -r $SCRIPT_DIR/share/acoustics $DATA_DIR/

