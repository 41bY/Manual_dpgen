# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 17:38:30 2023

@author: alber
"""

import sys

#Get LAMMPS input positions, xyz LAMMPS trajectory, number of frames, QE Input directory
IN_fname = str(sys.argv[1])
XYZ_fname = str(sys.argv[2])
N_frames = int(sys.argv[3])
QE_inp_path = str(sys.argv[4])

#IN_fname = 'Fe110+3AP+Fe110_pos.data'
#XYZ_fname = 'Fe110+3AP+Fe110_dyn_prova.xyz'
#N_frames = 10
#QE_inp_path = '../QE-scf/Step1/Input/'

OUT_fname = XYZ_fname.split('/')[-1].split('_dynpos.xyz')[0]

with open(IN_fname, 'r') as f:
    
    for n_line, line in enumerate(f):
        
        if n_line == 1: nat = int(line.split()[0])
        elif n_line == 2: ntyp = int(line.split()[0])
        elif n_line == 4: a = float(line.split()[1])
        elif n_line == 5: b = float(line.split()[1])
        elif n_line == 6: c = float(line.split()[1])
        
        elif n_line > 6: break   
    
with open(XYZ_fname, 'r') as f:
    
    block_size = int(f.readline()) + 2
    
    if (block_size - 2) != nat: raise ValueError("Mismatch between LAMMPS input and xyz trajectory!")
    
    n_lines = 1
    for line in f: n_lines = n_lines + 1
    

N_blocks = int(n_lines/block_size)
every_n_blocks = int(N_blocks/N_frames)

count_block = 0
with open(XYZ_fname, 'r') as f:
    
    for n in range(N_blocks):
        
        #Skip the block
        if n%every_n_blocks != 0:
            for i in range(block_size): f.readline()    
        
        
        #Save the block and write QE input file
        else:
            count_block += 1
            block = []
            for i in range(block_size):
                line = f.readline()
                block.append(line)

            
            time_step_frame = int(block[1].split('Timestep: ')[1])
            fname_out = QE_inp_path+OUT_fname+'_'+str(count_block)+'_frame_'+str(time_step_frame)+'.pwi'
            out_dir = fname_out.split('.pwi')[0].replace('/INPUT/', '/OUTPUT/')
            out_dir = out_dir + '/OUT/'
            
            pseudo_dir = QE_inp_path.split('Step')[0] + 'PSEUDO/'            

            strs_to_write = '&CONTROL\
                            \ncalculation = \'scf\'\
                            \nrestart_mode= \'from_scratch\'\
                            \npseudo_dir = \''+pseudo_dir+'\'\
                            \noutdir = \''+out_dir+'\'\
                            \nprefix = \'scf_conf\'\
                            \ntprnfor =.true.\
                            \ndisk_io = \'none\'\
                            \nmax_seconds = 7000  !2 hours\
                            \n/\
                            \n&SYSTEM\
                            \nibrav=0\
                            \nnat='+str(nat)+'\
                            \nntyp=4\
                            \nnosym=.true.\
                            \noccupations=\'smearing\'\
                            \nsmearing=\'gaussian\'\
                            \ndegauss=0.01\
                            \nnspin=2\
                            \nstarting_magnetization(1) = 1.2\
                            \necutwfc =30\
                            \necutrho =240\
                            \nvdw_corr=\'grimme-d2\'\
                            \n/\
                            \n&ELECTRONS\
                            \nelectron_maxstep= 800\
                            \ndiagonalization=\'david\'\
                            \nmixing_mode = \'local-TF\'\
                            \nmixing_beta = 0.50\
                            \nconv_thr = 1.0d-6\
                            \nstartingwfc = \'atomic\'\
                            \n/\
                            \nATOMIC_SPECIES\
                            \nFe   55.845   Fe.pbe-sp-van_ak.UPF\
                            \nC    12.0100   C.pbe-van_bm.UPF\
                            \nO    15.9990   O.pbe-van_bm.UPF\
                            \nH     1.00784  H.pbe-van_ak.UPF\
                            \n\
                            \nCELL_PARAMETERS angstrom\
                            \n'+str(a)+'  0.000000   0.000000\
                            \n0.000000   '+str(b)+'   0.000000\
                            \n0.000000   0.000000    '+str(c)+'\
                            \n\
                            \nK_POINTS gamma\
                            \n\
                            \nATOMIC_POSITIONS angstrom'            
            
            f_out = open(fname_out, 'w')
            f_out.write(strs_to_write)
            f_out.write('\n')
            
            for atom in block[2:]: f_out.write(atom)
            
            f_out.close()


                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
                
            
