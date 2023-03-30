#!/bin/bash

rm ./All-sampling.xyz
rm ./Frame-map.txt

count=0
for ite in 1 2 3 4 5
do

for file in ../../../Data/QE-scf/Step$ite/INPUT/*.pwi
do

fname=$(basename $file)
pwo_file=${file//INPUT\/$fname/OUTPUT\/${fname//.pwi/}\/${fname//.pwi/.pwo}}

found=$(grep '!' $pwo_file | wc -l)
if [ "$found" != "1" ]
then
continue
fi

bash ./conv.sh $file

cat ${file//.pwi/.xyz} >> All-sampling.xyz
echo "Frame $count -> ${fname//.pwi/-It$ite}" >> Frame-map.txt
count=$(( $count + 1 ))

done
done
