#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 24, 2015
'''
# enable debugging
import cgitb
cgitb.enable()

import json, sys
import getEntities
import commonVariables as comm

def readJson(jsonurl, readedPage, od):
    '''#if httpResponse is filepath
    jsonfile = (httpResponse.read()).decode('utf-8')
    '''
    #if httpResponse is saved nto string already
    try:
        jsonfile = (readedPage).strip()
        dictnry = json.loads(jsonfile)
        readDictValues(jsonurl, dictnry, set(), od)

    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_json.py " + jsonurl)
        pass

def startToGetEntities(jsonurl, lause, ontologyData):
    sentences = comm.replaceToPunkts(lause)
    for sentence in sentences:
        getEntities.getEntities(jsonurl, sentence, ontologyData)


def readDictValues(jsonurl, dictnry, tmpSet, ontologyData):
    if(type(dictnry) is dict):
        keys = list(dictnry.keys())
        for kii in keys:
            s6ne = dictnry[kii]
            if(type(s6ne) is not dict):
                if(type(s6ne) is list):
                    for e in s6ne:    
                        if(type(e) is dict): 
                            readDictValues(jsonurl, e, tmpSet, ontologyData)
                        else:   
                            if(e not in tmpSet) & (not comm.is_number(e)):                                 
                                tmpSet.add(e)
                                startToGetEntities(jsonurl, e, ontologyData)
                else:
                    if(s6ne not in tmpSet) & (not comm.is_number(s6ne)):                                  
                        tmpSet.add(s6ne)
                        startToGetEntities(jsonurl, s6ne, ontologyData)
            else:
                readDictValues(jsonurl, s6ne, tmpSet, ontologyData)
            




