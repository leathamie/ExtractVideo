#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 16:16:44 2018

@author: lea
"""
import os
#import cv2                            # importing Python OpenCV
import sys
import glob
#import shutil
import datetime
import subprocess
import subprocess 

def get_duration(file):
    """Get the duration of a video using ffprobe."""
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(file)
    output = subprocess.check_output(
        cmd,
        shell=True, # Let this run in the shell
        stderr=subprocess.STDOUT
    )
    # return round(float(output))  # ugly, but rounds your seconds up or down
    return float(output)


def cut_video(video_path, dur,overlap,in_wav, out_folder):
    """ take a video a duration and an ovelap and create extract with the duration and le overlap"""
    print (video_path)
    totalDur = get_duration(video_path)
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
               '-i', '{}'.format(video_path), '-c', 'copy','-an' ,'-t','{}'.format(hour_dur),
               out_file]
        print (cmd)
        process = subprocess.call(cmd)
        on = on + float(dur) - float(overlap)
        off = off + float(dur) - float(overlap)
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
    videoPath = sys.argv[1]
    dur = sys.argv[2]
    overlap = sys.argv[3]
    out_folder = sys.argv[4]
    for filename in glob.glob(videoPath + '*.mp4'):
        namelist = filename.split('/')
        name = namelist[len(namelist)-1]
        name = name.split('.')[0]
        cut_video(filename,dur,overlap, name, out_folder)
    
    
    
    
    


if __name__ == "__main__":
    main()
