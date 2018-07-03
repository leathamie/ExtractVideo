#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 16:16:44 2018

@author: lea
"""
import os
import cv2                            # importing Python OpenCV
import sys
import shutil
import datetime
import subprocess

def cut_video(video_path, dur, in_wav, out_folder):
    """ take a video a duration and an ovelap and create extract with the duration and le overlap"""
    video = cv2.VideoCapture(video_path)
    nbframes = video.get(7)
    fps = video.get(5)#frames /sec
    print("durée de la video " + str(nbframes/fps))
    print ("number of frames " + str(nbframes))
    totalDur= nbframes/fps
    on = 120.0 # start the cut after 2 minutes
    off = float(dur)
    while off <= totalDur:
        # convert the onset/offsets in hh:mm:ss format for ffmpeg
        hour_on = str(datetime.timedelta(seconds=float(on)))
        hour_dur = str(datetime.timedelta(seconds=float(dur)))
        # name of the output
        base = os.path.basename(in_wav).split('.')[0]
        out_file = os.path.join(out_folder,
                                '_'.join([base, str(on), str(off)]) + '.mp4')

        # command to launch
        cmd = ['ffmpeg', '-ss', '{}'.format(hour_on),
               '-i', '{}'.format(video_path), '-c', 'copy', '-t','{}'.format(hour_dur),
               out_file]
        process = subprocess.call(cmd)
        on = on + float(dur) - 1
        off = off + float(dur) - 1
    return process
         
""" 
    for on, off in sad:
        dur = off - on
        totalDur = totalDur + dur
        
        #dur = off
        # convert the onset/offsets in hh:mm:ss format for ffmpeg
        hour_on = str(datetime.timedelta(seconds=on))
        hour_dur = str(datetime.timedelta(seconds=dur))

        # name of the output
        base = os.path.basename(in_wav).split('.')[0]
        out_file = os.path.join(out_folder,
                                '_'.join([base, str(on), str(off)]) + '.mp4')

        # command to launch
        cmd = ['ffmpeg', '-ss', '{}'.format(hour_on),
               '-i', '{}'.format(in_wav), '-c', 'copy', '-t','{}'.format(hour_dur),
               out_file]
        process = subprocess.call(cmd)
    print ("durée totale : " + str(totalDur))
"""
    

def main():
    
    # read arguments
    video = sys.argv[1]
    dur = sys.argv[2]
    overlap = sys.argv[3]
    out_folder = sys.argv[4]

    # cut_video
    cut_video(video, dur, overlap, out_folder)
    
    
    


if __name__ == "__main__":
    main()
