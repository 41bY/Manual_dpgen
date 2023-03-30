#!/bin/bash

n_ite=$(bash Max_iter_num.sh /m100_work/IscrC_GF-Diam/alberto/Manual_dpgen_v2/Data/QE-scf/)

for dir in /m100_work/IscrC_GF-Diam/alberto/Manual_dpgen_v2/Data/ML-FF-MD/*/
do
sys=$(basename $dir)
dname=$(dirname $dir)

echo "Analysing results for system: $sys"

Emax=0
Fmax=0

Ftot=0
Fcount=0

Etot=0
Ecount=0

for it in $( seq 1 1 $n_ite )
do
step=Step$it

toPrint=($(python Analyse-deviation.py $dname/../QE-scf/$step/OUTPUT/ $dir/$step/OUTPUT/${sys}.out $dir/$step/OUTPUT/${sys}_dynforces.xyz))

F="${toPrint[4]}"

if [ "${#F}" -gt "1" ] && [ "$F" != "inf" ]
then 

Ftot=$(echo "$Ftot + $F" | bc -l )
Fcount=$(echo "$Fcount + 1" | bc -l )

if (( $(echo "$F > $Fmax" | bc -l) ))
then
Fmax=$F
sys_Fmax="$step for $sys"
fi

fi

E="${toPrint[10]}"

if [ "${#E}" -gt "1" ] && [ "$E" != "inf" ]
then 

Etot=$(echo "$Etot + $E" | bc -l )
Ecount=$(echo "$Ecount + 1" | bc -l )

if (( $(echo "$E > $Emax" | bc -l) ))
then
Emax=$E
sys_Emax="$step for $sys"
fi
fi
done

Favg=$(echo "$Ftot/$Fcount" | bc -l)
Eavg=$(echo "$Etot/$Ecount" | bc -l)

echo "Maximum Force err: $Fmax at $sys_Fmax"
echo "Maximum Energy err: $Emax at $sys_Emax";
echo "Average Force err: $Favg"
echo "Average Energy err: $Eavg";

done
