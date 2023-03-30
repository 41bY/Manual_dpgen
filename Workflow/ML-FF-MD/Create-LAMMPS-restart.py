# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 16:39:09 2023

@author: alber
"""
import sys

LAMMPS_start_fname = str(sys.argv[1])
Step_num = int(sys.argv[2])
Simulation_step_factor = float(sys.argv[3])

# LAMMPS_start_fname = './INPUT/Step1/Fe110+3LG+Fe110-5GPa+800K_start.in'
# Step_num = 3
# Simulation_step_factor = 2

#Open LAMMPS_start input and save fixes and dumps

to_write = []
fix_modify = []
fix = []
thermo = []
dump = []
compute = []
variable = []
run = []

with open(LAMMPS_start_fname, 'r') as f:
    for line in f:
        tokens = line.split()
        
        if len(tokens) > 0:
            
            if 'fix' == tokens[0]:
                fix.append(line)
                
            elif 'pair_style' == tokens[0]:
                line = line.replace('Step'+str(Step_num - 1), 'Step'+str(Step_num))
                to_write.append(line)
    
            elif 'pair_coeff' == tokens[0]:
                to_write.append(line)           
                
            elif 'newton' == tokens[0]:
                to_write.append(line) 
    
            elif 'neighbor' == tokens[0]:
                to_write.append(line)               
            
            elif 'neigh_modify' == tokens[0]:
                to_write.append(line)        
            
            elif 'fix_modify' == tokens[0]:
                fix_modify.append(line)
    
            elif 'dump_dyn' in line:
                line = line.replace('/Step'+str(Step_num - 1)+'/', '/Step'+str(Step_num)+'/')
                dump.append(line)            
                
            elif 'compute' == tokens[0]:
                compute.append(line)            
                
            elif 'variable' == tokens[0]:
                variable.append(line)         
            
            elif 'thermo' in line:
                thermo.append(line)
            
            elif 'run' in line:
                run.append(line)

#Construct 'to_write' list to be written to restart file:
for fixes in fix:
    to_write.append(fixes)

to_write.append(fix_modify[-1])

for variables in variable:
    to_write.append(variables)

for computes in compute:
    to_write.append(computes)

for dumps in dump:
    to_write.append(dumps)    
        
to_write.append(thermo[-2])
to_write.append(thermo[-1])

Simulation_steps = int(int(run[-1].split()[1])*Simulation_step_factor)

#Write LAMMPS_restart

LAMMPS_fname_base = LAMMPS_start_fname.split('/')[-1]
LAMMPS_restart_fname = LAMMPS_fname_base 

OUTDIR = LAMMPS_start_fname.split('Step')[0]

Restart_in_path = OUTDIR.replace('INPUT', 'OUTPUT') + 'Step' + str(Step_num - 1) + '/' \
    + LAMMPS_fname_base.replace('_restart.in', '.restart')

Restart_out_path = Restart_in_path.replace('Step' + str(Step_num - 1), 'Step' + str(Step_num))

Network_path = '../Training/OUTPUT/Step' + str(Step_num) + '/graph_compressed.pb'

with open(OUTDIR+'Step'+str(Step_num)+'/'+LAMMPS_restart_fname, 'w') as f:
    
    f.write('read_restart ' + Restart_in_path)
    f.write('\n\n')
    for line in to_write:
        f.write(line)
    
    f.write('\n\nrun ' + str(Simulation_steps) + ' start 0')
    f.write('\nwrite_restart ' + Restart_out_path)
