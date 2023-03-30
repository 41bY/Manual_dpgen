#!/bin/bash

QEstep="1"
step="2"

cp $1 ./temp.in

sed -i "s/OUTPUT\/Step$QEstep/OUTPUT\/Step$step/" ./temp.in
sed -i "s/Step${QEstep}\/OUTPUT/Step${step}\/OUTPUT/" ./temp.in


#CreateRND="velocity 
#sed -i "/create/c$CreateRND" ./temp.in

read -ra arr1 <<< $(grep 'create' ./temp.in)
Temp="${arr1[3]}"
Seed="$RANDOM"

echo "$Temp"
echo "$Seed"

NewCreate="velocity init_vel create $Temp $Seed dist gaussian"
sed -i "/create/c$NewCreate/" ./temp.in

LastRun=$(grep 'run' ./temp.in | tail -n 1)
read -ra arr2 <<< $LastRun
OldTime=${arr2[1]}
(( NewTime = $OldTime*2 ))
echo $NewTime

NewTimeString="run $NewTime start 0"
sed -i "s/${LastRun}/${NewTimeString}/" ./temp.in
