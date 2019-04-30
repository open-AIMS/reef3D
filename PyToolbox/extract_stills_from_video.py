# Program To Read video
# and Extract Frames
import os

import cv2
import sys


def frame_capture(file_to_import, frames_per_sec, stills_destination, deinterlacing):

    # Path to video file
    vidObj = cv2.VideoCapture(file_to_import)
    fps = vidObj.get(cv2.CAP_PROP_FPS)

    # Used as counter variable
    image_count = 0
    frame_counter = -1
    frames_per_sec = int(fps/frames_per_sec)
    print(frames_per_sec)
    # checks whether frames were extracted
    success = 1
    still_path = os.path.join(stills_destination, "frame%d.jpg")

    while success:

        frame_counter += 1

        # vidObj object calls read
        # function extract frames
        success, image = vidObj.read()

        if frame_counter % frames_per_sec == 0:

            print("Writing", image_count, still_path % frame_counter)

            if deinterlacing:
                #de-interlace the frame
                image[1:-1:2] = image[0:-2:2] / 2 + image[2::2] / 2

            # Saves the frames with frame-image_count
            cv2.imwrite(still_path % frame_counter, image)

            image_count += 1


'''

import glob2 as glob2
if __name__ == "__main__":
    # settings
    frames_per_sec = 4
    deinterlacing = False

    # find all videos in destinations
    video_root = "/media/mat/My Book Duo/NWSS/Trip6999/Structure Video/"
    videos = glob2.glob(video_root + "**/*.MP4")

    # loop through videos
    for video in videos:
        # make stills destination path for this video
        destination_path = video.replace("Structure Video", "Structure Stills").replace(".MP4", "")

        # make this stills directory for these stills
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        # extract stills and put them in a global output dir
        frame_capture(video, frames_per_sec, destination_path, deinterlacing)

'''

if __name__ == "__main__":

    if len(sys.argv) < 5:
        this_py_file = sys.argv[0]

        print ("Error!")
        print ("Usage: %s <import filename> <frames per second> <stills destination path> <de-interlacing (t|f)>" % this_py_file)
        print ("Example: %s myfile.avi 4 . t" % this_py_file)

        sys.exit(1)

    # image_paths = glob2.glob("/Users/mat/Downloads/Heithaus_BB_images/*/*.jpg")

    file_to_import = sys.argv[1]
    frames_per_sec = int(sys.argv[2])
    stills_destination = sys.argv[3]
    deinterlacing = sys.argv[4]

    if deinterlacing is "t":
        deinterlacing = True
    else:
        deinterlacing = False

    # Calling the function
    frame_capture(file_to_import, frames_per_sec, stills_destination, deinterlacing)