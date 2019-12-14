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

We started by using a dataset of 3D objects (chairs and tables) in the Object File Format (.off). The format is used for representing a geometric figure by specifying the surface polygons of the model. The format of a .off file is fairly simple: a list of all vertices, followed by a list of faces with the corresponding vertices. The .off objects were then converted to voxels using our own Python scripts. The scripts work by determing whether a voxel lies on a surface of the mesh. First the dimensions of the 3D mesh are scaled to fit within a 30x30x30 grid.  
The surfaces of the mesh are then converted into voxels by checking whether nearby points overlap with the given surface. We can check whether they overlap by calculating the normal vector of the surface, and projecting the possible points onto this vector. If the magnitude of the projected vector is with a certain threshold this means the point exists on the same plane as the surface.  
However, to check whether the point actually exists within the bounds of the surface we then calculate the barycentric coordinates of that points in relation to the surface. If all of the barycentrics coordinates are positive this means the point is within the bounds of the surface.  
Here is are the equations used in these calculations:

![image1](Images/Barycentric_Points.PNG?raw=true)

If both of these conditions are true then a voxel is placed at the points. The output of the script is a 3D matrix with dimensions of 30x30x30; the matrix is binary encoded, meaning that the entries that are 0 signify an empty block and the entries that are 1 signify a cube.

The model we use is a Wasserstein generative adversial netowrk (WGAN). We found this model provided us with better quality generations as compared to when we used a normal GAN model in our status report. The WGAN differes from a normal GAN in several ways. Firstly, it utilizes a Wasserstein loss function where as previously we used binary cross entropy. Wasserstein loss is defined here:

![image1](Images/Wasserstein_Loss.png?raw=true)

By doing so the discriminator is replaced with a critic. Tnstead of determing whether is real or fake the critic will score the input based on the realness of the input. The generator now trains to minimize the difference in score between real and generated voxel models. Overall, this makes the model more stable and less sensitive to changes to hyper parameters and model architecture.

Another difference with WGAN's is that the critic model is actually trained more than the generator model. In our model we for every time we train the generator model, the critic is trained 5 times. The reason for this is to ensure the critic is optimally trained through each step of the training. The reason for this is that with WGAN's a the critic must be near optimal otherwise training becomes unstable. A poor critic will lead poor assessments of loss on real and generated voxels, which will cause the generator to train inefficiently. Therefore we need to ensure the critic is near convergence before training the generator.

Lastly, we attempted to implement an auxilary conditional GANS (ACGANS) in conjunction with our WGANS. This would have made it possible to train multiple classes of object with a single training model. However, we were not able to achieve good quality results with this model, and instead decided to train 2 seperate WGAN models for chairs and tables.

## Evaluation

Our the process for evaluating the performance of our model revolves around looking at the loss rate of each of our models (the critic and generator), and adjusting the model depending upon which model is lacking in strength. Also we access the stability of the model by checking whether the difference between the critic loss rate of real and generated voxels converge.

## Resources Used

- [TensorFlow](https://www.tensorflow.org)
- [details for .off file format](https://segeval.cs.princeton.edu/public/off_format.html)
- [binary cross-entropy](https://peltarion.com/knowledge-center/documentation/modeling-view/build-an-ai-model/loss-functions/binary-crossentropy)
- [Determing Whether a point exists on a 3D triangular plane](https://math.stackexchange.com/questions/2582202/does-a-3d-point-lie-on-a-triangular-plane)
- [MNIST GANS](https://www.tensorflow.org/tutorials/generative/dcgan)
- [ModelNet Dataset](https://modelnet.cs.princeton.edu/)
- [GAN - Wasserstein Gan and WGAN-GP](https://medium.com/@jonathan_hui/gan-wasserstein-gan-wgan-gp-6a1a2aa1b490)
- [How to Develop a WGAN](https://machinelearningmastery.com/how-to-code-a-wasserstein-generative-adversarial-network-wgan-from-scratch/)
