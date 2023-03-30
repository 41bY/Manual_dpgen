#!/bin/bash

module purge
module load python/3.8.2
module load autoload hdf5/1.12.0--gnu--8.4.0

mkdir -p ../../Data/QE-scf/Step$1/INPUT/
num_samples=2


for dir in ../../Data/ML-FF-MD/*/
do

Sys=$(basename $dir)

python Select_structures.py ../../Data/ML-FF-MD/$Sys/Step1/INPUT/${Sys}_pos.data ../../Data/ML-FF-MD/$Sys/Step$1/OUTPUT/${Sys}_dynpos.xyz $num_samples ../../Data/QE-scf/Step$1/INPUT/

done

for filename in ../../Data/QE-scf/Step$1/INPUT/*.pwi
do
Base=$(basename $filename)
DirName=${Base//.pwi/}
outfname=${Base//.pwi/.pwo}

mkdir -p ../../Data/QE-scf/Step$1/OUTPUT/$DirName/OUT
sbatch jobscript_QE $filename ../../Data/QE-scf/Step$1/OUTPUT/$DirName/$outfname 
done

LOG=../../LOG

echo "-------------" >> $LOG 
echo "QE-scf sampling phase in progress..." >> $LOG
echo "This is the ending phase of iteration $1" >> $LOG
