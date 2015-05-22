#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 23, 2015
http://en.wikipedia.org/wiki/Cross-site_scripting
http://stackoverflow.com/questions/964459/how-to-remove-text-between-script-and-script-using-python
http://stackoverflow.com/questions/590747/using-regular-expressions-to-parse-html-why-not
'''
# enable debugging
import cgitb
cgitb.enable()


import getEntities
import commonVariables as comm
from lxml.html import parse



def readHtmlPage(htmlurl, readedPage, ontologyData, _encoding):
    try:
        sentences = set()
        root = parse(htmlurl).getroot()

        for element in root.iter("head"):
            element.drop_tree()
        for element in root.iter("script"):
            element.drop_tree()
        for element in root.iter("style"):
            element.drop_tree()
        for element in root.iter("noscript"):
            element.drop_tree()
        for element in root.iter("input"):
            element.drop_tree()
        for element in root.iter("form"):
            element.drop_tree()
        for element in root.iter("title"):
            element.drop_tree()
        for element in root.iter("img"):
            element.drop_tree()
            
        for element in root.iter("body"):
            try:
                sentences.add(element.text_content())
            except:
                pass
        if(len(sentences) > 0): 
            lsent = list(sentences)
            for lau in lsent:
                if(lau != ""):
                    laused = comm.replaceToPunkts(lau)
                    for s6ne in laused:
                        getEntities.getEntities(htmlurl, s6ne.strip(), ontologyData)
    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_html.py " + _encoding + " " + htmlurl)
        pass
    


