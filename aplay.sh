#!/bin/bash

main(){
    if pgrep -f "aplay" ;
    then
       pkill -f "aplay" && echo "Play stopped"
    fi
}

main "$@"


