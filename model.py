import csv
import numpy as np
import cv2

lines = []

#driving log for 1st lap
#driving log for 2nd lap

with open('../driving_log_2nd_lap.csv') as csvfile:
	reader = csv.reader(csvfile)
	for line in reader:
		lines.append(line)

images = []
measurements = []

#correction for center, left and right camera (0.3 for first track, 0.5 for second track)
corr = 0.5
corr_lst = [0, corr, -corr]

for line in lines:
	for pos in range(3):
		img_src = line[pos]
		fname = img_src.split('/')[-1]
		new_path = "../IMG_T2/" + fname
		image = cv2.imread(new_path)
		image.reshape((160, 320, 3))
		images.append(image)
		measurement = float(line[3]) + float(corr_lst[pos])
		measurements.append(measurement)
	cnt = cnt + 1

aug_images = []
aug_measurements = []

# augment the images by flipping them
for image, measurement in zip(images, measurements):
	aug_images.append(image)
	aug_measurements.append(measurement)
	aug_images.append(np.fliplr(image))
	aug_measurements.append(-1.0*measurement)

aug_images = aug_images
aug_measurements = aug_measurements

X_train = np.array(aug_images)
y_train = np.array(aug_measurements)

###################

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D, Dropout
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D

#simple LeNet architecture
model = Sequential()
model.add(Lambda(lambda x : x/255.0 - 0.5, input_shape = (160, 320, 3)))
model.add(Cropping2D(cropping=((50,35), (0,0)), input_shape=(3,160,320)))
model.add(Convolution2D(6, 5, 5, activation = 'relu'))
model.add(MaxPooling2D())
model.add(Convolution2D(6, 5, 5, activation = 'relu'))
model.add(MaxPooling2D())
model.add(Flatten())
model.add(Dense(120))
model.add(Dense(64))
model.add(Dense(1))
model.compile(loss = 'mse', optimizer = 'adam')
model.fit(X_train, y_train, validation_split = 0.1, shuffle = True, nb_epoch = 1) 

model.save('../model.h5')
exit()