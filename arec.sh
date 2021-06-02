#!/bin/bash
# Author: Serg Kolo
# Date: Dec 1, 2016
# Purpose: simple script for recording audio with arecord
# Written for: https://askubuntu.com/q/855893/295286

filename=$1

record_audio()
{
    # Set up some variables to control arecord here
    # Please remember to quote the variables
    # and pay attention to slashes in file paths



    # This part will initiate recording of timestamped
    # please see arecord's man page for other options
    echo "Recording started"
    #exec arecord -t "$filetype" "$directory""$filename"."$filetype"

    exec arecord --format=S16_LE --rate=16000 --file-type=wav "$filename" &
}

main(){
    if pgrep -f "arecord" ;
    then
       pkill -f "arecord" && echo "Recording stopped"
    else
       record_audio
    fi
}

main "$@"


