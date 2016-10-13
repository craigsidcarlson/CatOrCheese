from keras.models import Sequential
from keras.preprocessing.image import ImageDataGenerator 
from keras.models import load_model
import numpy as np
import tempfile
import shutil
import sys

from modelCatOrCheese import makeModel

IMAGE_DIM = 375
batch_size = 32
classes=['cat', 'cheese']

savedModel = "models/topdog/my_model.h5"

def normalizeImage(image_dir):
	#Normalize RGB
	imageDataGen = ImageDataGenerator(rescale=1./255)
	#Convert to correct image size
	normalizedImageData = imageDataGen.flow_from_directory(
		image_dir,
		target_size=(IMAGE_DIM,IMAGE_DIM),
		color_mode="rgb",
		batch_size=batch_size,
		class_mode=None,
		shuffle=False)
	return normalizedImageData


def predict(norm_image_data):
	model = load_model(savedModel)
	prediction = model.predict_generator(norm_image_data, norm_image_data.N)
	return prediction



if __name__ == '__main__':
	#Get file to analyze and predict
	image = sys.argv[1]

	#Create tmp dir structure needed for >=1 images(Can analyze n images)
	highlevel = tempfile.mkdtemp()
	lowlevel = tempfile.mkdtemp(dir=highlevel)

	#Copy image into tiered tmp dir
	shutil.copy(image, lowlevel+"/")

	#Normalize and generate image data
	norm_image_data = normalizeImage(highlevel)

	#Become Magician
	prediction = predict(norm_image_data)

	#remove tmp hierarchy
	shutil.rmtree(highlevel)

	#Strut your stuff
	print(classes[np.argmax(prediction)])