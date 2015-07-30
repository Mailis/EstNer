#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()
'''
Created on Feb 22, 2015
http://lxml.de/lxmlhtml.html
'''
import sys
import read_eksel, read_json, read_html, read_xml, read_pdf, read_plaintext
from storage import commonvariables as comm


def detectEncoding(_encoding, httpResponse):
    doctext = httpResponse
    
    try:
        doctext = httpResponse.encode(_encoding).decode(sys.stdout.encoding)
    except:
        pass
   
    return doctext

'''
    compulsory inputs are web source url(html or xls or...) and file type
    this function uses different parsers for every file type
'''

def spreadURLsByContentType(url, httpResponse, tyyp, od, _encoding, filePath = None):
    doctext = httpResponse
    '''#parse excel file'''
    if("excel" in tyyp.lower()):
        try:
            '''#parse web page excel'''
            read_eksel.readExcel(filePath, url, od)
        except:
            comm.printException(comm.pathToSaveParsingErrors, "fileparser_excel")
            pass
            
    elif("xml" in tyyp.lower()):
        try:
            '''#parse web page xml'''
            doctext = detectEncoding(_encoding, httpResponse)
            read_xml.readXml(url, doctext, od)
        except:
            comm.printException(comm.pathToSaveParsingErrors, "fileparser_xml")
            pass
    elif("html" in tyyp.lower()) :
        try:
            '''#parse web page html/txt'''
            doctext = detectEncoding(_encoding, httpResponse)
            read_html.readHtmlPage(url, doctext, od, _encoding)
        except:
            comm.printException(comm.pathToSaveParsingErrors, "fileparser_html")
            pass
    elif("json" in tyyp.lower()):
        try:
            '''#parse json app/json'''
            doctext = detectEncoding(_encoding, httpResponse)
            read_json.readJson(url, doctext, od, _encoding)
        except:
            comm.printException(comm.pathToSaveParsingErrors, "fileparser_json")
            pass
    elif("pdf" in tyyp.lower()):
        try:
            '''#parse pdf'''
            read_pdf.readPdf(url, doctext, od)
        except:
            comm.printException(comm.pathToSaveParsingErrors, "fileparser_pdf")
            pass
    elif("plain" in tyyp.lower()) or ("text" in tyyp.lower()):
        try:
            doctext = detectEncoding(_encoding, httpResponse)
            '''#assumes incoming is plain text try to parse text lines'''
            read_plaintext.readPlainText(url, doctext, od, _encoding)
        except:
            comm.printException(comm.pathToSaveParsingErrors, "fileparser_plainText")
            pass
    else:
        comm.printException(comm.pathToSaveParsingErrors, "The_parser_for_the_type_" + tyyp + "_is_not_implemented\n")



