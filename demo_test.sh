#!/bin/bash

#. bin/activate

(cd demos;
 for demo in `ls *dm_73`; do
     timeout -s INT 10 qldemosummary.py $demo
     case $? in
	 124)
	     echo "${demo}: TIMEOUT"
	     ;;
	 0)
	     mv $demo pass/
	     ;;
	 *)
	     echo "${demo}: FAIL"
	     ;;
     esac
 done
)
