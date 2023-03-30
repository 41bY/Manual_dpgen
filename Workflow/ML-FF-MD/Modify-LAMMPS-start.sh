#!/bin/bash

QEstep=$1
step=$2

cp $3 $4

sed -i "s/OUTPUT\/Step$QEstep/OUTPUT\/Step$step/" $4
sed -i "s/Step${QEstep}\/OUTPUT/Step${step}\/OUTPUT/" $4

#CreateRND="velocity 
#sed -i "/create/c$CreateRND" ./temp.in

read -ra arr1 <<< $(grep 'create' $4)
Temp="${arr1[3]}"
Seed="$RANDOM"

echo "$Temp"
echo "$Seed"

NewCreate="velocity init_vel create $Temp $Seed dist gaussian"
sed -i "/create/c$NewCreate" $4

LastRun=$(grep 'run' $4 | tail -n 1)
read -ra arr2 <<< $LastRun
OldTime=${arr2[1]}
#(( NewTime = $OldTime*$5 ))
NewTime=$( echo $OldTime*$5 | bc )
NewTime=${NewTime%.*}
echo $NewTime

NewTimeString="run $NewTime start 0"
sed -i "s/${LastRun}/${NewTimeString}/" $4
