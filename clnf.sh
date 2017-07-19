#!/bin/bash
#if the program is run without parameter,
#it will get the current path
if [ -z "$1" ] ; then
    path=$(pwd)
else
    path=$1
fi

#get all the filename, and then clear all
#contents of them
for file in ${path}/*.log ; do
    echo > $file
    echo $file " has been set to null"
done
