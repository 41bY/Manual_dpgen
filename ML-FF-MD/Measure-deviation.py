# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 16:39:09 2023

@author: alber
"""
import sys
from glob import glob
import numpy as np

Ry2eV = 13.605703976
B2A = 0.529177

lmp_energy_pos = 2
energy_trh = 0.01 #Energy threshold in eV per atom
force_trh = 0.1 #Force threshold in eV/A per atom

#Loop through all QE outputs to save all the frame #
#Loop through all LMP force output and save all the forces corresponding to the frame #
#Read LMP.out to get energies at those frame #
#Compare the two 'Lists'

# QE_out_dirname = '../QE-scf/Step1/Output/'
# LMP_out_fname = 'OUTPUT/Step1/Fe110+3LG+Fe110-5GPa+800K.out'
# LMP_force_fname = 'OUTPUT/Step1/Fe110+3LG+Fe110-5GPa+800K_dynforces.xyz'

QE_out_dirname = str(sys.argv[1])
LMP_out_fname = str(sys.argv[2])
LMP_force_fname = str(sys.argv[3])

Sys = LMP_out_fname.split('.out')[0].split('/')[-1]

#Get frame numbers and save LMP forces for them
dirs = glob(QE_out_dirname+Sys+'*')
frame_nums = [int(Dir.split('/')[-1].split('_frame_')[1]) for Dir in dirs]

forces_lmp = {}

with open(LMP_force_fname) as f:
    
    for line in f:
        
        if 'TIMESTEP' in line:
            line = next(f)
            frame_num_lmp = int(line)
            
            if frame_num_lmp in frame_nums: #Match
                
                #Skip 7 lines
                for i in range(7): next(f)
                
                
                forces = []
                for line in f:
                    tokens = line.split()
                    
                    if len(tokens) != 4: break #End collect force loop
                    else:
                        forces.append(tokens[1:4]) #LMP forces in eV/A
                        
                forces = np.array(forces, dtype=float) 
                forces_lmp[str(frame_num_lmp)] = forces
            else: continue
        else: continue

#Get LMP energies from the '.out', get only sliding dynamic output
energies_lmp = {}

Step_counter = 0
with open(LMP_out_fname) as f:
    
    for line in f:
        
        if 'Step' in line: Step_counter += 1

Step_counter_finder = 0
with open(LMP_out_fname) as f:
    
    for line in f:
        
        if 'Step' in line:
            Step_counter_finder += 1
            
            if Step_counter_finder == Step_counter: #Right output section (sliding dynamics)
                    
                tokens_num = len(line.split())
            
                for line in f:
                    tokens = line.split()
                    
                    if len(tokens) != tokens_num: break
                    
                    time_step = int(tokens[0])
                    energy = float(tokens[lmp_energy_pos]) #Energy in eV
                    
                    if time_step in frame_nums: energies_lmp[str(time_step)] = energy


#Get QE energies and forces for every QE output           
forces_qe = {}                    
energies_qe = {}


for Dir in dirs:
    
    Dir = Dir.replace('\\', '/')
    QE_out_name = Dir.split('/')[-1]
    Step_num = int(QE_out_name.split('_frame_')[1])
    fname = Dir+'\\'+QE_out_name+'.pwo'
    fname = fname.replace('\\', '/')

    #Get energy and forces from QE output
    energy_QE = 0
    forces_QE = []
    
    nat = 0
    with open(fname) as f:
        for line in f:
            
            if '!' in line:
                energy_QE = float(line.split()[4])*Ry2eV #Energy in eV
                
            if 'Forces acting on atoms' in line:
                line = next(f) #Void line
                
                for line in f:
                    tokens = line.split()
                    
                    if len(tokens) == 0: break
                    else:
                        nat += 1
                        forces_QE.append(tokens[6:9])
    
    forces_QE = np.array(forces_QE, dtype=float)*(Ry2eV/B2A) #Forces in eV/angstrom

    forces_qe[str(Step_num)] = forces_QE
    energies_qe[str(Step_num)] = energy_QE


#Get Error between LMP and QE energies and forces for every frame
energies_err = {}
forces_err = {}

for frame in frame_nums:
    
    step = str(frame)
    
    if forces_qe[step].size == 0: #SCF did not converged -> Maximum error
        energies_err[step] = 2*energy_trh 
        forces_err[step] = 2*force_trh

    else:
        energies_err[step] = abs(energies_qe[step] - energies_lmp[step])/nat
        forces_err[step] = np.max(np.sqrt(np.mean((forces_qe[step] - forces_lmp[step])**2, axis=0)))

energy_error_max = 0
force_error_max = 0

for frame in frame_nums:
    
    step = str(frame)
    
    if energies_err[step] > energy_error_max: energy_error_max = energies_err[step] 
    if forces_err[step] > force_error_max: force_error_max = forces_err[step]
    
#Print MD simulation time multiplier to bash variable
good_dynamics = (energy_error_max < energy_trh) and (force_error_max < force_trh)
sample_dynamics = ((energy_error_max < energy_trh) and (force_error_max > force_trh)) or ((energy_error_max > energy_trh) and (force_error_max < force_trh))
bad_dynamics = (energy_error_max > energy_trh) and (force_error_max > force_trh)


if good_dynamics:
    print("2.0")

elif sample_dynamics:
    print("1.0")

elif bad_dynamics:
    print("0.5")

else: raise ValueError("Impossible deviation has occurred, something went wrong...")
