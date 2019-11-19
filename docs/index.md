---
layout: default
title:  Home
---
## Alaina

Let's welcome our 3D objects builder in Minecraft: Alaina!

![image1](Images/Code_Builder.png?raw=true)

Source code: [Github](https://github.com/bdon1990x/minecraft-alaina)

## Video
[![Titile](/Images/FirstPage.png)](https://youtu.be/eLTgYg-6Mcw "Alaina: Status Report")

## Summary

The goal of our project was to generate 3D structures using a generative adversial network(GAN). Our AI "Alaina" will parse the input text for
keywords which will be used to identify the type of object being generated. After the type of object has been decided the appropriate pre-trained
model will be loaded and the generative model is inputted with random noise. The output of the generative model will be a 3D matrix consisting
of a probability for each value. The probabilities are rounded and the model is then rendered. 0's will be interpretted as an empty space while 1's will be interpretted as occupied space.

## Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)