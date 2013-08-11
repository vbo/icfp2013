#!/bin/bash

FILE="$3`basename $1`"
TARGET_FILE=$FILE

NUM=1

while : ; do
    [[ ! -f $TARGET_FILE ]] && break
    TARGET_FILE="$FILE.$NUM"
    ((NUM+=1))
done

comm -23 $1 $2 2>/dev/null | head -n -1 | tee >> $2 $TARGET_FILE

