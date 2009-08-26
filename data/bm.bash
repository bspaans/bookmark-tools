#!/bin/sh

function cdbm() {
    if [ -n "$1" ]; then
        if [ `expr index "$1" -` -eq 1 ]; then
            bm "$@"
        else
            cd "`bm $1`";
        fi
    else
        bm
    fi
}

function bmcmd {
    # Helper function to extend common commands that take (arguments and) 
    # two filenames. Where the first file is the source and the second the 
    # target. This command treats the target as a bookmark.
    # This function can be partially applied to create cpbm, lnbm, etc.
    #
    # Parameters:
    #
    #       $1        -   The command
    #       $2..$n-2  -   Command arguments
    #       $n-1      -   The file name
    #       $n        -   Bookmark

    # Check for --help or -h parameter
    if [ -n $2 ]; then
        if [ "$2" = "--help" ] || [ "$2" = "-h" ]; then
            echo "$1bm - $1 extended with bookmark support (bmcmd)"
            echo "Copyright 2008, 2009, Bart Spaans"
            echo "Usage: $1bm [args] FILE BOOKMARK"
            echo 
            echo "Following is the help for $1"
            echo "-------------------------------------------------------------"
            $1 --help
            return 0 
        fi
    fi

    # Check number of parameters
    if [ $# -lt 3 ]; then
        if [ -n $1 ]; then
            echo "Usage: $1bm [args] file bookmark"
        else
            echo "Usage: bmcmd cmd [args] file bookmark"
        fi
        return 1
    fi



    CMD=$1
    FILE=""
    BOOKMARK=""
    ARGS=""

    # Find out which parts are arguments and which parts are 
    # files and bookmarks. 
    #warning Isn't there a nicer way to do this (splicing?)
    i=0
    for a in "$@";
    do
        if [ $i -gt 0 ]; then
            if [ $i -eq "$(expr $# - 1)" ]; then
                BOOKMARK=$a
            elif [ $i -eq "$(expr $# - 2)" ]; then
                FILE=$a
            else
                ARGS="$ARGS $a"
            fi
        fi
        i="$(expr $i + 1)"
    done

	BM="$(bm $BOOKMARK)"
	if [ $? -eq 0 ]; then
		$CMD $ARGS $FILE $BM
	else
		echo "Error: Unknown bookmark '$BOOKMARK'"
		return 1
	fi
}

alias cpbm="bmcmd cp"
alias lnbm="bmcmd ln"
alias scpbm="bmcmd scp"

# not so nice
alias lsbm="bmcmd ls \"\""
