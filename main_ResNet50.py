import glob
import pandas as pd
import numpy as np
import os
from keras.layers import *
from keras.applications.resnet50 import ResNet50, preprocess_input
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
import keras.callbacks
from keras.callbacks import ModelCheckpoint, EarlyStopping, LearningRateScheduler
from keras.models import model_from_json
from keras import backend as k
from keras.optimizers import SGD
import tensorflow as tf
from keras import optimizers
import scipy.ndimage as sc # This is for matrix interpolation
import json

from sklearn.model_selection import train_test_split
# from split_train_val_dataset import split_dataset_into_test_and_train_sets

# fix seed for reproducible results (only works on CPU, not GPU)
SEED = 9
np.random.seed(seed=SEED)
tf.set_random_seed(seed=SEED)

# hyper parameters for model

modelNameResults = 'ResNet50'   # At least image of size 197x197 px


based_model_last_block_layer_number = 153  # value is based on based model selected
batch_size = 64 # 256 0.45 0.86                            # try 4, 8, 16, 32, 64, 128, 256 depending on CPU/GPU memory capacity (powers of 2 values).
nb_classes = 2                             # number of classes

topModel = 2
num_epochs = 200
epochsToChangelr = 40
learn_rate = 1e-4                           # learning rate
newLearn_rate = 1e-5
momentum = .9                               # momentum to avoid local minimum

optimizer = SGD(lr=learn_rate, momentum=momentum)

transformation_ratio = .7                   # how aggressive will be the data augmentation/transformation
img_size = (299, 299)
img_width, img_height = img_size       # change based on the shape/structure of your images


# default paths
model_name =  modelNameResults + '_galahad.json'
model_weights = modelNameResults + '_Batch' + str(batch_size)  + '_weights.h5'


# def to_array(data):
#     arrays = []
#     labels = []
#
#     for i in data.index:
#
#         band_1 = np.array(data.loc[i].band_1).reshape(75, 75)
#         band_2 = np.array(data.loc[i].band_2).reshape(75, 75)
#         # resizing the images
#         band_1 = sc.zoom(band_1, factorIm, order=0)
#         band_2 = sc.zoom(band_2, factorIm, order=0)
#         band_3 = band_1 + band_2
#
#         band_1_scale = (band_1 - band_1.mean()) / (band_1.max() - band_1.min())
#         band_2_scale = (band_2 - band_2.mean()) / (band_2.max() - band_2.min())
#         band_3_scale = (band_3 - band_3.mean()) / (band_3.max() - band_3.min())
#
#         arrays.append(np.dstack((band_1_scale, band_2_scale, band_3_scale)))
#         if 'is_iceberg' in data:
#             labels.append(data.loc[i].is_iceberg)
#
#     return np.array(arrays), labels


