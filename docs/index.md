---
layout: default
title:  Home
---
## Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/sxEHsrqkEUA" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>

## Summary

The goal of our project was to generate 3D structures using a Generative Adversarial Network(GAN). After the type of object has been decided the appropriate pre-trained
model will be loaded and the generative model is inputted with random noise. The output of the generative model will be a 3D matrix consisting
of a probability for each value. The probabilities are rounded such that 0's will be interpreted as an empty space while 1's will be interpreted as occupied space. Lastly the 3D matrices are rendered into Minecraft in a 30x30 area.

## Reports:

- [Proposal](proposal.html)
- [Status](status.html)
- [Final](final.html)