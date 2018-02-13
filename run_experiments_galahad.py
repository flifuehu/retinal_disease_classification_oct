# run different tests
import os
import json
import base64

########################################################################################################################
#       WITHOUT ANY FILTER
########################################################################################################################

# experiment_name = 'D0_before-D7'
experiment_name = 'D0_before-D7'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D7.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')


# experiment_name = 'D0_before-D14'
experiment_name = 'D0_before-D14'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D14.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')



# experiment_name = 'D0_beforeD7_PBS-D7'
experiment_name = 'D0_beforeD7_PBS-D7'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv',
                       '/home/felix/Scratch/projects/galahad/dataset_information/D7_PBS.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D7.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')



# experiment_name = 'D0_beforeD14_PBS-D14'
experiment_name = 'D0_beforeD14_PBS-D14'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv',
                       '/home/felix/Scratch/projects/galahad/dataset_information/D14_PBS.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D14.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')



# experiment_name = 'D0_beforeD7_PBSD14_PBS-D7D14'
experiment_name = 'D0_beforeD7_PBSD14_PBS-D7D14'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv',
                       '/home/felix/Scratch/projects/galahad/dataset_information/D7_PBS.csv',
                       '/home/felix/Scratch/projects/galahad/dataset_information/D14_PBS.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D7.csv',
                            '/home/felix/Scratch/projects/galahad/dataset_information/D14.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')



########################################################################################################################
#       WITH GAUSSIAN FILTER
########################################################################################################################


# experiment_name = 'D0_before-D7'
experiment_name = 'D0_before-D7-gf'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D7.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')



# experiment_name = 'D0_before-D14'
experiment_name = 'D0_before-D14-gf'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D14.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')



# experiment_name = 'D0_beforeD7_PBS-D7'
experiment_name = 'D0_beforeD7_PBS-D7-gf'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv',
                       '/home/felix/Scratch/projects/galahad/dataset_information/D7_PBS.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D7.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')


# experiment_name = 'D0_beforeD14_PBS-D14'
experiment_name = 'D0_beforeD14_PBS-D14-gf'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv',
                       '/home/felix/Scratch/projects/galahad/dataset_information/D14_PBS.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D14.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')



# experiment_name = 'D0_beforeD7_PBSD14_PBS-D7D14'
experiment_name = 'D0_beforeD7_PBSD14_PBS-D7D14-gf'
DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv',
                       '/home/felix/Scratch/projects/galahad/dataset_information/D7_PBS.csv',
                       '/home/felix/Scratch/projects/galahad/dataset_information/D14_PBS.csv'],
           'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D7.csv',
                            '/home/felix/Scratch/projects/galahad/dataset_information/D14.csv']}
PATTERNS_EXCLUDED_TRAINING = ['C-2']

json_parameters = {'experiment_name': experiment_name,
                   'DATASET': DATASET,
                   'PATTERNS_EXCLUDED_TRAINING': PATTERNS_EXCLUDED_TRAINING}

json_parameters_encoded = json.dumps(json_parameters)
json.dump(json_parameters, open('jsparams.txt', 'w'))

params = '-cs 224 -l 2e-4 -uiw --max-epoch 40 -b 4 -cm DenseNet201 -doc 0.4 -jp'
os.system('python train.py ' + params + ' >> ' + experiment_name + '.txt')
