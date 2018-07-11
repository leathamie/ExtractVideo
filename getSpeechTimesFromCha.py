#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 11 02:06:40 2018

@author: lea
"""
import re

def extractFileContent(filename):
    fileContent = ""
    file = open(filename, "r")
    for line in file : 
        fileContent = fileContent + line
    return fileContent


        
def getAllSpeechDuration(filename):
    content = extractFileContent(filename)
    duration_tab = re.findall('[0123456789][0123456789]*_[0123456789][0123456789]*', content)
    return duration_tab
            
def getBigining(filename):
    content = extractFileContent(filename)
    m = re.search('[0123456789][0123456789]*_[0123456789][0123456789]*', content)
    first_duration = m.group(0)
    on = first_duration.split('_')[0]
    return on

def getEnd(filename):
    content = extractFileContent(filename)
    last_duration = re.findall("[0123456789][0123456789]*_[0123456789][0123456789]*", content)[-1]
    off = last_duration.split('_')[1]
    print(off)
    return off

print ("resultat de getBiigining" + str(getBigining('/home/lea/Stage/DATA/chaFiles/Rollins/cb06.cha')))
getEnd('/home/lea/Stage/DATA/chaFiles/Rollins/cb06.cha')