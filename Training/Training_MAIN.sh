#!/bin/bash

module purge
module load python/3.8.2
module load autoload hdf5/1.12.0--gnu--8.4.0

((QEstep = $1 - 1))

QEinp_dir=../../Data/QE-scf/Step$QEstep/INPUT
QEout_dir=../../Data/QE-scf/Step$QEstep/OUTPUT

for filename in $QEout_dir/*/*.pwo
do

found=$(grep '!' $filename | wc -l)

if [ "$found" -ge "1" ]
then
fname=$(basename $filename)
BaseName=${fname//.pwo/}
DirName=../../Data/Training/Data_RAW/Step$1/$BaseName
mkdir -p $DirName

echo "$QEinp_dir/$BaseName.pwi"
echo "$QEout_dir/$BaseName/$BaseName.pwo"
echo "$DirName"

#Generate RAW files from QE pwos
python ./QE-to-RAW_dpgen.py $QEinp_dir/$BaseName.pwi $QEout_dir/$BaseName/$BaseName.pwo $DirName/

else
echo "$filename has not converged"

fi
done

#Generate NPY files from RAW files
python ./Script-dpdata.py $1 ../../Data/Training/

#Divide NPY data into Training and Validation sets
bash ./Divide_NPYdata.sh 

#Generate Training input file based on new NPY files
mkdir -p ../../Data/Training/OUTPUT/Step$1/
python ./Create-Input-Training.py ../../Data/Training/Data_Train/ ../../Data/Training/Data_Valid/ ../../Data/Training/OUTPUT/Step$1/

##if [ $1 -eq "1" ]; then
cp ./jobscript_training ../../Data/Training/OUTPUT/Step$1/
cd ../../Data/Training/OUTPUT/Step$1/
sbatch jobscript_training .

##elif [ $1 -gt "1" ]; then 
##cp ./jobscript_training_restart ../../Data/Training/OUTPUT/Step$1/
##cd ../../Data/Training/OUTPUT/Step$1/
##sbatch jobscript_training_restart . ../Step1/model.ckpt
##fi

LOG=../../../../LOG

echo "--------------------------------------------------------" >> $LOG
echo "$( date )" >> $LOG
echo "Main itaration: $1" >> $LOG
echo "Training phase in progress..." >> $LOG
echo "Next phase will be LAMMPS MD..." >> $LOG
