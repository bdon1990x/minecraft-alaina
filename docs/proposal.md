---
layout: default
title: Proposal
---

## Proposal

### Summary of the Project

The goal of our project was to generate 3D structures using a generative adversial network(GAN). Our AI "Alaina" will parse the input text for
keywords which will be used to identify the type of object being generated. After the type of object has been decided the appropriate pre-trained
model will be loaded and the generative model is inputted with random noise. The output of the generative model will be a 3D matrix consisting
of a probability for each value. The probabilities are rounded and the model is then rendered. 0's will be interpretted as an empty space while 1's will be interpretted as occupied space.

### AI/ML Algorithms

We plan on using generative adversial networks. The dataset will be a set of 3D models, which will be voxelized so that it is more easily buildable in Minecraft. Text command could be implemented by simplying parsing the text for keywords.

### Evaluation Plan

#### Quantitative:

- Time the agent take to finish the task.
- Mistakes the agent made through the process.

As for quantitative evualuations we will look at the training time of model.  

#### Qualitative:

- Completeness of the building. Is every block arranged correctly? Is any part of the structure missing?

In terms of qualitative evaluations, we would like to evaluate the generated structures by how seamlessly they pass the eye-test. We'd like to ask questions such as, 'Does the structure look at all abnormal?', 'Does it resemble the desired item?', or 'Is the object structurally sound?'

### Appointment with the Instructor

Time: 09:30 am Oct 16, 2019
