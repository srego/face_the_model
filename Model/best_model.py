'''
Best performing version of Face the Model (May, 2018).

This code was guided an inspired by Super Data Science's
Deep Learning Udemy course (https://www.udemy.com/deeplearning/).

Model structure
4 convolutional layers before flatenning.
4 layers after faltenning with dropout.

Data structure
1,585 train images per class (Paul; actors & actresses)
1,000 test images per class (Paul; actors & actresses)
'''


from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from keras.optimizers import Adam
from keras.preprocessing.image import ImageDataGenerator


# Set global variables
img_width = 256
img_height = 256
input_shape = (img_width, img_height, 3)
batch_size = 32
epochs = 50
dropout_rate = 0.6


# Convolutional Neural Network
model = Sequential()

# Convolution Layer 1
model.add(Conv2D(32, (3, 3), padding='same', input_shape=input_shape, activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Convolution Layer 2
model.add(Conv2D(32, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Convolution Layer 3
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Convolution Layer 4
model.add(Conv2D(64, (3, 3), padding='same', activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

# Flatten CNN
model.add(Flatten())


# Fully Connected Artificial Neural Network
# Layer (with Dropout) 1
model.add(Dense(64, activation='relu'))
model.add(Dropout(dropout_rate))

# Layer 2
model.add(Dense(64, activation='relu'))

# Layer (with Dropout) 3
model.add(Dense(64, activation='relu'))
model.add(Dropout(dropout_rate/2))

# Final Layer 
model.add(Dense(1, activation='sigmoid'))

# Compile Model 
model.compile(optimizer=Adam(lr=1e-3), 
              loss='binary_crossentropy', 
              metrics=['accuracy'])


# Handle Image Data
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255)

training_set = train_datagen.flow_from_directory('/home/ubuntu/h_hour/test_1/train',
                                                 target_size = (img_width, img_height),
                                                 batch_size = batch_size,
                                                 class_mode = 'binary')

test_set = test_datagen.flow_from_directory('/home/ubuntu/h_hour/test_1/test',
                                            target_size = (img_width, img_height),
                                            batch_size = batch_size,
                                            class_mode = 'binary')


# Fit the model
model.fit_generator(training_set,
                    epochs = epochs,
                    steps_per_epoch=3170//batch_size,
                    validation_data = test_set,
                    validation_steps = 2000//batch_size,
                    workers=12,
                    max_q_size=100)


# Save the model
model.save('/home/ubuntu/h_hour/test_1/test_1.h5')