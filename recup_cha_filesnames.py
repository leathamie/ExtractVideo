#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 02:20:53 2018

@author: lea
"""
import os

path = '/home/lea/Stage/DATA/chaFiles/Rollins'
filesnames=''
for filename in os.listdir(path):
        if filename.endswith('.cha'):
            namelist = filename.split('/')
            name = namelist[len(namelist)-1]
            name = name.split('.')[0]
            filesnames = filesnames+( name + ".mp4\n")
            
print(filesnames)

