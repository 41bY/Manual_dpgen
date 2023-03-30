# -*- coding: utf-8 -*-
"""
Author Alberto

Script for dpdata
"""
from dpdata import LabeledSystem, MultiSystems
from glob import glob
import sys


n_batches = 10


#number_of_set = 1
iteration = int(sys.argv[1])
DATA_DIR = str(sys.argv[2])

RAW_DIR = DATA_DIR + 'Data_RAW'
NPY_DIR = DATA_DIR + 'Data_NPY'

fs_all=glob(RAW_DIR+'/*/*')  # remeber to change here !!!
ms=MultiSystems()
print(fs_all)


#From second iteration, train the network with only new data initializing from old network
#So remove RAW Data from iteration 1
#if iteration > 1: fs = [f for f in fs_all if not 'Step1' in f]

#At first iteration use all the found RAW Data and create a Network from scratch
#elif iteration == 1: fs = fs_all 
#else: raise ValueError("Iteration must be a positive integer number!")
fs = fs_all
print(fs)
for f in fs:
    print(f)
    try:
        ls=LabeledSystem(f, fmt = 'deepmd/raw')
        ls.shuffle()
    except:
        print(f)



    if len(ls)>0:
        ms.append(ls)
print(ms)


for ls in ms:
    #print(ls)
    n_frames = ls.get_nframes()
    
    if n_frames < n_batches: size = 1
    else: size = int(n_frames/n_batches) + 1
    
    # size = n_frames
        
    types = ls.get_atom_names()
    nat_per_type = ls.get_atom_numbs()
    
    name = '/'
    for i, ele in enumerate(types):
        name = name + str(ele) + str(nat_per_type[i])
    print(name)
    print(n_frames)
    print(size)
    
    ls.shuffle()
    ls.to_deepmd_npy(NPY_DIR+name+'/', set_size=size)

#size is the maximum number of frames in each set
#size = int(ms.get_nframes()/number_of_set)+1
#size = 200
#ms.to_deepmd_npy('Data_deepmd', set_size=size)
