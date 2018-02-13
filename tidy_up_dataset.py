import os
import shutil
from tqdm import tqdm
from PIL import Image


dataset_folder = '/media/CVBLab/Proyectos/GALAHAD/INVESTIGACION/BBDD/REGH/201801/RAT OCT STUDIES/'


def keep_only_tiff(file_path):
    return file_path.find('.tif') != -1 and file_path.find('_raw') == -1 and file_path.find('_fundus') == -1  and file_path.find('_layers') == -1  and file_path.find('Sandra') == -1


def string_complies_with(s, needles_yes, needles_no=[]):
    # positive needles
    for n in needles_yes:
        if s.find(n) == -1:
            return False
    # negative needles
    for n in needles_no:
        if s.find(n) != -1:
            return False
    # if not string meets conditions
    return True


def findall(p, s):
    '''Yields all the positions of
    the pattern p in the string s.'''
    i = s.find(p)
    while i != -1:
        yield i
        i = s.find(p, i + 1)


# 17-2-6 ET1-4 +++
# 17-5-23 100uM ET1 3ul pilot
# 17-6-20 ET1 dose response study PartB
# 17-7-24 ET-1 300-500 DR StudyB t2
# 17-7-29 ET-1 100-500 DR StudyB t3
# C-3 NPY335-ET1 17-10-30
# Study C-2  ET1 17-9-1
# Study C-5 2018  Dose Response
# STUDY C T1 17-8-14 ET1

# filter out DAY 0 before
def filter_D0_before(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D0', 'before'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D0', 'before'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 0', 'before'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'DAY 0', 'Before'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 0', 'Before'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Before'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Before'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Before'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Before'])
    return all_filters


