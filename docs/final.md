---
layout: default
title: Status
---

## Video

## Summary

The goal of our project was to generate 3D structures using a generative adversial network(GAN). After the type of object has been decided the appropriate pre-trained
model will be loaded and the generative model is inputted with random noise. The output of the generative model will be a 3D matrix consisting
of a probability for each value. The probabilities are rounded such that 0's will be interpretted as an empty space while 1's will be interpretted as occupied space. Lastly the 3D matrices are rendered into minecraft in a 30x30 area.

## Approach

We started by using a dataset of 3D objects (chairs) in the Object File Format (.off). The format is used for representing a geometric figure by specifying the surface polygons of the model. The format of a .off file is fairly simple: a list of all vertices, followed by a list of faces with the corresponding vertices. The .off objects were then converted to voxels using our own Python scripts. The scripts work by determing whether a voxel lies on a surface of the mesh. First the dimensions of the 3D mesh are scaled to fit within a 30x30x30 grid.  
The surfaces of the mesh are then converted into voxels by checking whether nearby points overlap with the given surface. We can check whether they overlap by calculating the normal vector of the surface, and projecting the possible points onto this vector. If the magnitude of the projected vector is with a certain threshold this means the point exists on the same plane as the surface.  
However, to check whether the point actually exists within the bounds of the surface we then calculate the barycentric coordinates of that points in relation to the surface. If all of the barycentrics coordinates are positive this means the point is within the bounds of the surface.  
Here is are the equations used in these calculations:

![image1](Images/Barycentric_Points.PNG?raw=true)

If both of these conditions are true then a voxel is placed at the points. The output of the script is a 3D matrix with dimensions of 30x30x30; the matrix is binary encoded, meaning that the entries that are 0 signify an empty block and the entries that are 1 signify a cube.

The model we use is a Wasserstein generative adversial netowrk (WGAN). We found this model provided us with better quality generations as compared to when we used a normal GAN model in our status report. The WGAN differes from a normal GAN in several ways. Firstly, it utilizes a Wasserstein loss function where as previously we used binary cross entropy. Wasserstein loss is defined using this function:

![image1](Images/Wasserstein_Loss.PNG?raw=true)

## Evaluation

In terms of qualitative evaluations, we would like to evaluate the generated structures by how seamlessly they pass the eye-test. We'd like to ask questions such as, 'Does the structure look at all abnormal?', 'Does it resemble the desired item?', or 'Is the object structurally sound?'

As for quantitative evualuations we will look at the training time of model.

Here is an example of a chair we have generated with our current model:  
![image1](Images/Status_Chair.png?raw=true)  
From this image we can see that the chair is starting to take form, but it obviously missing some features, as well as generally being very noisy.

## Remaining Goals and Challenges

Our goals are for the future include further refinining our training model to achieve better looking results, and expanding the versality of our model to handle multiple types of objects besides just chairs. Lastly if time permits we want to implement text commands, which will generate an item depends on a text input.

A possible challenge we may have is that there is too much variation in our dataset. In particular chairs have extreme variations in form. For example, some may be round, some are rectangular, some have legs, some have wheels, etc... This could potentially be overcome by increasing training time.

## Resources Used

- [TensorFlow](https://www.tensorflow.org)
- [details for .off file format](https://segeval.cs.princeton.edu/public/off_format.html)
- [binary cross-entropy](https://peltarion.com/knowledge-center/documentation/modeling-view/build-an-ai-model/loss-functions/binary-crossentropy)
- [Determing Whether a point exists on a 3D triangular plane](https://math.stackexchange.com/questions/2582202/does-a-3d-point-lie-on-a-triangular-plane)
- [MNIST GANS](https://www.tensorflow.org/tutorials/generative/dcgan)
- [ModelNet Dataset](https://modelnet.cs.princeton.edu/)
- [GAN - Wasserstein Gan and WGAN-GP](https://medium.com/@jonathan_hui/gan-wasserstein-gan-wgan-gp-6a1a2aa1b490)
- [How to Develop a WGAN](https://machinelearningmastery.com/how-to-code-a-wasserstein-generative-adversarial-network-wgan-from-scratch/)