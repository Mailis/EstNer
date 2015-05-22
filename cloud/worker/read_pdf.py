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
from io import BytesIO
import commonvariables as comm

#readdedpdf = (ur.urlopen(url).read())
def readPdf(url, readdedpdf, od):
    b = BytesIO(readdedpdf)
    pdfFile = PdfFileReader(b, "rb")
    pdfFile.strict = False
    #pdfFile = PdfFileReader("pdf-sample.pdf", "rb")
    
    #print(pdfFile)
    try:
        for i in range(pdfFile.numPages):
            #print(i)
            pageObject = pdfFile.getPage(i)#ContentStream(pdfFile.getPage(i)["/Contents"])
            text = (pageObject.extractText())
            sentences = comm.replaceToPunkts(text)
            for sentence in sentences:
                if(len(sentence) > 2) & (not comm.is_number(sentence)):
                    getEntities.getEntities(url, sentence, od)
    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_pdf.py " + url)
        pass




