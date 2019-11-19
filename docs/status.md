---
layout: default
title: Status
---

## Summary

The goal of our project was to generate 3D structures using a generative adversial network(GAN). Our AI "Alaina" will parse the input text for
keywords which will be used to identify the type of object being generated. After the type of object has been decided the appropriate pre-trained
model will be loaded and the generative model is inputted with random noise. The output of the generative model will be a 3D matrix consisting
of a probability for each value. The probabilities are rounded and the model is then rendered. 0's will be interpretted as an empty space while 1's will be interpretted as occupied space.

## Approach

We started by using a dataset of 3D objects (chairs) in the Object File Format (.off). The format is used for representing a geometric figure by specifying the surface polygons of the model. The format of a .off file is fairly simple: a list of all vertices, followed by a list of faces with the corresponding vertices. The .off objects were then converted to voxels using our own Python scripts. The scripts work by determing whether a voxel lies on a surface of the mesh. First the dimensions of the 3D mesh are scaled to fit within a 30x30x30 grid.
The surfaces of the mesh are then converted into voxels by checking whether nearby points overlap with the given surface. We can check whether they overlap by calculating the normal vector of the surface, and projecting the possible points onto this vector. If the magnitude of the projected vector is with a certain threshold this means the point exists on the same plane as the surface.
However, to check whether the point actually exists within the bounds of the surface we then calculate the barycentric coordinates of that points in relation to the surface. If all of the barycentrics coordinates are positive this means the point is within the bounds of the surface.
Here is are the equations used in these calculations:

![image1](Images/Barycentric_Points.PNG?raw=true)

If both of these conditions are true then a voxel is placed at the points. The output of the script is a 3D matrix with dimensions of 30x30x30; the matrix is binary encoded, meaning that the entries that are 0 signify an empty block and the entries that are 1 signify a cube.

GANs operate by learn through supervised learning. mean they need an existing dataset to train on. GANs are made up of two networks, generative and discriminative. The 2 networks are in competition constantly trying to outsmart the other. While the generator learns to create models that fool the discriminator, the discriminator gets better at spotting fakes.

The generator model is composed of several convolutional layers. It takes in a random noise vector as input, and outputs a 3D 30x30x30 matrix. It uses a the Adam optimizer to update the models parameters. The Adam optimizer is a form of stochastic gradient descent. The loss rate of the model is calculated using binary cross entropy which is defined by this equation:

![image1](Images/Binary_Cross_entropy.PNG?raw=true)

The discrimator model is composed of several transposed convolutional layers. It takes in a 30x30x30 matrix as input and output the probability of whether the input was fake. This model also use an Adam optimizer, as well as binary cross entropy to calculate loss.

## evaluation

We are currently opting for a more qualitative approach. We'd like to evaluate the generated structures by how seamlessly they pass the eye-test. We'd like to ask questions such as, 'Does the structure look at all abnormal?', 'Does the structure look like a first-party item or does it look tacked on?'

## remaining goals and challenges

- convert GAN-generated training data to be Malmo-friendly
- training is a potential challenge due to time required; might need to look into using Azure credits
- we may possibly expand the model domain to include stuff other than chairs

The main challenge for our group is the amount of time needed to train the GANs. (need epoch time from Brandon). One solution that we are planning to explore is executing training on Azure servers, but we have yet to ask the Professor for the credits.

After the GANs, we'll need to convert the generated training data into a Malmo-friendly format, but we don't anticipate this to be very challenging as the generated format is relatively straightforward (flattened binary matrix).

As for goals, we'd like to expand the model domain so that we can generate models other than chairs.

## resources used

- [TensorFlow](https://www.tensorflow.org)
- [details for .off file format](https://segeval.cs.princeton.edu/public/off_format.html)
- [binary cross-entropy](https://peltarion.com/knowledge-center/documentation/modeling-view/build-an-ai-model/loss-functions/binary-crossentropy) -[Determing Whether a point exists on a 3D triangular plane](https://math.stackexchange.com/questions/2582202/does-a-3d-point-lie-on-a-triangular-plane)
- [MNIST GANS](https://www.tensorflow.org/tutorials/generative/dcgan)
