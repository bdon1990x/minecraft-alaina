---
layout: default
title:  Home
---
## Alaina

Let's welcome our 3D objects builder in Minecraft: Alaina!

![image1](Images/Code_Builder.png?raw=true)

Source code: [Github](https://github.com/bdon1990x/minecraft-alaina)

## Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/sxEHsrqkEUA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Summary

The goal of our project was to generate 3D structures using a generative adversial network(GAN). After the type of object has been decided the appropriate pre-trained
model will be loaded and the generative model is inputted with random noise. The output of the generative model will be a 3D matrix consisting
of a probability for each value. The probabilities are rounded such that 0's will be interpretted as an empty space while 1's will be interpretted as occupied space. Lastly the 3D matrices are rendered into minecraft in a 30x30 area.

## Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)