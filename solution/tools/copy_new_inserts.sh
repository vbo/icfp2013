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

    diff --unchanged-line-format= --old-line-format= --new-line-format='%L' $2 $1 2>/dev/null | tee >> $2 $TARGET_FILE

    head -n $(( `wc -l 2>/dev/null < $TARGET_FILE` - 1 )) $TARGET_FILE 1>/dev/null

    cp $TARGET_FILE ~/Dropbox/Icfp2013/problems_index/

    sleep $4

done

