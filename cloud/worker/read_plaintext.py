#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 27, 2015
'''
# enable debugging
import cgitb
cgitb.enable()

import getEntities, sys
import commonvariables as comm

def readPlainText(htmlurl, plaintext, ontologyData, _encoding):
    try:
        if(_encoding != None):
            if("utf" in _encoding.lower()):
                _encoding = _encoding.upper()
            try:
                punc = (plaintext.decode(_encoding)).strip()
            except:
                try:
                    punc = (plaintext.decode(sys.stdout.encoding)).strip()
                except:
                    punc = (plaintext.decode('latin-1')).strip() 
        else:
            try:
                punc = (plaintext.decode(sys.stdout.encoding)).strip()
            except:
                punc = (plaintext.decode('latin-1')).strip()    
                
        sentences = comm.replaceToPunkts(punc)
        for sentence in sentences:
            if(len(sentence) > 2) & (not comm.is_number(sentence)):
                getEntities.getEntities(htmlurl, sentence, ontologyData)
    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_plaintext.py " + _encoding + " " + htmlurl)
    

