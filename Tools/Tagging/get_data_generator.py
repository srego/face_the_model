'''
This class creaters a generator to feed in training and test data to face_the_model.
This code is based on https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly.html
'''

import numpy as np
import keras
# import imageio # Added 
import cv2
from keras.preprocessing.image import img_to_array

import random

'''
?list_IDs is a dict of the names of the image files.
lables is a dict of the label of the image files (paul or not paul -- make binary)
'''

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, labels, batch_size=32, dim=(64,64), n_channels=3,
                 n_classes=2, shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.labels = labels
        self.list_IDs = list_IDs
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.on_epoch_end()

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.list_IDs) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index * self.batch_size: (index+1) * self.batch_size]

        # Find list of IDs
        list_IDs_temp = [self.list_IDs[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(list_IDs_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.list_IDs))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, list_IDs_temp):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        X = np.empty((self.batch_size, *self.dim, self.n_channels))  # we're setting the dimensions to (32, 32, 32, 1)
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        for i, ID in enumerate(list_IDs_temp):
            # Store sample


            # X[i,] = np.load('data/' + ID + '.npy') ORIGINAL
            # X[i,] = imageio.imread(ID) FAILED ATTEMPT
            image = cv2.imread(ID)
            image = cv2.resize(image, (64, 64))
            X[i,] = img_to_array(image)  # (32, 32, 32, 1) <- (64, 64, 3)

            # Store class
            y[i] = self.labels[ID]
            # y[i] = random.randint(0, 1) #change when mdict is made

        return X, y #keras.utils.to_categorical(y, num_classes=self.n_classes)