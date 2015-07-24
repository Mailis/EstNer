#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 23, 2015
https://docs.python.org/3.4/library/xml.etree.elementtree.html
'''
# enable debugging
import cgitb
cgitb.enable()

import xml.etree.ElementTree as ET
import getEntities
import commonVariables as comm


def readXml(xmlurl, pathToFile, ontologyData):
    
    #https://docs.python.org/3.4/library/functions.html#setattr
    '''
    #https://docs.python.org/3.4/library/xml.etree.elementtree.html?highlight=elementtree#parsing-xml
    if httpResponse is path to xml file:
      tree = ET.parse(httpResponse)
      root = tree.getroot()
    
    Or directly from a string: (xml is read already):
    '''
    try:
        root = ET.fromstring(pathToFile)
        if(root is  not None):
            for data in root.iter():
                if(data.text is not None):
                    stripped = data.text.strip()
                    if(stripped is not None) & (len(stripped)>2):
                        sentences = comm.replaceToPunkts(stripped)
                        for sentence in sentences:
                            getEntities.getEntities(xmlurl, sentence, ontologyData)
    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_xml.py " + xmlurl)
        pass

