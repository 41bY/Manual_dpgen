#!/bin/bash

TrainDir=../../Data/Training/Data_Train
ValidDir=../../Data/Training/Data_Valid

rm -r -f $TrainDir
rm -r -f $ValidDir

for dirname in ../../Data/Training/Data_NPY/*
do
BaseDir=$(basename $dirname)
mkdir -p $TrainDir/$BaseDir
mkdir -p $ValidDir/$BaseDir
cp -f $dirname/type.raw $TrainDir/$BaseDir/ 
cp -f $dirname/type.raw $ValidDir/$BaseDir/ 
cp -f $dirname/type_map.raw $TrainDir/$BaseDir/ 
cp -f $dirname/type_map.raw $ValidDir/$BaseDir/  

SubDirs=( $dirname/set* )

if [ "${#SubDirs[@]}" -gt "1" ]
then
ToValid=( "${SubDirs[@]: -1}" )
ToTrain=( "${SubDirs[@]:0:${#SubDirs[@]}-1}" )
else
ToValid=( "${SubDirs[@]}" )
ToTrain=( "${SubDirs[@]}" )
fi

for subdirname in "${ToTrain[@]}"
do
cp -r -f $subdirname  $TrainDir/$BaseDir/ 
done

for subdirname in "${ToValid[@]}"
do
cp -r -f $subdirname  $ValidDir/$BaseDir/ 
done

done
