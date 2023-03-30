# -*- coding: utf-8 -*-
"""
Author Alberto

Script for dpdata
"""
import json
import sys
import os
import random
from glob import glob

TRAIN_DIR = str(sys.argv[1])
VALID_DIR = str(sys.argv[2])
OUT_DIR = str(sys.argv[3])

training_system_paths = glob(TRAIN_DIR+'*')
for i, path in enumerate(training_system_paths):
    abs_path = os.path.abspath(path)
    ok_path = abs_path.replace('\\', '/')
    training_system_paths[i] = ok_path

validation_system_paths = glob(VALID_DIR+'*')
for i, path in enumerate(validation_system_paths):
    abs_path = os.path.abspath(path)
    ok_path = abs_path.replace('\\', '/')
    validation_system_paths[i] = ok_path
#Model dictionary#######################################################
model = {}

type_map = ["Fe", "C", "O", "H"]

descriptor = {}
type_ = "se_e2_a"
sel = [300, 200, 200, 200]
rcut_smth = 1.50
rcut = 9.00
neuron = [25, 50, 100]
resnet_dt = False
axis_neuron = 16
seed = 1
descriptor['type'] = type_
descriptor['sel'] = sel
descriptor['rcut_smth'] = rcut_smth
descriptor['rcut'] = rcut
descriptor['neuron'] = neuron
descriptor['resnet_dt'] = resnet_dt
descriptor['axis_neuron'] = axis_neuron
descriptor['seed'] = seed
descriptor['_comment_model'] = " that's all"

fitting_net = {}
neuron = [240, 240, 240]
resnet_dt = True
seed = 1
fitting_net['neuron'] = neuron
fitting_net['resnet_dt'] = resnet_dt
fitting_net['seed'] = seed
fitting_net['_comment'] = " that's all"


model['type_map'] = type_map
model['descriptor'] = descriptor
model['fitting_net'] = fitting_net
model['_comment'] = " that's all"
##########################################################################


#Learning rate dictionary#################################################
learning_rate = {}
type_ = "exp"
decay_steps = 5000
start_lr = 0.001
stop_lr = 3.51e-8
learning_rate['type'] = type_
learning_rate['decay_steps'] = decay_steps
learning_rate['start_lr'] = start_lr
learning_rate['stop_lr'] = stop_lr
learning_rate['_comment'] = " that's all"
##########################################################################


#Loss dictionary#################################################
loss = {}
type_ = "ener"
start_pref_e = 0.02
limit_pref_e = 1
start_pref_f = 1000
limit_pref_f = 1
start_pref_v = 0
limit_pref_v = 0
loss['type'] = type_
loss['start_pref_e'] = start_pref_e
loss['limit_pref_e'] = limit_pref_e
loss['start_pref_f'] = start_pref_f
loss['limit_pref_f'] = limit_pref_f
loss['start_pref_v'] = start_pref_v
loss['limit_pref_v'] = limit_pref_v
loss['_comment'] = " that's all"
##########################################################################



#Training dictionary#################################################
training = {}

training_data = {}
systems = training_system_paths
batch_size = "auto"
auto_prob = "prob_uniform"
training_data['systems'] = systems
training_data['batch_size'] = batch_size
training_data["auto_prob"] = auto_prob
training_data['_comment'] = " that's all"

validation_data = {}
systems = validation_system_paths
batch_size = 1
numb_btch = 6
validation_data['systems'] = systems
validation_data['batch_size'] = batch_size
validation_data['numb_btch'] = numb_btch
validation_data['_comment'] = " that's all"

numb_steps = 1000000
seed = random.randint(1,999999)
disp_file = "lcurve.out"
disp_freq = 1000
save_freq = 10000
training['training_data'] = training_data
training['validation_data'] = validation_data
training['numb_steps'] = numb_steps
training['seed'] = seed
training['disp_file'] = disp_file
training['disp_freq'] = disp_freq
training['save_freq'] = save_freq
training['_comment'] = " that's all"
##########################################################################

file_dictionary = {}
file_dictionary['_comment'] = " model parameters"
file_dictionary['model'] = model
file_dictionary['learning_rate'] = learning_rate
file_dictionary['loss'] = loss
file_dictionary['training'] = training
file_dictionary['_comment'] = " that's all"

jsonString = json.dumps(file_dictionary, indent=4)

with open(OUT_DIR+'input.json', 'w') as f_out:
    f_out.write(jsonString)