# filter out DAY 0 after
def filter_D0_after(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D0', 'after'], ['PBS', 'pbs'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D0', 'after'], ['PBS', 'pbs'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 0', 'after'],
                                                      ['PBS', 'pbs'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'DAY 0', 'After'],
                                                      ['PBS', 'pbs'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 0', 'After'],
                                                      ['PBS', 'pbs'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'After'], ['PBS', 'pbs'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'After'], ['PBS', 'pbs'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'After'], ['PBS', 'pbs'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'After'], ['PBS', 'pbs'])
    return all_filters


# filter out DAY 0 after PBS
def filter_D0_after_PBS(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D0', 'after', 'PBS'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D0', 'after', 'PBS'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 0', 'after',
                                                          'PBS'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'DAY 0', 'After', 'PBS'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 0', 'After', 'PBS'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'After', 'PBS'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'After', 'PBS'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'After', 'PBS'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'After', 'PBS'])
    return all_filters


# filter out DAY 0
def filter_D0(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D0'], ['fter', 'efore'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D0'], ['fter', 'efore'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 0'],
                                                      ['fter', 'efore'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'DAY 0'],
                                                      ['fter', 'efore'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 0'],
                                                      ['fter', 'efore'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Day 0'], ['fter', 'efore'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Day 0'], ['fter', 'efore'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Day 0'], ['fter', 'efore'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Day 0'], ['fter', 'efore'])
    return all_filters


# filter out DAY 3
def filter_D3(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D3'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D3'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 3'],
                                                      ['PBS', 'pbs'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'DAY 3'], ['PBS', 'pbs'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 3'], ['PBS', 'pbs'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Day 3'], ['PBS', 'pbs'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Day 3'], ['PBS', 'pbs'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Day 3'], ['PBS', 'pbs'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Day3'], ['PBS', 'pbs'])
    return all_filters


# filter out DAY 7
def filter_D7(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D7'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D7'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 7'],
                                                      ['PBS', 'pbs'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'DAY 7'], ['PBS', 'pbs'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 7'], ['PBS', 'pbs', '70'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Day 7'], ['PBS', 'pbs'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Day 7'], ['PBS', 'pbs'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Day 7'], ['PBS', 'pbs'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Day7'], ['PBS', 'pbs'])
    return all_filters


# filter out DAY 7 PBS
def filter_D7_PBS(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D7', 'PBS'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D7', 'PBS', 'pbs'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 7', 'PBS'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'Day 7', 'PBS'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 7', 'PBS'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Day 7', 'PBS'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Day 7', 'PBS'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Day 7', 'PBS'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Day7', 'PBS'])
    return all_filters


# filter out DAY 14
def filter_D14(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D14'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D14'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 14'],
                                                      ['PBS', 'pbs'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'Day 14'],
                                                      ['PBS', 'pbs'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 14'],
                                                      ['PBS', 'pbs'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Day 14'], ['PBS', 'pbs'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Day 14'], ['PBS', 'pbs'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Day 14'], ['PBS', 'pbs'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Day14'], ['PBS', 'pbs'])
    return all_filters


# filter out DAY 14 PBS
def filter_D14_PBS(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D14', 'PBS'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D14', 'PBS'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 14', 'PBS'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'Day 14', 'PBS'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 14', 'PBS'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Day 14', 'PBS'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Day 14', 'PBS'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Day 14', 'PBS'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Day14', 'PBS'])
    return all_filters


# filter out DAY 17
def filter_D17(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D17'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'day17'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 17'],
                                                      ['PBS', 'pbs'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'Day 17'],
                                                      ['PBS', 'pbs'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 17'],
                                                      ['PBS', 'pbs'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Day 17'], ['PBS', 'pbs'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Day 17'], ['PBS', 'pbs'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Day 17'], ['PBS', 'pbs'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Day17'], ['PBS', 'pbs'])
    return all_filters


# filter out DAY 21
def filter_D21(s):
    # 17-2-6 ET1-4 +++
    all_filters = string_complies_with(s, ['17-2-6 ET1-4 +++', 'D21'])
    # 17-5-23 100uM ET1 3ul pilot
    all_filters = all_filters or string_complies_with(s, ['17-5-23 100uM ET1 3ul pilot', 'D21'])
    # 17-6-20 ET1 dose response study PartB
    all_filters = all_filters or string_complies_with(s, ['17-6-20 ET1 dose response study PartB', 'Day 21'],
                                                      ['PBS', 'pbs'])
    # 17-7-24 ET-1 300-500 DR StudyB t2
    all_filters = all_filters or string_complies_with(s, ['17-7-24 ET-1 300-500 DR StudyB t2', 'Day 21'],
                                                      ['PBS', 'pbs'])
    # 17-7-29 ET-1 100-500 DR StudyB t3
    all_filters = all_filters or string_complies_with(s, ['17-7-29 ET-1 100-500 DR StudyB t3', 'Day 21'],
                                                      ['PBS', 'pbs'])
    # C-3 NPY335-ET1 17-10-30
    all_filters = all_filters or string_complies_with(s, ['C-3 NPY335-ET1 17-10-30', 'Day 21'], ['PBS', 'pbs'])
    # Study C-2  ET1 17-9-1
    all_filters = all_filters or string_complies_with(s, ['C-2  ET1 17-9-1', 'Day 21'], ['PBS', 'pbs'])
    # Study C-5 2018  Dose Response
    all_filters = all_filters or string_complies_with(s, ['C-5 2018  Dose Response', 'Day 21'], ['PBS', 'pbs'])
    # STUDY C T1 17-8-14 ET1
    all_filters = all_filters or string_complies_with(s, ['C T1 17-8-14 ET1', 'Day21'], ['PBS', 'pbs'])
    return all_filters


list_files = []
for subdir, dirs, files in os.walk(dataset_folder, topdown=True):
    for file in files:
        # print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        list_files.append(filepath) # [len(dataset_folder):])

list_files_tiff = list(filter(keep_only_tiff, list_files))

# save all files
print('All files list generated!')
with open(os.path.join('dataset_information', 'all_files_list.csv'), 'w') as result_file:
    for f in list_files_tiff:
        result_file.write(f + '\n')

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
        oct_day_moment = '-'
    else:
        if re_before != None:
            oct_day = '0'
            oct_day_moment = 'before'
        elif re_after != None:
            oct_day = '0'
            oct_day_moment = 'after'
        else:
            oct_day = '-'
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
    result_file.write('oct_name, oct_experiment, oct_label, oct_day, oct_day_moment, oct_pbs, oct_cage, oct_group, oct_eye, oct_dose, oct_path\n')
    for r in oct_file_list:
        result_file.write(', '.join(r) + '\n')
print('OCT_file_list created!')
exit(0)


# create list of corresponding files
file_list = {'D0_before': [fn for fn in list_files_tiff if filter_D0_before(fn)],
             'D0_after': [fn for fn in list_files_tiff if filter_D0_after(fn)],
             'D0_after_PBS': [fn for fn in list_files_tiff if filter_D0_after_PBS(fn)],
             'D0': [fn for fn in list_files_tiff if filter_D0(fn)],
             'D3': [fn for fn in list_files_tiff if filter_D3(fn)],
             'D7': [fn for fn in list_files_tiff if filter_D7(fn)],
             'D7_PBS': [fn for fn in list_files_tiff if filter_D7_PBS(fn)],
             'D14': [fn for fn in list_files_tiff if filter_D14(fn)],
             'D14_PBS': [fn for fn in list_files_tiff if filter_D14_PBS(fn)],
             'D17': [fn for fn in list_files_tiff if filter_D17(fn)],
             'D21': [fn for fn in list_files_tiff if filter_D21(fn)]}

already_done = False
if not already_done:
    for k, v in file_list.items():
        print('List composed for: ' + k)
        with open(os.path.join('dataset_information', k+'.csv'), 'w') as result_file:
            for r in v:
                result_file.write(r + '\n')

    # Choose D0_before as healthy and D3 as pathological
    healthy_dataset = 'D0_before'
    pathological_dataset = 'D14'

    # Copy the images to project folder
    for f in tqdm(file_list[healthy_dataset]):
        # shutil.copy2(os.path.join(dataset_folder, f), os.path.join('data', 'healthy', f.split(os.sep)[-1]))
        im = Image.open(os.path.join(dataset_folder, f))
        im.save(os.path.join('input', healthy_dataset + '-' + pathological_dataset, 'originals', 'healthy', f.split(os.sep)[-1]).replace('.tif', '.png'))

    for f in tqdm(file_list[pathological_dataset]):
        # shutil.copy2(os.path.join(dataset_folder, f), os.path.join('data', 'pathological', f.split(os.sep)[-1]))
        im = Image.open(os.path.join(dataset_folder, f))
        im.save(os.path.join('input', healthy_dataset + '-' + pathological_dataset, 'originals', 'pathological', f.split(os.sep)[-1]).replace('.tif', '.png'))

# Copy Dx to folder
copy_dataset_to_folder = False
if copy_dataset_to_folder:

    target_dataset = 'D21'

    # create labels file
    with open(os.path.join('input', target_dataset, target_dataset + '.csv'), 'w') as labels_file:
        # Copy the images to project folder
        for f in tqdm(file_list[target_dataset]):
            # shutil.copy2(os.path.join(dataset_folder, f), os.path.join('input', target_dataset, f.split(os.sep)[-1]))
            im = Image.open(os.path.join(dataset_folder, f))
            im.save(os.path.join('input', target_dataset, f.split(os.sep)[-1]).replace('.tif', '.png'))
            labels_file.write(os.path.join(dataset_folder, f) + '\n')