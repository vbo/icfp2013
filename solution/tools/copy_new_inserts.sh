#!/bin/bash

FILE="$3`basename $1`"
TARGET_FILE=$FILE

NUM=1

TARGET_FILE="$FILE.part.$NUM"

while : ; do

    while : ; do
        [[ ! -f $TARGET_FILE ]] && break
        TARGET_FILE="$FILE.part.$NUM"
        ((NUM+=1))
    done

    comm -23 $1 $2 2>/dev/null | tee >> $2 $TARGET_FILE

    head -n $(( `wc -l < $TARGET_FILE` - 1 )) $TARGET_FILE

    cp $TARGET_FILE ~/Dropbox/Icfp2013/problems_index/

    sleep $4

done

