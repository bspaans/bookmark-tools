#!/bin/bash

function cdbm() {
    if [ -n "$1" ]; then
        if [ `expr index "$1" -` == 1 ]; then
            bm "$@"
        else
            cd "`bm $1`";
            echo "`bm $1`"
        fi
    else
        bm
    fi
}

