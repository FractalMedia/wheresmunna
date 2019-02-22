# "Where's Waldo: Facial Recognition Package"

## Installation
1. pip install requirements.txt for all relevant dependencies.
2. install face_recognition: https://github.com/ageitgey/face_recognition.
3. install openface: https://github.com/cmusatyalab/openface.

## Face Detection and Landmarks (face_recognition)

HOG-Landmarks uses face_recognition extensively. The code in "HOG-Landmarks" have details to produce images shown in the video.

## Deep Learning Feature Maps (openface)

Replace vis-outputs.lua in the Openface install with the file in our "CNN-Openface" to replicate the figures from the video (line 30 specifies the aligned image to use, after normalization has been completed following the "Preprocess" step here: http://cmusatyalab.github.io/openface/visualizations/. 

You will need to add the file structure from our "data" folder into the Openface directory. 

## Results/MTurk 

We used the following setup for the task: https://blog.mturk.com/tutorial-annotating-images-with-bounding-boxes-using-amazon-mechanical-turk-42ab71e5068a?gi=e1efd0da6360.

"MTurk Analysis.xlsx" contains a summary pivot table that averages results from 100 participants (in sheet2). 

The .csv labeled "Final_Mturk_Raw" contains task performance by participant and picture on MTurk. Our only eligibility criteria was       participant age > 18 and > 90% HIT acceptance rate (i.e. high performance workers). 

mturk_analysis.py contains the reading of the raw data, merging it with the information from “key.xlsx” to output “MTurk                Analysis.xlsx.” Line 80 specifies the IOU, > 0.30 (relatively low threshold due to the nature of the task on MTurk). 

## Histogram of Oriented Gradients Display

In the HOG.py script, you will be prompted for a video file. The script will then output a new file that displays the HOG over that video.

## Landmarks

In the landmarks.py script, head to the bottom to make some adjustments. You will need to enter an input file path, choose an output name, and indicate whether you are inputting a video or a picture. Then, the script will output two files: The first is a .csv that contains position data for the landmarks. Each row represents a different frame. Two columns represent a landmark, first the x value position and then the y value position. 

The second file will be a video or picture with landmarks drawn onto the file. 

## Webcam

A fun little addition, the webcam.py script allows you to identify your own face in a webcam video. Simply add a photo to face1 or face2. This script will also overlay the HOG patterns and landmarks. We recommend running one of those at a time, as they will slow the webcam view down significantly.  
