#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import commonVariables as comm

    
def isValideType(tyyp):
    typeIsDesired = True
    #disable unwanted content types
    for typ in comm.undesiredFileTypes:
        tyyyp = typ.lower()
        if (tyyyp  in tyyp) or (tyyp in tyyyp ):
            typeIsDesired = False
    return typeIsDesired


def isNeededUrl(url):
    neededUrl = True
    fileName =  (url.lower().split("/"))[-1]
    if(fileName in comm.undesiredFileName):
        neededUrl = False
    if(neededUrl):        
        extSplit = (fileName.split("."))
        lastIndex = len(extSplit)-1
        if(lastIndex > 0):
            extension = (extSplit[lastIndex]).lower()
            for ext in comm.undesiredFileExtensions:
                ext = ext.lower()
                if(extension in ext) or (ext in extension):
                    neededUrl = False
    if(neededUrl):
        for udft in comm.undesiredFileTypes:
            if(udft in url):
                neededUrl = False
                break
    return neededUrl