#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 27, 2015
'''
# enable debugging
import cgitb
cgitb.enable()

import getEntities, sys
from storage import commonvariables as comm

def readPlainText(htmlurl, plaintext, ontologyData, _encoding):
    try:
        try:
            punc = (plaintext.decode(_encoding)).strip()
        except:
            try:
                punc = (plaintext.decode(sys.stdout.encoding)).strip()
            except:
                try:
                    punc = (plaintext.decode('UTF-8')).strip()
                except:
                    try:
                        punc = (plaintext.decode('latin-1')).strip() 
                    except:
                        try:
                            punc = (plaintext.decode('ISO-8859-1')).strip()  
                        except:
                            try:
                                punc = (plaintext.decode()).strip()  
                            except:
                                punc = plaintext
                                pass 
                        
        sentences = comm.replaceToPunkts(punc)
        for sentence in sentences:
                getEntities.getEntities(htmlurl, sentence, ontologyData)
    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_plaintext.py " + _encoding + " " + htmlurl)
    

