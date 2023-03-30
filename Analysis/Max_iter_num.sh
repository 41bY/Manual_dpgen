#!/bin/bash

raw_path="$1/*/"
path=${raw_path//\/\//\/}

n_ite=0
for dir in $raw_path
do

string=$(basename $dir)
token=${string//[0-9]/}

if [ "$token" == "Step" ]
then
num=${string//[!0-9]/}

if [ "$num" -ge "$n_ite" ]
then
n_ite=$num
fi

fi
done

echo $n_ite
