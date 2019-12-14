from __future__ import print_function
from builtins import range
import MalmoPython
import os
import sys
import time
import numpy as np
import random
import tensorflow as tf
import glob
import matplotlib.pyplot as plt
import numpy as np
import os
from tensorflow.keras import layers
import time
from keras import backend
from keras.constraints import Constraint
from voxels import *

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
	

def generate_chair():
	# Notice `training` is set to False.
	# This is so all layers run in inference mode (batchnorm).
	predictions = np.array(generator(seed, training=False))
	vox = predictions.reshape(30,30,30).round()
	return vox


noise_dim = 100
num_examples_to_generate = 1

seed = tf.random.normal([num_examples_to_generate, noise_dim])

generator = make_generator_model()
generator.compile(loss=wasserstein_loss, optimizer=tf.keras.optimizers.RMSprop(lr=0.00005))
discriminator = make_discriminator_model()
discriminator.compile(loss=wasserstein_loss, optimizer=tf.keras.optimizers.RMSprop(lr=0.00005))

  
checkpoint_dir = './training_checkpoints_chair'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt")
checkpoint = tf.train.Checkpoint(generator=generator,
                                 discriminator=discriminator)
  
checkpoint.restore(tf.train.latest_checkpoint(checkpoint_dir))


if sys.version_info[0] == 2:
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
    import functools
    print = functools.partial(print, flush=True)

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print('ERROR:', e)
    print(agent_host.getUsage())
    exit(1)
if agent_host.receivedArgument("help"):
    print(agent_host.getUsage())
    exit(0)


def createBlock(x, y, z, blockType="air"):
    return '<DrawBlock x="' + str(x) + '" y="' + str(y) + '" z="' + str(z) + '" type="' + blockType + '"/>'


def createCuboid(x1, y1, z1, x2, y2, z2, blockType="wool"):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(
        y2) + '" z2="' + str(z2) + '" type="' + blockType + '"/>'


def renderObject(x, y, z, object):
    # (x, y, z) is the left-bottom corner of the object bounding box
    # +x: east(forward)  +z: east(right)  +y: height(up)
    genstring = createCuboid(x, y, z, x + 29, y + 29, z + 29)
    index = np.argwhere(object == 0)
    for coordinate in index:
        genstring += createBlock(x + coordinate[1], y + coordinate[2], z + coordinate[0]) + "\n"
    return genstring


def renderObjects(objects, originX=30, originY=4, originZ=0):
    genstring = ''
    for j in range(len(objects)):
        genstring += renderObject(originX, originY, originZ + j * 35, objects[j]) + "\n"
    return genstring


objects = []
for i in range(3):
    objects.append(generate_chair())
    # objects.append(np.reshape(np.ones(12), (2, 2, 3)))

missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>Alaina: Let's generate our objects!</Summary>
              </About>

              <ServerSection>
                <ServerInitialConditions>
                   <Time>
                    <StartTime>12000</StartTime>
                    <AllowPassageOfTime>false</AllowPassageOfTime>
                   </Time>
                </ServerInitialConditions>
                <ServerHandlers>
                  <FlatWorldGenerator generatorString="1;7,2x3,5;1" forceReset="true"/>
                  <DrawingDecorator>''' + renderObjects(objects) + '''</DrawingDecorator>
                  <ServerQuitFromTimeUp timeLimitMs="1000"/>
                  <ServerQuitWhenAnyAgentFinishes/>
                </ServerHandlers>
              </ServerSection>

              <AgentSection mode="Creative">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="4.0" z="0.5" yaw="-90"/>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

print(missionXML)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()
my_client_pool = MalmoPython.ClientPool()
my_client_pool.add(MalmoPython.ClientInfo("127.0.0.1", 10000))
print(my_mission.getAsXML(True))
# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        # agent_host.startMission(my_mission, my_mission_record)
        agent_host.startMission(my_mission, my_client_pool, my_mission_record, 0, "0")
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission:",e)
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:", error.text)

print()
print("Mission running ", end=' ')

# Loop until mission ends:
while world_state.is_mission_running:
    print(".", end="")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print("Error:", error.text)

print()
print("Mission ended")
# Mission has ended.
