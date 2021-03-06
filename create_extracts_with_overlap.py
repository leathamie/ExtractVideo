#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 16:16:44 2018

@author: lea
"""
import os
import re
import datetime
import argparse
import subprocess


def extractFileContent(filename):
    """ take a file path and return the content of the file in a str"""
    fileContent = ""
    file = open(filename, "r")
    for line in file : 
        fileContent = fileContent + line
    return fileContent
            
def getBigining(filename):
    """Get the bigining of the speech in the cha file (str). If the speech duration 
        is not specified return '-1'. """
    content = extractFileContent(filename)
    all_duration = re.findall('[0123456789][0123456789]*_[0123456789][0123456789]*', content)
    if len(all_duration) > 0:
        first_duration = all_duration[0]
        on = first_duration.split('_')[0]
    else:
        on = '-1'   
    return on

def getEnd(filename):
    """ Read a cha file and get the end of the last speech in the file """
    content = extractFileContent(filename)
    last_duration = re.findall("[0123456789][0123456789]*_[0123456789][0123456789]*", content)[-1]
    off = last_duration.split('_')[1]
    return off

def get_duration(file):
    """Get the duration of a video using ffprobe."""
    cmd = 'ffprobe -i {} -show_entries format=duration -v quiet -of csv="p=0"'.format(file)
    output = subprocess.check_output(
        cmd,
        shell = True, # Let this run in the shell
        stderr=subprocess.STDOUT
    )
    # return round(float(output))  # ugly, but rounds your seconds up or down
    return float(output)


def cut_video(video_path, dur,overlap,in_wav, out_folder, begin, end):
    """ take a video a duration and an ovelap and create extract with the duration and le overlap"""
    on = float(begin)
    off = on + float(dur)
    while off <= float(end):
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
        process = subprocess.call(cmd)
        on = on + float(dur) - float(overlap)
        off = off + float(dur) - float(overlap)
    return process
         
 

def main():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--input", help="Video(s) folder path")
    ap.add_argument("-o", "--output", help="Videos extracts folder path")
    ap.add_argument("-d", "--duration", type=float, default=4.0, help="Exracts duration in seconds (default : 5sec)")
    ap.add_argument("-ov", "--overlap",type=float, default=1.0, help="Extracts overlap in seconds (default : 1.0)")
    ap.add_argument("-s", "--start", type=float, default=120.0, help="start of cutting in seconds (default: 0)")
    ap.add_argument("-e", "--end", type=float, help="start of cutting in seconds (default: file length)")
    ap.add_argument("-cha", "--cha", help="if a cha folder file is specified, the begin and the and of the cutting will match with the corresponding cha file" )
    args = vars(ap.parse_args())

    # read arguments and call cut_video function
    folderPath = args["input"]
    for filename in os.listdir(folderPath):
        videoPath = folderPath+'/'+filename
        if filename.endswith('.mp4'):
            namelist = filename.split('/')
            name = namelist[-1]
            name = name.split('.')[0]
            if args.get("cha", None) is not None: 
                chafile = args["cha"] + "/" + name + ".cha"
                if os.path.isfile(chafile):
                    on = float(getBigining(chafile))*0.001
                    if (on >= 0):
                        if float(args["start"]) > on:
                            on = float(args["start"])
                        off = float(getEnd(chafile))*0.001
                        cut_video(videoPath,args["duration"],args["overlap"], name, args["output"], on, off)
            else:
                totalDur = get_duration(videoPath)
                begin = args["start"] # default : start the cut after 2 minutes
                cut_video(videoPath,args["duration"],args["overlap"], name, args["output"],float(begin), float(totalDur) )

    
    
    


if __name__ == "__main__":
    main()
