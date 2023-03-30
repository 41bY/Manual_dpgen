#!/bin/bash

#Get final iteration number
n_ite=$(bash Max_iter_num.sh /m100_work/IscrC_GF-Diam/alberto/Manual_dpgen_v2/Data/QE-scf/)


#Process data files
for Step in $( seq 1 1 $n_ite )
do
avg_time=0

for dir in /m100_work/IscrC_GF-Diam/alberto/Manual_dpgen_v2/Data/ML-FF-MD/*/
do
IFS='/' read -ra arr <<< $dir
sys=${arr[-1]}
file=${dir}Step$Step/INPUT/${sys}_start.in
read -ra var <<< $( grep 'run' $file | tail -n 1 )
val=${var[1]}
avg_time=$(( $val + $avg_time ))
done
avg_time=$(( $avg_time/30 ))
echo "Mean iteration number at step $Step = $avg_time"
done
