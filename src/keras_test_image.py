from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras import backend as K
from keras.models import load_model
from scipy import misc
import os

# dimensions of our images.
img_width, img_height = 80, 80
batch_size = 1

validation_data_dir = './test'

model = load_model('my_model.h5')
model.load_weights('first_try.h5', by_name=True)

datagen = ImageDataGenerator(rescale=1. / 255)

img = misc.imread('./data/train/positive/1010.png')

os.system('clear')

x = img[None, :80, :80, :3]

for batch in datagen.flow(x, batch_size=1):
    print model.predict_on_batch(batch)
    break
