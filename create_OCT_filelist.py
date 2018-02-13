import os
import shutil
from tqdm import tqdm
from PIL import Image


dataset_folder = '/media/CVBLab/Proyectos/GALAHAD/INVESTIGACION/BBDD/REGH/201801/RAT OCT STUDIES/'


def keep_only_tiff(file_path):
    return file_path.find('.tif') != -1 and file_path.find('_raw') == -1 and file_path.find('_fundus') == -1  and file_path.find('_layers') == -1  and file_path.find('Sandra') == -1

# 17-2-6 ET1-4 +++
# 17-5-23 100uM ET1 3ul pilot
# 17-6-20 ET1 dose response study PartB
# 17-7-24 ET-1 300-500 DR StudyB t2
# 17-7-29 ET-1 100-500 DR StudyB t3
# C-3 NPY335-ET1 17-10-30
# Study C-2  ET1 17-9-1
# Study C-5 2018  Dose Response
# STUDY C T1 17-8-14 ET1

list_files = []
for subdir, dirs, files in os.walk(dataset_folder, topdown=True):
    for file in files:
        # print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        list_files.append(filepath) # [len(dataset_folder):])

list_files_tiff = list(filter(keep_only_tiff, list_files))

# save all files
with open(os.path.join('dataset_information', 'all_files_list.csv'), 'w') as result_file:
    for f in list_files_tiff:
        result_file.write(f + '\n')
print('All files list generated!')

# create a good usable filelist
# oct_name, oct_experiment, oct_label, oct_day, oct_day_moment, oct_pbs, oct_cage, oct_group, oct_eye, oct_dose, fn
import re
oct_file_list = []
trim = re.compile('\s+')
for fn in list_files_tiff:
    re_cage = re.search(r'C\s*?\d+', fn)
    re_group = re.search(r'A\s*?\d+', fn)
    re_eye = re.search(r'(/[lL].*?[eE]/)', fn)
    re_day = re.search(r'(?i)[d](ay)?\s*?\d{1,2}', fn)
    re_dose = re.search(r'\d{2,3}uM', fn)
    re_pbs = re.search(r'(?i)pbs', fn)
    re_before = re.search(r'(?i)before', fn)
    re_after = re.search(r'(?i)after', fn)
    re_name = re.search(r'OCT_Image.*?\d{2}\.tif', fn)

    if re_cage != None:
        oct_cage = trim.sub('', re_cage.group())
    else:
        oct_cage = '-'

    if re_group != None:
        oct_group = trim.sub('', re_group.group())
    else:
        oct_group = '-'

    if re_eye != None:
        oct_eye = 'left'
    else:
        oct_eye = 'right'

    if re_day != None:
        oct_day = re.search('\d+', re_day.group())
        oct_day = str(oct_day.group()) if oct_day != None else print('ERROR!')
    else:
        oct_day = '-'

    if re_before != None:
        oct_day = '0' if oct_day == '-' else oct_day
        oct_day_moment = 'before'
    elif re_after != None:
        oct_day = '0' if oct_day == '-' else oct_day
        oct_day_moment = 'after'
    else:
        oct_day_moment = '-'

    if re_dose != None:
        oct_dose = re_dose.group()
    else:
        oct_dose = '-'

    if re_pbs != None:
        oct_pbs = 'PBS'
    else:
        oct_pbs = '-'

    if re_name != None:
        oct_name = re_name.group()
    else:
        oct_name = fn.split(os.sep)[-1]

    # oct label
    oct_label = 'healthy' if oct_pbs == 'PBS' or oct_eye == 'left' or oct_day_moment == 'before' else 'pathological'

    # oct expetiment
    oct_experiment = fn.split('RAT OCT STUDIES')[1].split(os.sep)[1]

    # add oct instance to the list
    oct_file_list.append([oct_name, oct_experiment, oct_label, oct_day, oct_day_moment, oct_pbs, oct_cage, oct_group, oct_eye, oct_dose, fn])

# write csv with oct_file_list
with open(os.path.join('dataset_information', 'OCT_file_list.csv'), 'w') as result_file:
    result_file.write('name,experiment,label,day,day_moment,pbs,cage,group,eye,dose,path\n')
    for r in oct_file_list:
        result_file.write(','.join(r) + '\n')
print('OCT_file_list created!')
