# -*- coding: utf-8 -*-

import os
import sys
# sys.path.append('../')
# from pytube import YouTube
from annotator import Annotator

# Set up some folders
demo_folder = r'./'
clips_folder = r'video_clips'
# youtube_filename = 'youtube.mp4'
videos_folder = r'videos'


vids = [each for each in os.listdir("videos")]

# Create the folders
if not os.path.exists(clips_folder):
    os.mkdir(clips_folder)

# fin = []
# #check if the video is done.
# with open("finished_vids.txt","r") as f:
#     for line in f:
#         fin.append(line.strip())

each = sys.argv[1]
if len(sys.argv) > 2:
	loadflag = sys.argv[2]
else:
	loadflag = None

#clips forlder for this video
clips_folder = os.path.join(clips_folder,each)
annotation_path = os.path.join("annotation",each)

annotation_path_for_vid = os.path.exists(os.path.join(annotation_path,"labels.json"))
if not os.path.exists(annotation_path):
    os.makedirs(annotation_path)

# Initialise the annotator
annotator = Annotator([
        {'name': 'goal', 'color': (0, 255, 0)},
        {'name': 'others', 'color': (0, 0, 255)},
        {'name': 'startgame', 'color': (0, 255, 255)},
        {'name': 'endgame', 'color': (255, 255, 255)},
        {'name': 'replay_goal', 'color': (0, 0, 0)},
        {'name': 'resume','color':(64,244,226)},
        {'name':'SOT','color':(66, 86, 244)},
        {'name':'play','color':(244, 155, 65)},
        {'name':'replay','color':(193, 52, 156)}],
        clips_folder, sort_files_list=True, N_show_approx=20, screen_ratio=16/9, 
        image_resize=1, loop_duration=None, annotation_file=os.path.join(annotation_path,'labels.json'))

if not os.path.exists(clips_folder):
    # Split the video into clips
    os.makedirs(os.path.join(clips_folder))
    print('Generating clips from the video...')
    annotator.video_to_clips(os.path.join(videos_folder,each), clips_folder, clip_length=60, overlap=0, resize=0.5)

if annotation_path_for_vid:
	if loadflag is None:
	    resp = input("the anotations will be overwritten. continue? (y/n)")
	    if resp.strip().lower() == "n":
	        sys.exit()

	    else:
	        #remove the older annotations for the video.
	        if annotation_path_for_vid:
	            os.remove(os.path.join(annotation_path,"labels.json"))

# Run the annotator
annotator.main()

print("video annotation for ",each," finished.")