#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import commonVariables as comm

def isNeededUrl(url):
    neededUrl = True
    fileName =  (url.lower().split("/"))[-1]
    if(fileName in comm.undesiredFileName):
        neededUrl = False
    if(neededUrl):        
        extSplit = (fileName.split("."))
        lastIndex = len(extSplit)-1
        if(lastIndex > 0):
            extension = (extSplit[lastIndex])
            if(extension in comm.undesiredFileExtensions):
                neededUrl = False
    if(neededUrl):
        for udft in comm.undesiredFileTypes:
            if(udft in url):
                neededUrl = False
                break
    return neededUrl