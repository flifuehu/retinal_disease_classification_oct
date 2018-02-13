import os
import csv
import numpy as np
from sklearn.model_selection import train_test_split



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


def get_class(class_name, CLASSES):
    if class_name in CLASSES:
        class_idx = CLASSES.index(class_name)
    else:
        assert False
    assert class_idx in range(len(CLASSES))
    return class_idx


def print_distribution(ids, CLASSES, classes=None):
    if classes is None:
        classes = [get_class(idx.split('/')[-2], CLASSES) for idx in ids]
    classes_count = np.bincount(classes)
    for class_name, class_count in zip(CLASSES, classes_count):
        print('{:>22}: {:5d} ({:04.1f}%)'.format(class_name, class_count, 100. * class_count / len(classes)))


def return_train_and_test_set(DATASET, PATTERNS_EXCLUDED_TRAINING, SEED=7, test_pcnt=0.3):

    CLASSES = [k for k in DATASET.keys()]
    N_CLASSES = len(CLASSES)

    # file structure for files
    file_list_all = []
    for cl in CLASSES:
        # read class=cl files
        for fh in DATASET[cl]:
            with open(fh, 'r') as fp:
                reader = csv.reader(fp)
                for row in reader:
                    file_list_all.append([cl, row[0]])

    # remove only-test instances
    fl_excluded = list(filter(lambda s: string_complies_with(s[1], PATTERNS_EXCLUDED_TRAINING), file_list_all))
    fl_wo_excluded = [list(x) for x in set(tuple(x) for x in file_list_all).difference(tuple(y) for y in fl_excluded)]
    n_fl_only_test = len(fl_excluded)
    n_fl = len(file_list_all)
    current_test_pcnt = n_fl_only_test / n_fl

    remaining_test_size = test_pcnt - current_test_pcnt
    if remaining_test_size < 0:
        files_train, files_test = fl_wo_excluded, fl_excluded
        print('Attention! Leaving {0} experiments out implies a test % of {1:.2f}, greater than the desired {2:.2f}'
              .format(*PATTERNS_EXCLUDED_TRAINING, current_test_pcnt, test_pcnt))
    else:
        # get some more test files until test_pcnt is met
        gts = [s[0].find('healthy') != -1 for s in fl_wo_excluded]
        files_train, files_test = train_test_split(fl_wo_excluded, test_size=remaining_test_size, random_state=SEED, stratify=gts)

        # add exclusive-test
        for fl in fl_excluded:
            files_test.append(fl)

    files_test.sort()
    files_train.sort()

    print("Training set distribution:")
    print_distribution([f[0] + '/' + f[1].split(os.sep)[-1] for f in files_train], CLASSES)

    print("Test set distribution:")
    print_distribution([f[0] + '/' + f[1].split(os.sep)[-1] for f in files_test], CLASSES)

    final_test_pcnt = len(files_test) / n_fl

    return files_train, files_test, final_test_pcnt


# SEED = 7
# test_pcnt = 0.3
# DATASET = {'healthy': ['/home/felix/Scratch/projects/galahad/dataset_information/D0_before.csv',
#                        '/home/felix/Scratch/projects/galahad/dataset_information/D14_PBS.csv'],
#            'pathological': ['/home/felix/Scratch/projects/galahad/dataset_information/D14.csv']}
# PATTERNS_EXCLUDED_TRAINING = [
#     'C-2'
# ]
#
# files_train, files_test = return_train_and_test_set(DATASET, PATTERNS_EXCLUDED_TRAINING, SEED, test_pcnt)
# print('Done!')