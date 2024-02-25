#!/bin/sh

BIGCOPY() {
    cat $1 > $2
    for i in $(seq 1 9); do
        cat $1 >> $2
    done
}


BIGCOPY example_base0.txt example_long1.txt
BIGCOPY example_long1.txt example_long2.txt
BIGCOPY example_long2.txt example_long3.txt
