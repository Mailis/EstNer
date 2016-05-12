#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 22, 2015
http://lxml.de/lxmlhtml.html
'''
import time
import read_eksel, read_json, read_html, read_xml, read_pdf, read_plaintext
import commonVariables as comm


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
    #od = initRdf.OntologyData('/var/www/html/mag/rdf_files/')
    #initRdf.RdfFilesCreator(od)
    doctext = httpResponse#detectEncoding(_encoding, httpResponse)
    '''#parse excel file'''
    if("excel" in tyyp.lower()):
        '''#parse web page excel'''
        read_eksel.readExcel(filePath, url, od)
    elif("xml" in tyyp.lower()):
        #print(tyyp)
        '''#parse web page xml'''
        doctext = detectEncoding(_encoding, httpResponse)
        read_xml.readXml(url, doctext, od)
    elif("html" in tyyp.lower()) :
        '''#parse web page html/txt'''
        doctext = detectEncoding(_encoding, httpResponse)
        read_html.readHtmlPage(url, doctext, od)
    elif("json" in tyyp.lower()):
        '''#parse json app/json'''
        doctext = detectEncoding(_encoding, httpResponse)
        read_json.readJson(url, doctext, od)
    elif("pdf" in tyyp.lower()):
        '''#parse pdf'''
        read_pdf.readPdf(url, doctext, od)
    elif("plain" in tyyp.lower()) or ("text" in tyyp.lower()):
        doctext = detectEncoding(_encoding, httpResponse)
        '''#assumes incoming is plain text try to parse text lines'''
        read_plaintext.readPlainText(url, doctext, od)
    else:
        jf = open(comm.pathToSaveParsingErrors, 'a',  encoding='utf-8')
        jf.write(time.strftime("%d/%m/%Y_%H:%M:%S") + " " + url + " " + "The_parser_for_the_type_" + tyyp + "_is_not_implemented\n")
        jf.close()


