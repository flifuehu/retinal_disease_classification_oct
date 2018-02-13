import os
import glob
import shutil
from tqdm import tqdm
import numpy as np
from sklearn.model_selection import train_test_split
from PIL import Image

SEED = 9

dataset_name = 'D0_before-D14'
extension = '.png'
convert = False
extension_to = '.png'

data_dir = 'input/' + dataset_name + '/originals/'
train_dir = 'input/' + dataset_name + '/train/'
test_dir = 'input/' + dataset_name + '/test/'
# val_dir = 'input/' + dataset_name + '/val/'

CLASSES = [
    'pathological',
    'healthy'
]

N_CLASSES = len(CLASSES)

def get_class(class_name):
    if class_name in CLASSES:
        class_idx = CLASSES.index(class_name)
    else:
        assert False
    assert class_idx in range(N_CLASSES)
    return class_idx


def print_distribution(ids, classes=None):
    if classes is None:
        classes = [get_class(idx.split('/')[-2]) for idx in ids]
    classes_count = np.bincount(classes)
    for class_name, class_count in zip(CLASSES, classes_count):
        print('{:>22}: {:5d} ({:04.1f}%)'.format(class_name, class_count, 100. * class_count / len(classes)))


# create needed folders
if not os.path.exists(train_dir):
    os.makedirs(train_dir)
for c in CLASSES:
    if not os.path.exists(os.path.join(train_dir, c)):
        os.makedirs(os.path.join(train_dir, c))
if not os.path.exists(test_dir):
    os.makedirs(test_dir)
# for c in CLASSES:
#     if not os.path.exists(os.path.join(test_dir, c)):
#         os.makedirs(os.path.join(test_dir, c))
# if not os.path.exists(val_dir):
#     os.makedirs(val_dir)
# for c in CLASSES:
#     if not os.path.exists(os.path.join(val_dir, c)):
#         os.makedirs(os.path.join(val_dir, c))

# list all files in the dataset
file_list = glob.glob(os.path.join(data_dir, '*/*' + extension))

# split in train and test
gt_train_test = [s.find('healthy') != -1 for s in file_list]
files_train, files_test = train_test_split(file_list, test_size=0.3, random_state=SEED, stratify=gt_train_test)

# split in val and test
gt_train_val = [s.find('healthy') != -1 for s in files_test]
files_test, files_val = train_test_split(files_test, test_size=0.2, random_state=SEED, stratify=gt_train_val)

print("Training set distribution:")
print_distribution(files_train)

# print("Validation set distribution:")
# print_distribution(files_val)

print("Testing set distribution:")
print_distribution(files_test)


# copy training images
for file_name in tqdm(files_train):
    if not convert:
        shutil.copy2(file_name, os.path.join(train_dir, os.sep.join(file_name.split(os.sep)[-2:])))
    else:
        im = Image.open(file_name)
        im.save(os.path.join(train_dir, os.sep.join(file_name.split(os.sep)[-2:]).replace(extension, extension_to)))

# copy val images
# for file_name in tqdm(files_val):
#     if not convert:
#         shutil.copy2(file_name, os.path.join(val_dir, os.sep.join(file_name.split(os.sep)[-2:])))
#     else:
#         im = Image.open(file_name)
#         im.save(os.path.join(val_dir, os.sep.join(file_name.split(os.sep)[-2:]).replace(extension, extension_to)))

# copy test images
with open(os.path.join(test_dir, 'test_labels.csv'), 'w') as labels_file:
    for file_name in tqdm(files_test):

        # save test labels
        img_name = str(file_name.split(os.sep)[-1:][0])
        img_class = str(file_name.split(os.sep)[-2:-1][0])
        labels_file.write(img_name + ',' + img_class + '\n')

        # copy to folder structure
        if not convert:
            shutil.copy2(file_name, os.path.join(test_dir, os.sep.join(file_name.split(os.sep)[-1:])))
        else:
            im = Image.open(file_name)
            im.save(os.path.join(test_dir, os.sep.join(file_name.split(os.sep)[-1:]).replace(extension, extension_to)))
