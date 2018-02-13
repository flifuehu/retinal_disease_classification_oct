# run different tests
import os
import json
import base64

########################################################################################################################
#       WITHOUT ANY FILTER
########################################################################################################################

# experiment_name = 'D0_before-D7'
experiment_name = 'D0b-D14_woPBS,LE'
DATASET = {'healthy': ['D0b'],
           'pathological': ['D14']}
PATTERNS_EXCLUDED_TRAINING = ['']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')
