# **Behavioral Cloning** 

---

**Behavioral Cloning Project**

The goals / steps of this project are the following:
* Use the simulator to collect data of good driving behavior
* Build, a convolution neural network in Keras that predicts steering angles from images
* Train and validate the model with a training and validation set
* Test that the model successfully drives around track one without leaving the road
* Summarize the results with a written report


[//]: # (Image References)

[center]: ./writeup_img/center.jpg "Center Image"
[left]: ./writeup_img/left.jpg "Left Image"
[right]: ./writeup_img/right.jpg "Right Image"

## Rubric Points
###Here I will consider the [rubric points](https://review.udacity.com/#!/rubrics/432/view) individually and describe how I addressed each point in my implementation.  

---
## Files submitted

* model.py for creating the model with keras
* drive.py for running the car in autonomous mode (did not modify it)
* model_first_track.h5 model trained from the first track images only
* model_second_track.h5 model trained from the second track images only
* track1.mp4 video of car driving on track 1
* track2.mp4 video of car driving on track 2
* writeup.md summary of the work

## Input data
Data was recorded in 160x320 RGB format, and images from left, center and right cameras were used. Some examples are shown below, for a particular position on the second track.

![alt text][center]
![alt text][left]
![alt text][right]

### Data preprocessing

Each image was normalized by diving each channel by 255 and making it zero mean by substracting 0.5 (range from -0.5 to 0.5). No grayscaling was applied. The images were also cropped so that the main focus was on the road, for minimizing the landscape content in the images. In order to augment the data, the images were flipped, corresponding to a negative steering angle output compared to the original images. When using the left and right images, a small correction was applied to the original steering angle. I found that a good value is somewhere between 0.3 to 0.5. This is achieved by experimenting with different values, but in reality it depends, on the distance between the cameras, and the distance/orientation between the cameras and the road.

## Network architecture

The starting point was the LeNet architecture. 

* The only modification I made was to reduce the number of neurons in the last fully connected layer to 64.
* Adam optimizer was used
* For both the first and second track, between 40000 and 50000 images were used
* trained for 1 epoch (if more epochs were used, the training and validation losses would have increased, so I stayed with 1 epoch)
* 10% validation data
* did not use any droput, since the network is fairly small and the droput is effective in deeper networks with more connections
* RMSE cost function
* model trained on the AWS instance

## Strategies for recording data

There are a few interesting findings for recording the training data:

* since the network uses the RMSE of the steering angle, continuous values of the steering angle result in better training for the network; that is why the mouse was used for steering. Keyboard inputs are very discrete, having many spikes. This means that, for the same set of images, very high or close to zero steering angles are fed in the network for training, resulting in erratic behavior.
* I drove the car quite slowly, especially in the turns, so that more images were recorded for these important edge cases (images are recorded at 10 Hz, so driving slower will result in more training data at a given position on the track).
* After driving the car in the center of the lane, I also drove it close to the edges and then recovering it towards the middle, so that it knows not to stick close to the edges. I also drove the car in the other direction on the track. This results in a better generalization of the training data.
* By observing where the car failed to stay on the lane, I took extra training data on those regions specifically. (For example in very sharp turns in the second track, I had to drive very slowly in these sharp turns and record extra training data).

## Considerations 
* The car drives successfully on the first track.
* The car drives successfully on the second track, except at the very end, where it crosses the metal poles and starts driving on the road from the other side of the track. It is interesting that it does not go away from the road, but just switches from the main road to the one from the other side. 
* I should have trained a single network with the combined data from the first and second tracks. Now, I have 2 separate models for the two tracks. I will do this soon, however I wanted to sumbit this project as is for now. 