def train(data_dir, model_path, results_dir):

    # Pre-Trained CNN Model. Using imagenet dataset to obtain the pre-trained weights
    base_model = ResNet50(input_shape=(img_width, img_height, 3), weights='imagenet', include_top=False)
    #base_model = VGG16(input_shape=(img_width, img_height, 3), weights='imagenet', include_top=False)


    # THESE ARE THE LAYERS WE ADD TO THE BASE MODEL

    if topModel == 1:
        # Top Model Block 1.
        x = base_model.output
        x = GlobalAveragePooling2D()(x)
        predictions = Dense(nb_classes, activation='sigmoid')(x)

    if topModel == 2:
        # Top Model Block 2
        x = base_model.output
        x = Flatten()(x)
        x = Dense(1024, activation='relu')(x)
        x = Dropout(0.3)(x)
        x = Dense(512, activation='relu')(x)
        x = Dropout(0.3)(x)
        predictions = Dense(nb_classes, activation='sigmoid')(x)


    # add top layer block to base model
    model = Model(base_model.input, predictions)
    #print(model.summary())


    # trainJson = pd.read_json(data_dir + 'train.json')
    #
    # train, labels = to_array(trainJson)
    # nb_train_samples = len(train)
    #
    # print('training samples:   ' + str(len(train[nb_validation_samples:,:,:,:])))
    # print('validation samples: ' + str(len(train[:nb_validation_samples,:,:,:])))
    # print('shape of training: ' + str(train[nb_validation_samples:,:,:,:].shape))
    # print('shape of validation: ' + str(train[:nb_validation_samples,:,:,:].shape))

    # Training images
    train_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        # rotation_range=40,
        # width_shift_range=0.2,
        # height_shift_range=0.2,
        # rescale=1./255,
        # shear_range=0.2,
        # horizontal_flip=True,
        # fill_mode='nearest'
    )

    train_generator = train_datagen.flow_from_directory(
        directory=data_dir + 'train',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )

    # Test images
    validation_datagen = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        # rescale=1. / 255
    )
    validation_generator = validation_datagen.flow_from_directory(
        directory=data_dir + 'val',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )

    # Here we defined the layers we want to use from the base model
    for layer in model.layers[:based_model_last_block_layer_number]:
        layer.trainable = False
    for layer in model.layers[based_model_last_block_layer_number:]:
        layer.trainable = True

    # compile the model with an optimizer and a very slow learning rate.
    model.compile(optimizer = optimizer,
                  loss = 'categorical_crossentropy',
                  metrics = ['accuracy'])

    # save weights of best training epoch: monitor can be either val_loss or val_acc
    final_weights_path = os.path.join(os.path.abspath(model_path), model_weights)


    # Change learning rate after some epoch. It is used in the callback lists (model.fit)
    def scheduler(epoch):
        if epoch == epochsToChangelr:
            k.set_value(model.optimizer.lr, newLearn_rate)
            print('             #############  CHANGING THE LEARNING RATE #############         ')
        return K.get_value(model.optimizer.lr)

    change_lr = LearningRateScheduler(scheduler)


    callbacks_list = [
        ModelCheckpoint(final_weights_path, monitor='val_acc', verbose=1, save_best_only=True),
        change_lr
        # EarlyStopping(monitor='val_loss', patience=10, verbose=0)

    ]


    print("fine-tuning model\n")

    # fine-tune the model
    history = model.fit_generator(train_generator,
                        steps_per_epoch = train_generator.n // batch_size,
                        epochs = num_epochs,
                        validation_data = validation_generator,
                        validation_steps = validation_generator.n // batch_size,
                        verbose=1,  # How to see the training process. Actually 1 is by default. We can delete this line.
                        callbacks = callbacks_list
                        )


    # Saving history
    data = np.transpose(history.history['acc'])
    header = ['Accuracy']
    accFrame = pd.DataFrame(data=data, columns=header) # data frame creation
    accFrame.to_csv(results_dir +  modelNameResults  +  '_Acc' + '.csv', sep=',') # saving the data frame in csv file

    data = np.transpose(history.history['val_acc'])
    header = ['Validation Accuracy']
    val_accFrame = pd.DataFrame(data=data, columns=header) # data frame creation
    val_accFrame.to_csv(results_dir  + modelNameResults + '_Val_acc'  + '.csv', sep=',')  # saving the data frame in csv file

    data = np.transpose(history.history['loss'])
    header = ['Loss']
    lossFrame = pd.DataFrame(data=data, columns=header) # data frame creation
    lossFrame.to_csv(results_dir + modelNameResults + '_Loss'   + '.csv', sep=',')  # saving the data frame in csv file

    data = np.transpose(history.history['val_loss'])
    header = ['Validation Loss']
    val_lossFrame = pd.DataFrame(data=data, columns=header) # data frame creation
    val_lossFrame.to_csv(results_dir + modelNameResults + '_Val_loss'  + '.csv', sep=',')  # saving the data frame in csv file


    # save model
    model_json = model.to_json()
    with open(os.path.join(os.path.abspath(model_path), model_name), 'w') as json_file:
        json_file.write(model_json)



def classify(trained_model_dir, data_dir, results_dir):

    print(' -----------------  Loading the model to classify test images   ---------------------')

    # load json and create model
    json_file = open(os.path.join(trained_model_dir, model_name), 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    model.load_weights(os.path.join(trained_model_dir, model_weights))

    testJson =  pd.read_json(data_dir + 'test.json')
    test,_  = to_array(testJson)

    # test data as generator
    test_datagen = ImageDataGenerator()
    test_generator = test_datagen.flow(test, batch_size = batch_size, shuffle = False )

    print(' -----------------          Classifing test images              ---------------------')

    # Calculate class probabilities (For iceberg and ship)
    y_probabilities = model.predict_generator(test_generator,
                                              steps = np.math.ceil(len(test) / float(batch_size))
                                              )

    id_image = testJson.id
    print('Number of test images: ' +  str(len(id_image)))

    filenameResults = results_dir + modelNameResults + '_results' + '_Batch' + str(batch_size) + '.csv'

    res = pd.DataFrame({'id': id_image, 'is_iceberg': y_probabilities.reshape((y_probabilities.shape[0]))})
    res.to_csv(filenameResults, index=False)



if __name__ == '__main__':

    data_dir = 'input/'
    model_dir = 'models/'
    results_dir = 'results/'

    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    if not os.path.exists(results_dir):
        os.makedirs(results_dir)


    train(data_dir, model_dir, results_dir)     # train model
    classify(model_dir, data_dir, results_dir)
    # release memory
    k.clear_session()


