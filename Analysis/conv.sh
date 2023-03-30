#! /bin/bash

echo "--- PWO2XYZ ---"
echo "Usage: ./script trajectory.pwo"
echo ""

filename=$(echo $1 | sed -r 's/.{4}$//')

# Generating an xyz file containing the trajectory

echo "Generating the file '$filename.xyz' containing the trajectory..."
nat=$(grep -m 1 number\ of\ atoms $1 | awk '{print $5}')

#If the file is a .pwi
if [ -z "$nat" ]
then
IFS='=' read -ra arr <<< "$(grep -m 1 nat $1)"
nat=${arr[1]}
nat=${nat// /}
nat=${nat//,/}
fi

grep -A $nat ATOMIC_POSITIONS $1 >  $filename.xyz
sed -i "s/--/$nat/g" $filename.xyz
sed -i "1s/^/$nat \n/" $filename.xyz
sed -i 's/0   0   0//g' $filename.xyz
