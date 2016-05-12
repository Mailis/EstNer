#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 27, 2015
'''
# enable debugging
import cgitb
cgitb.enable()

import getEntities, sys
import commonVariables as comm

def readPlainText(htmlurl, plaintext, ontologyData):
    try:
        punc = (plaintext).strip() 
        sentences = comm.replaceToPunkts(punc)
        for sentence in sentences:
            getEntities.getEntities(htmlurl, sentence, ontologyData)
    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_plaintext.py " + htmlurl)
      

