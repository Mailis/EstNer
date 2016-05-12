#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 26, 2015
http://pythonhosted.org//PyPDF2/
print(PyPDF2.__version__)
http://www.binpress.com/tutorial/manipulating-pdfs-with-python/167
http://stackoverflow.com/questions/9751197/opening-pdf-urls-with-pypdf
'''
# enable debugging
import cgitb
cgitb.enable()


import getEntities
from PyPDF2 import PdfFileReader
from urllib.request import urlretrieve as urldownl
from storage import commonvariables as comm

#readdedpdf = (ur.urlopen(url).read())
def readPdf(filePath, url, od):
    urldownl(url, filePath)
    pdf = PdfFileReader(open(filePath, "rb"))
    pdf.strict = True
 
    try:
        for page in pdf.pages:
            text = (page.extractText())
            sentences = comm.replaceToPunkts(text)
            for sentence in sentences:
                getEntities.getEntities(url, sentence, od)
    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_pdf.py " + url)
        pass




