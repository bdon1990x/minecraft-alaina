from voxels import *

import tensorflow as tf
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras import layers
import time
from keras import backend
from keras.constraints import Constraint

train_models = []
for filename in os.listdir('dataset/table/'):
    v = loadVoxels(os.getcwd() + '/dataset/table/' + filename)
    train_models.append(v)
    print(filename)
train_models = np.array(train_models)
train_labels = np.ones(train_models.shape[0])
print(train_models.shape)
print(train_labels.shape)

BUFFER_SIZE = train_models.shape[0] 
BATCH_SIZE = 32

train_models = train_models.reshape(train_models.shape[0], 30, 30, 30, 1).astype('float32')

def get_batch():
    idx = np.random.randint(BUFFER_SIZE, size=BATCH_SIZE)
    return train_models[idx]

# implementation of wasserstein loss
def wasserstein_loss(y_true, y_pred):
    return backend.mean(y_true * y_pred)
	

# clip model weights to a given hypercube
class ClipConstraint(Constraint):
	# set clip value when initialized
	def __init__(self, clip_value):
		self.clip_value = clip_value

	# clip model weights to hypercube
	def __call__(self, weights):
		return backend.clip(weights, -self.clip_value, self.clip_value)

	# get the config
	def get_config(self):
		return {'clip_value': self.clip_value}
		
def make_generator_model():
    const = ClipConstraint(0.01)

    model = tf.keras.Sequential()
    model.add(layers.Dense(5*5*5*256, use_bias=False, input_shape=(100,)))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Reshape((5, 5,5, 256)))
    assert model.output_shape == (None, 5, 5,5, 256) # Note: None is the batch size

    model.add(layers.Conv3DTranspose(128, (5, 5, 5), strides=(1, 1, 1), padding='same', use_bias=False))
    assert model.output_shape == (None, 5, 5,5, 128)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv3DTranspose(64, (5, 5, 5), strides=(3, 3, 3), padding='same', use_bias=False))
    assert model.output_shape == (None, 15, 15,15, 64)
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())

    model.add(layers.Conv3DTranspose(1, (5, 5, 5), strides=(2, 2, 2), padding='same', use_bias=False, activation='sigmoid'))
    assert model.output_shape == (None, 30, 30, 30, 1)

    return model
	
def make_discriminator_model():
    model = tf.keras.Sequential()
    model.add(layers.Conv3D(64, (5, 5, 5), strides=(2, 2, 2), padding='same',
                                     input_shape=[30, 30, 30, 1]))
    model.add(layers.BatchNormalization())
    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Conv3D(128, (5, 5, 5), strides=(2, 2, 2), padding='same'))
    model.add(layers.BatchNormalization())

    model.add(layers.LeakyReLU())
    model.add(layers.Dropout(0.3))

    model.add(layers.Flatten())
    model.add(layers.Dense(1))

    return model
	
def define_gan(generator, critic):
    # make weights in the critic not trainable
    critic.trainable = False
    # connect them
    model = tf.keras.Sequential()
    # add generator
    model.add(generator)
    # add the critic
    model.add(critic)
    # compile model
    opt = tf.keras.optimizers.RMSprop(lr=0.00005)
    model.compile(loss=wasserstein_loss, optimizer=opt)
    return model

def generate_and_save_images(model, test_input):
	# Notice `training` is set to False.
	# This is so all layers run in inference mode (batchnorm).
	predictions = np.array(model(test_input, training=False))
	vox = predictions.reshape(30,30,30).round()
	plotVoxels(vox, 'chair')

def train(epochs):
  loss = open('loss/table_loss.txt', 'w')
  loss.write('epoch,real,fake,generator\n')
  for epoch in range(epochs):
    start = time.time()
    
    avg_g_loss = 0
    avg_d_loss = 0
    count = 0
    generate_and_save_images(generator,seed)
    for b in range(16):
        for i in range(10):
            image_batch = get_batch()
            noise = tf.random.normal([image_batch.shape[0], noise_dim])
            generated_images = generator(noise, training=True)
            real_loss = discriminator.train_on_batch(image_batch, -np.ones((BATCH_SIZE, 1)))
            fake_loss = discriminator.train_on_batch(generated_images, np.ones((BATCH_SIZE, 1)))
        noise = tf.random.normal([BATCH_SIZE, noise_dim])
        gen_loss = wgan.train_on_batch(noise, -np.ones((BATCH_SIZE, 1)))
        s = "{}: {},{},{}"
        s = s.format(epoch, real_loss,fake_loss, gen_loss)
        loss.write(s+'\n')
        print(s)
        loss.close()
        loss = open('loss/ctable_loss.txt', 'a')
    checkpoint.save(file_prefix = checkpoint_prefix)


EPOCHS = 1000
noise_dim = 100
num_examples_to_generate = 1

# We will reuse this seed overtime (so it's easier)
# to visualize progress in the animated GIF)
seed = tf.random.normal([num_examples_to_generate, noise_dim])

generator = make_generator_model()
generator.compile(loss=wasserstein_loss, optimizer=tf.keras.optimizers.RMSprop(lr=0.00005))
discriminator = make_discriminator_model()
discriminator.compile(loss=wasserstein_loss, optimizer=tf.keras.optimizers.RMSprop(lr=0.00005))

  
checkpoint_dir = './training_checkpoints_table'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator=generator,
                                 discriminator=discriminator)
  
checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))

wgan = define_gan(generator,discriminator)
train(EPOCHS)
