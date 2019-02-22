import os
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import data, exposure
import numpy as np
import cv2 as cv2
from natsort import natsorted
import tkinter as tk
from tkinter import filedialog
import shutil

# Most effective at 1280x720.

def readMov(mov):
    # Open the input movie file
    input_movie = cv2.VideoCapture(mov)
    length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

    # Declare some variables.
    frame_number = 1
    all_hogs = [] # running storage for hogs
    ret = True

    # This loop will read each frame of the video and calulate the HOG. It will then save the HOG pattern as an image
    # to a temp directory.
    while frame_number < length + 1:
        # Grab a single frame of video
        ret, frame = input_movie.read()


        # Quit when the input video file ends
        if not ret:
            break

        # Processes the image and creates a hog image.
        fd, hog_image = hog(frame, orientations=10, pixels_per_cell=(16, 16),
                            cells_per_block=(1, 1), visualize=True, multichannel=True)

        # Rescale brightness of the HOG for better display.
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

        # Save to a temp directory.
        plt.imsave(str('temp/' + str(frame_number)), hog_image_rescaled, cmap=plt.cm.gray)
        print('Encoding frame: {} / {}'.format(frame_number, movLength))
        frame_number += 1


def writeMov(video_name, image_folder, fps):
    # use ffmpeg to write the images to video
    images = [img for img in sorted(os.listdir(image_folder)) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'H264')  # 'x264' doesn't work

    video = cv2.VideoWriter('Output/' + video_name, fourcc, 24, (width,height))
    images = natsorted(images)
    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    # All done!


root = tk.Tk()
root.withdraw()
InputVideo = filedialog.askopenfilename()

# Output file name
OutputFileName = os.path.basename(InputVideo).split('.')[0] + "_HOG.mp4"

# Open the input movie file
input_movie = cv2.VideoCapture(InputVideo)
movLength = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))  # Number of frames in the video.

# Creates the temp directory.
os.mkdir('temp/')

# This function reads the input video and calculates the HOG patterns.
readMov(InputVideo)

# This function writes a video where each frame is a HOG pattern.
writeMov(OutputFileName, 'temp/', 30)

