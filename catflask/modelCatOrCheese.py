#THEANO_FLAGS=device=gpu,floatX=float32 python modelCatOrCheese.py

from keras.preprocessing.image import ImageDataGenerator 
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D
from keras.optimizers import SGD, Adam, RMSprop
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
import os
import sys
#Here are all of the subtyes
#Init impl will be CatOrCheese
# abyssinian# angora# bermese# egyptain# persian# siamese# tabby# tiger# tortoiseShell# blue# brie# camembert# gouda# mozzarella# ricotta# swiss


classes=['cat', 'cheese']
nb_classes = len(classes)
testDirName = '../data/generic/test'
trainDirName = '../data/generic/train'
SEED = 1
#the images seemed to be 375x375 ish....sooo im cropping everthing to that size
IMAGE = 375
#rgb
COLOR_DIM = 3
#Most that 16 gigs can handle
batch_size = 32
#How many times to look at the images
nb_epoch = 1
#size of the convolution kernal
conv_kernal_size = 3

def getData():
	if not os.path.isdir(testDirName):
		raise Exception('Test dir does not exist')
	if not os.path.isdir(trainDirName):
		raise Exception('Train dir does not exist')

	train_datagen = ImageDataGenerator(rescale=1./255, horizontal_flip=True, zoom_range=0.2)

	test_datagen = ImageDataGenerator(rescale=1./255)

	train = train_datagen.flow_from_directory(
		trainDirName,
		target_size=(IMAGE,IMAGE),
		color_mode="rgb",
		classes=classes,
		batch_size=batch_size,
		class_mode="categorical",
		shuffle=True)

	test = test_datagen.flow_from_directory(
		testDirName,
		target_size=(IMAGE,IMAGE),
		color_mode="rgb",
		classes=classes,
		batch_size=batch_size,
		class_mode="categorical",
		shuffle=True)
	return train, test

def makeModel():
	model = Sequential()

	model.add(Convolution2D(32, conv_kernal_size, conv_kernal_size, input_shape=(COLOR_DIM, IMAGE, IMAGE)))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Convolution2D(32, conv_kernal_size, conv_kernal_size))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))


	model.add(Convolution2D(64, conv_kernal_size, conv_kernal_size))
	model.add(Activation('relu'))
	model.add(MaxPooling2D(pool_size=(2, 2)))

	model.add(Flatten())
	model.add(Dense(64))
	model.add(Activation('relu'))
	model.add(Dropout(0.5))
	model.add(Dense(nb_classes))
	model.add(Activation('sigmoid'))
	###
	rmsprop =RMSprop()

	model.compile(loss='categorical_crossentropy', optimizer=rmsprop, metrics=['accuracy'])

	return model


def trainModel(train, test):
	model.fit_generator(train, samples_per_epoch = train.N, nb_epoch=nb_epoch, validation_data=test, nb_val_samples=test.N, nb_worker=1)
	model.save('my_model.h5')
	model.save_weights('my_model_weights.h5')
	print(model.summary())


if __name__ == '__main__':
	train, test = getData()
	model = makeModel()
	trainModel(train, test)
