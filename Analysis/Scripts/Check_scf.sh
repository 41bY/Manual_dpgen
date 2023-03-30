#!/bin/bash

for dir in $1
do 

sys=$(basename $dir)

found=$(grep '!' $dir/${dir}.pwo | wc -l)

if [ "$found" == "0" ]
then
echo $dir
fi

done
