#!/bin/bash

module purge
module load python/3.8.2
module load autoload hdf5/1.12.0--gnu--8.4.0

((QEstep = $1 - 1))

for dir in ../../Data/ML-FF-MD/*/
do

Sys=$(basename $dir)

if [ "$1" -gt "1" ]; then
echo "Restart"
mkdir -p ../../Data/ML-FF-MD/$Sys/Step$1/INPUT
mkdir -p ../../Data/ML-FF-MD/$Sys/Step$1/OUTPUT

#Measure deviation between AB-INITIO and ML-MD to get new simulation time
TimeMultiplier=`python Measure-deviation.py ../../Data/QE-scf/Step$QEstep/OUTPUT/ ../../Data/ML-FF-MD/$Sys/Step$QEstep/OUTPUT/$Sys.out ../../Data/ML-FF-MD/$Sys/Step$QEstep/OUTPUT/${Sys}_dynforces.xyz`

#Write LAMMPS restart input

#if [ "$1" -eq "2" ]; then
#python Create-LAMMPS-restart_init.py ../../Data/ML-FF-MD/$Sys/Step1/INPUT/${Sys}_start.in $1 $TimeMultiplier

#elif [ "$1" -gt "2" ]; then
#python Create-LAMMPS-restart.py ../../Data/ML-FF-MD/$Sys/Step$QEstep/INPUT/${Sys}_restart.in $1 $TimeMultiplier
#fi

bash Modify-LAMMPS-start.sh $QEstep $1 ../../Data/ML-FF-MD/$Sys/Step$QEstep/INPUT/${Sys}_start.in ../../Data/ML-FF-MD/$Sys/Step$1/INPUT/${Sys}_start.in $TimeMultiplier 

#Restart LAMMPS simulation with new network
sbatch jobscript_LAMMPS ../../Data/ML-FF-MD/$Sys/Step$1/INPUT/${Sys}_start ../../Data/ML-FF-MD/$Sys/Step$1/OUTPUT/$Sys

else
sbatch jobscript_LAMMPS ../../Data/ML-FF-MD/$Sys/Step$1/INPUT/${Sys}_start ../../Data/ML-FF-MD/$Sys/Step$1/OUTPUT/$Sys

fi
done

LOG=../../LOG

echo "-------------" >> $LOG
echo "$( date )" >> $LOG
echo "LAMMPS MD phase in progress..." >> $LOG
echo "Next phase will be QE-scf sampling..." >> $LOG
