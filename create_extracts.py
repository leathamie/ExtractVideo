#!/usr/bin/env
#
import os
import sys
import shutil
import datetime
import subprocess
#from progressbar import ProgressBar

def read_lab(lab):
    """ read the speech activity detection and output list of 
        onsets and offsets"""
    sad = []

    with open(lab, 'r') as fin:
        speech = fin.readlines()
        for line in speech:
            on, off, state = line.strip('\n').split(' ')
            if state == "speech":
                sad.append((float(on), float(off)))

    return sad

def read_lab_getAll(lab):
    """ read the speech activity detection and output list of 
        onsets and offsets"""
    sad = []
    with open(lab, 'r') as fin:
        speech = fin.readlines()
        for line in speech:
            on, off, state = line.strip('\n').split(' ')
            if state == "speech":
                sad.append((float(on), float(off), 'True'))
            else: 
                sad.append((float(on), float(off), 'False'))
    return sad

def read_txt(txt): 
    sad = []
    with open(txt, 'r') as fin:
        speech = fin.readlines()
        for line in speech:
            on, off, state = line.strip('\n').split(',')
            sad.append((float(on), float(off), state))
    return sad

def read_rttm(rttm):
    """ read the speech activity detection in rttm format and output
        list of onsets and offsets"""
    sad = []
    with open(rttm, 'r') as fin:
        speech = fin.readlines()
        for line in speech:
            _, _, _, on, off, _, _, _, _ = line.strip('\n').split('\t')
            try:
                sad.append((float(on), float(off)))
            except:
                pass
    return sad

def concatenate(sad, dur):
    """ take a list of onsets and offsets and a duartion. It contatenate
    wo onsets if the offset between them lasts less than dur """
    onlyTrueList = []
    for on, off, state in sad: 
        i = len(onlyTrueList)-1
        if state == 'True':
            if i<0:
                onlyTrueList.append([on,off])
            else:
                if on == onlyTrueList[i][1]:
                    onlyTrueList[i][1] = off
                else:
                    onlyTrueList.append([on,off])
        else:
            duration = off - on;
            if duration <= dur:
                onlyTrueList[i][1] = off
    return onlyTrueList
        
def deleteByLength(sad, dur):
    returnList = []
    for on, off in sad:
        duration = off - on
        if duration > dur:
            returnList.append([on, off])
    return returnList        
        
    
    
def cut_video(sad, in_wav, out_folder):
    """ take list of onsets and offsets and cut the video at these times"""
    totalDur= 0
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
    return process

def main():
    """
    # read arguments
    lab = sys.argv[1]
    video = sys.argv[2]
    out_folder = sys.argv[3]

    # read sad
    #sad = read_lab(lab)
    sad = read_rttm(lab)
    # cut_video
    cut_video(sad, video, out_folder)
    """
    video = 'data/011100.mp4'
    out_folder = 'data'
    filename = '/home/lea/Stage/DATA/videos/011100.mp4.txt'
    sad = read_txt(filename)
    print (str(sad))
    """
    filename = 'datatest/011100.lab'
    sad = read_lab_getAll(filename)
    print (str(len(sad)))
    sad = concatenate(sad, 0.0000005)
    sad = deleteByLength(sad, 1)
    print (str(len(sad)))
    print (str(sad))
    cut_video(sad, video, out_folder)
    """
    


if __name__ == "__main__":
    main()

