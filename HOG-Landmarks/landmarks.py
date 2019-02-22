import face_recognition
import cv2
import csv
import pandas as pd
import numpy as np
from scipy.signal import savgol_filter
import tkinter as tk
from tkinter import filedialog
from natsort import natsorted
import os
import sys


def landmarks_smoothed_video_csvexport(video, length):
    ### This function will take a video, capture landmark data for each frame, and export that data to a csv. Each landmark will
    ### have two columns, x position and y position. Each column will span the length of the video, in frames, for that landmark.


    frame_number = 0  # Starting frame.
    agg_array = np.zeros((length, 144))

    while True:
        # Grab a single frame of video.
        ret, frame = video.read()

        # Quit when the input video file ends.
        if not ret:
            break

        # Find all facial features in all the faces in the image.
        face_landmarks_list = face_recognition.face_landmarks(frame)

        # This will store an array for each face in the video.
        arrays = [[]] * len(face_landmarks_list)


        # Extract the data. [{[(x,y)]}]. The resulting array will become a row, with x0,y0,x1,y1,x2,y2,...,x68,y68 where
        # there are 68 facial features [chin 1, chin 2, ... , left_eyebrow 4, left_eyebrow 5, ...]
        for index, face in enumerate(face_landmarks_list):
              # Initialize a final array.
            entry_num = 0

            for feature in face:
                for currTup in face[feature]:
                    for currPoint in currTup:
                        # append to the array x00, y00, x10, y10, x20, y20... xnm, ynm where n is the number of facial
                        # features (68) and m is the number of frames of the video. Each row of the outputted csv is a
                        # frame.
                        agg_array[frame_number][entry_num] = currPoint
                        entry_num += 1
            entry_num = 0

        entry_num = 0

        frame_number = frame_number + 1
        print('Writing frame to CSV: {} / {}'.format(frame_number, length))

    # This smooths the data to avoid jumpiness in the landmarks.
    aggArraySmoothed = agg_array
    colCount = 0
    for column in agg_array.T:
        currArr = np.array(column)
        filtArr = savgol_filter(currArr, 5, 2)  # window size 5, polynomial order 2
        aggArraySmoothed[:, colCount] = filtArr
        colCount += 1

    np.savetxt('Output/' + OutputFileName + '_landmarks.csv', aggArraySmoothed, delimiter=",", fmt='%f')
    print('Done')


def landmarks_single_frame(frame, length):
    ### This function will take a photo, capture landmark data, and export that data to a csv. Each landmark will
    ### have two columns, x position and y position.

    face_landmarks_list = face_recognition.face_landmarks(frame)

    aggregatearray = []

    entryNum = 0

    for face in face_landmarks_list:
        temp_array = np.zeros((1, 144))
        for feature in face:
            for currTup in face[feature]:
                for currPoint in currTup:
                    # append to the array x00, y00, x10, y10, x20, y20... xnm, ynm where n is the number of facial
                    # features (68) and m is the number of frames of the video. Each row of the outputted csv is a
                    # frame.
                    temp_array[0][entryNum] = currPoint
                    entryNum += 1
        aggregatearray.append(temp_array)
        entryNum = 0


    for index, face in enumerate(face_landmarks_list):
        np.savetxt('Output/' + OutputFileName + '_landmarks.csv', aggregatearray[index], delimiter=",", fmt='%f')
    print('Done')


def landmarks_over_video(video, radius, thickness):
    frame_number = 0
    temp_dir = 'temp/'
    if os._exists(temp_dir):
        pass
    else:
        os.mkdir('temp/')
    while True:
        # Grab a single frame of video.
        ret, frame = video.read()

        # Quit when the input video file ends.
        if not ret:
            break

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses).
        rgb_frame = frame[:, :, ::-1]

        # Find all facial features in all the faces in the image.
        face_landmarks_list = face_recognition.face_landmarks(frame)

        # Extract the data. [{[(x,y)]}]. The resulting array will become a row, with x0,y0,x1,y1,x2,y2,...,x68,y68 where
        # there are 68 facial features [chin 1, chin 2, ... , left_eyebrow 4, left_eyebrow 5, ...]
        for face in face_landmarks_list:
            for feature in face:
                for currTup in face[feature]:
                    cv2.circle(frame, currTup, radius, (0, 0, 255), thickness)
                    # Edit size of circles here.
                    # (img, center, radius, color, thickness=1, lineType=8, shift=0)

        frame_number = frame_number + 1
        cv2.imwrite('temp/' + str(frame_number)+'.png', frame)
        print('Writing frame with landmarks: {} / {}'.format(frame_number, movLength))

    writeMov(OutputFileName, 'temp/', 30)


def writeMov(video_name, image_folder, fps):
    # use ffmpeg to write the images to video
    images = [img for img in sorted(os.listdir(image_folder)) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # 'x264' doesn't work

    video = cv2.VideoWriter('Output/' + video_name + '_landmarks_overlay.mp4', fourcc, 24, (width, height))
    images = natsorted(images)
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    # All done!


def landmarks_over_image(picture, radius, thickness):

    # Find all facial features in all the faces in the image.
    face_landmarks_list = face_recognition.face_landmarks(picture)

    # Extract the data. [{[(x,y)]}]. The resulting array will become a row, with x0,y0,x1,y1,x2,y2,...,x68,y68 where
    # there are 68 facial features [chin 1, chin 2, ... , left_eyebrow 4, left_eyebrow 5, ...]
    for face in face_landmarks_list:
        for feature in face:
            for currTup in face[feature]:
                cv2.circle(picture, currTup, radius, (0, 0, 255), thickness)
                # Edit size of circles here.
                # (img, center, radius, color, thickness=1, lineType=8, shift=0)

    cv2.imwrite('Output/' + OutputFileName +'landmarks_overlay.png', picture)





############################################################
# MANUALLY SET THE FOLLOWING THREE ITEMS. The rest will run automatically.

# Input Video or Photo goes here:
Input = 'example.jpg'

# Output file name goes here. Do not put a file extension, will be automatically set by the function.
OutputFileName = 'Example'

# Is this a video? True. Is this a picture? False.
isVideo = False


# Below are two sets of code, one for outputting a CSV with the landmark data, the other for automatically drawing
# landmark dots over a video/picture. Feel free to run one or the other, or both.


#### CSV CODE ####
# The following code will export a CSV with the landmark data for either a video or a picture.
if isVideo:
    # Video
    input_movie = cv2.VideoCapture(Input)
    movLength = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT)) # Number of frames in the video.
    landmarks_smoothed_video_csvexport(input_movie, movLength)
else:
    # Single picture.
    input_picture = cv2.imread(Input)
    length = 1
    landmarks_single_frame(input_picture, length)


#### OVERLAY CODE ####
# This code will out put a video/picture with landmarks drawn on.

# These values set the radius and thickness of the landmark dots. They will need to be played with
# depending on the resolution of the video.
radius = 2
thickness = 4


if isVideo:
    InputVideo = Input

    input_video = cv2.VideoCapture(InputVideo)
    movLength = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))  # Number of frames in the video.
    landmarks_over_video(input_video, radius, thickness)

else:
    InputPhoto = Input

    input_photo = cv2.imread(InputPhoto)
    landmarks_over_image(input_photo, radius, thickness)

############################################################
