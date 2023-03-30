# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 10:35:51 2022

@author: Alberto
"""
import sys
import os
import numpy as np

#Usage:
# python QE-to-RAW_dpgen.py QEinput QEoutput OutputDir

#Only .pwo is required. .pwi is given if external forces are present.
#Variable Cell calculations are considered with changing cell at every iteration.
#External forces are subtracted from total forces read.
#Type_map given in input.
#Atomic types are trimmed to exclude numbers.
#TODO: Unit handling. For now these physical units are expected:
    # Energy (Rydberg)
    # alat (Bohr)
    # Atomic coordinates (angstrom)
    # Cell parameters (angstrom)
    # Forces (Rydberg/Bohr)

name_pwi = str(sys.argv[1])
name_pwo = str(sys.argv[2])
name_OUTdir = str(sys.argv[3])
type_map = {'Fe' : 0, 'C' : 1, 'O' : 2, 'H' : 3}

Ry2eV = 13.605698066
B2A = 0.529177
A2B = 1.8897259886

box_raw = open(name_OUTdir+'box.raw', 'w')
coord_raw = open(name_OUTdir+'coord.raw', 'w')
energy_raw = open(name_OUTdir+'energy.raw', 'w')
force_raw = open(name_OUTdir+'force.raw', 'w')

types = []
box = []
coords = []
forces_ext = []
forces = []
energy = None                    

if os.path.isfile(name_pwi):
    with open(name_pwi, 'r') as infile:
        
        for line in infile:
            if ('CELL_PARAMETERS' in line):
                for line in infile:
                    row = line.split()
                    if len(row) != 3:
                        break
                    
                    box.append(list(map(float,row)))
            
            elif ('ATOMIC_POSITIONS' in line):
                for line in infile:
                    row = line.split()
                    if len(row) != 4 and len(row) != 7: break
                    
                    atom = ''.join(c for c in row[0] if c in 'AaBbCcDdEeFfGgHhIiLlMmNnOoPpQqRrSsTtUuVvZzXxYyJjKkWw')
                    coords.append(list(map(float,row[1:4])))
                    
                    if atom in type_map: types.append(type_map[atom])     
                    else: raise ValueError('Atomic type not found')
                        
            elif ('ATOMIC_FORCES' in line):
                for line in infile:
                    row = line.split()
                    if len(row) != 4:
                        break
                    
                    atom = row[0]
                    forces_ext.append(list(map(float,row[1:4])))

if len(forces_ext) == 0: forces_ext = np.zeros((len(coords), 3)) #No external forces
else: forces_ext = np.array(forces_ext) #External forces


#Read .pwo
if os.path.isfile(name_pwo):
    with open(name_pwo, 'r') as infile:
        
        for line in infile:
            
            #Read atomic configuration first
            if len(coords) == 0 or len(box) == 0:
                
                if ('CELL_PARAMETERS' in line):
                    box = []
                    for line in infile:
                        row = line.split()
                        if len(row) != 3: break
                        
                        box.append(list(map(float,row)))                
                
            
                elif ('ATOMIC_POSITIONS' in line):
                    for line in infile:
                        row = line.split()
                        if len(row) != 4 and len(row) != 7: break
                        
                        coords.append(list(map(float,row[1:4])))
                    coords = np.array(coords) #Atomic coordinates in angstrom
                
                
                elif ('lattice parameter (alat)' in line):
                    token = line.split('=')[1]
                    alat = float(token.split()[0])*B2A #Lattice parameter in angstrom
            
            
                elif ('crystal axes:' in line):
                    box = []
                    for line in infile:
                        row = line.split()
                        if len(row) != 7: break
                    
                        box.append(list(map(float,row[3:6])))
                    
                    box = np.array(box)*alat #Cell parameters in angstrom


                elif ('site n.' in line):
                    for line in infile:
                        tokens = line.split('=')
                        if len(tokens) != 2: break
                        
                        token_at = tokens[0]
                        token_val = tokens[1]
                        
                        at = token_at.split()[1]
                        atom = ''.join(c for c in at if c in 'AaBbCcDdEeFfGgHhIiLlMmNnOoPpQqRrSsTtUuVvZzXxYyJjKkWw')
                        
                        if atom in type_map: types.append(type_map[atom])
                        else: raise ValueError('Atomic type not found')
                        
                        row = token_val.split()
                        coords.append(list(map(float,row[1:4])))       
                    coords = np.array(coords)*alat #Atomic coordinates in angstrom
            
            #Read energy and force data for the specific atomic configuration
            else:
            
                if ('!    total energy' in line):
                    energy = float(line.split()[4])*Ry2eV #Energy in eV
                
                
                elif ('Forces acting on atoms' in line):
                    forces_tmp = []
                    next(infile)
                    for line in infile:
                        row = line.split()
                        if len(row) != 9: break
                        
                        forces_tmp.append(list(map(float,row[6:])))
                    
                    if len(forces_ext) == 0: forces_ext = np.zeros((len(coords), 3)) #No external forces
                    else: forces_ext = np.array(forces_ext) #External forces    
                    forces = (np.array(forces_tmp) - forces_ext)*(Ry2eV/B2A)
                    
            
            
            #Conditions for writing output
            if (energy != None and len(forces) != 0) and (len(coords) != 0 and len(box) != 0):
                
                if len(forces) == len(coords):
                
                    #Writing raw files
                    for cor in coords:
                        coord_raw.write(str(cor[0])+' '+str(cor[1])+' '+str(cor[2])+' ')
                    coord_raw.write('\n')
                    
                    for For in forces:
                        force_raw.write(str(For[0])+' '+str(For[1])+' '+str(For[2])+' ')
                    force_raw.write('\n')
                        
                    for cel_vec in box:
                        box_raw.write(str(cel_vec[0])+' '+str(cel_vec[1])+' '+str(cel_vec[2])+' ')
                    box_raw.write('\n')
                    
                    
                    #Compute ext. force energy contribution and subract from scf energy
                    U = 0.0
                    for i, cor in enumerate(coords):
                        for j in range(3):
                            U = U - forces_ext[i][j]*cor[j]*A2B #Ext. force energy in Rydberg
                    
                    energy = energy - U*Ry2eV #Scf energy in eV
                    energy_raw.write(str(energy)+'\n')
                    
                    energy = None
                    forces = []
                    coords = []
                    
                else: raise ValueError('Error: Mismatch between atomic coordinates and forces!')

else:
    raise ValueError('\'.pwo\' file not found!')

box_raw.close()
coord_raw.close()
energy_raw.close()
force_raw.close()

type_raw = open(name_OUTdir+'type.raw', 'w')
type_map_raw = open(name_OUTdir+'type_map.raw', 'w')

for atom in types:
    type_raw.writelines([str(atom)+' '])
    
for typs in type_map:
    type_map_raw.writelines([str(typs)+' '])

type_raw.close()
type_map_raw.close()