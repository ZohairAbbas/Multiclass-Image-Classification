# -*- coding: utf-8 -*-
"""Multiclass Image Classification.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QieBBqdmodlaxoGouDxahWLhrj542FQZ

**Mounting Drive**
"""

# Commented out IPython magic to ensure Python compatibility.
try:
    from google.colab import drive
    drive.mount('/content/drive', force_remount=True)
    COLAB = True
    print("Note: using Google CoLab")
#     %tensorflow_version 2.x
except:
    print("Note: not using Google CoLab")
    COLAB = False

"""
**Training Directory**"""

DATADIR = "/content/drive/My Drive/Colab Notebooks/Fruits_Train"
CATEGORIES = ["1-Tomato 3", "2-Tomato 4", "3-Tomato Cherry Red", "4-Tomato Maroon", "5-Tomato Yellow", "6-Walnut"]

"""**Necessary Imports**"""

import matplotlib.pyplot as plt
import os
import cv2
import numpy as np
import random
import csv

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.utils import  normalize, to_categorical
from sklearn.model_selection import train_test_split

"""
**Creating Training Data**"""

training_data = []
IMG_SIZE = 50
def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)
        class_num = CATEGORIES.index(category)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img), cv2.IMREAD_UNCHANGED)
                img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
                new_array = cv2.resize(img_rgb, (IMG_SIZE, IMG_SIZE))
                training_data.append([new_array,class_num])
            except Exception as e:
                pass

create_training_data()
print(len(training_data))

"""


**Seperating Pics and Labels**"""

random.shuffle(training_data)

X=[]
Y=[]
for features, label in training_data:
    X.append(features)
    Y.append(label)

X = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE,3)
Y = np.array(Y)
X = normalize(X, axis=1)
Y = to_categorical(Y)

"""**Spliting Data**"""

x_train, x_test, y_train, y_test = train_test_split(    
    X, Y, test_size=0.2, random_state=42)
print("X.shape=",X.shape)
print("x_train.shape=",x_train.shape)
print("y_train.shape=",y_train.shape)
print("x_test.shape=",x_test.shape)
print("y_test.shape=",y_test.shape)

"""**Model**"""

model1 = Sequential()

model1.add(Conv2D(32, (3,3) ,input_shape=X.shape[1:], activation="relu"))
model1.add(Conv2D(32, (3,3) ,input_shape=X.shape[1:], activation="relu"))
model1.add(MaxPooling2D(pool_size=(2,2)))

model1.add(Conv2D(64,(3,3), activation="relu"))
model1.add(Conv2D(64,(3,3), activation="relu"))
model1.add(MaxPooling2D(pool_size=(2,2)))

model1.add(Conv2D(128,(3,3), activation="relu"))
model1.add(Conv2D(128,(3,3), activation="relu"))
model1.add(MaxPooling2D(pool_size=(2,2)))

model1.add(Dropout(0.2))
model1.add(Flatten())
model1.add(Dense(256))

model1.add(Dense(6, activation="softmax"))

# model1.summary()

model1.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

history = model1.fit(x_train, y_train, batch_size=64, epochs=20, validation_data=(x_test,y_test), verbose=2)

"""**Accuracy and Loss curves**"""

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']
loss = history.history['loss']
val_loss = history.history['val_loss']

epochs = range(len(acc))

plt.plot(epochs, acc, 'b', label='Training acc')
plt.plot(epochs, val_acc, 'r', label='Validation acc')
plt.title('Training accuracy')
plt.legend()

plt.figure()

plt.plot(epochs, loss, 'b', label='Training loss')
plt.plot(epochs, val_loss, 'r', label='Validation loss')
plt.title('Training loss')
plt.legend()

plt.show()

"""**Testing Performance**"""

predict = model1.predict(x_test)

# Used for checking the accuracy of the model

for i in range(0,10):
  plt.title("Predicted {}".format(np.argmax(predict[i], axis=-1)))
  plt.xlabel("Actual {}".format(np.argmax(y_test[i], axis=-1)), fontsize=12)
  plt.imshow(x_test[i].reshape(IMG_SIZE, IMG_SIZE, 3))
  plt.show()

"""**Testing Directory**"""

TESTDIR = "/content/drive/My Drive/Colab Notebooks/fruits-test"

"""**Creating Testing Data**"""

testing_data = []
IMG_SIZE = 50
def create_testing_data():
      for img in os.listdir(TESTDIR):
          try:
              img_array2 = cv2.imread(os.path.join(TESTDIR,img), cv2.IMREAD_UNCHANGED)
              img_rgb2 = cv2.cvtColor(img_array2, cv2.COLOR_BGR2RGB)
              new_array2 = cv2.resize(img_rgb2, (IMG_SIZE, IMG_SIZE))
              testing_data.append(new_array2)
          except Exception as e:
              pass

create_testing_data()
print(len(testing_data))

X1 = np.array(testing_data).reshape(-1, IMG_SIZE, IMG_SIZE,3)
X1 = normalize(X1, axis=1)

"""**Testing model on the final testing data**"""

predict1 = model1.predict(X1)

# Used for checking the accuracy of the model on the newly imported testing data

for i in range(0,10):
  plt.title("Predicted {}".format(np.argmax(predict1[i], axis=-1)))
  plt.imshow(X1[i].reshape(IMG_SIZE, IMG_SIZE, 3))
  plt.show()