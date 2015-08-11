#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''        
escape xml-invalid charas:        
http://www.w3.org/TR/xml/#syntax        
http://stackoverflow.com/questions/1091945/what-characters-do-i-need-to-escape-in-xml-documents        
'''
import os
import time
import hashlib
import linecache
import sys, re
import codecs
import json
import chardet

# enable debugging
import cgitb
cgitb.enable()


if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')


chunksize=500

'''
    Lists file types, where one cannot find entities
'''
desiredFileTypes = ['excel', 'json', 'html', 'xml', 'pdf', 'plain', 'text']#
undesiredFileTypes = ['image', 'no-type', 'javascript', 'flash', 'dns', 'ttf', 'js', 'css', 'video', 'zip']
undesiredFileExtensions = ['jpg', 'jpeg', 'gif', 'png', 'bmp', 'ico', 'swf', 'js', 'css', 'php', 'ShockwaveFlash', 'dns', 'ttf']
undesiredFileName = ['robots.txt', '/robots.txt', 'xmlrpc.php']


'''
    Directories and paths so save rdf-files, errors, statistics etc.
'''
parentDir = "/var/www/html/"
timeDir = time.strftime("%d_%m_%Y")
#some target paths for saving

downloadsDir = parentDir + "downloaded_files/"+timeDir+"/"
if (not os.path.isdir(downloadsDir)) & (not os.path.exists(downloadsDir)):
    os.makedirs(downloadsDir)
#jsonsbucket
jsonsDir = "datadownload_jsons"

pathToRDFdir = parentDir + "rdf_files/"
#create folder for rdf-files
if not os.path.isdir(pathToRDFdir):
    os.makedirs(pathToRDFdir)  

processed_logfiles_dir = parentDir + "statistics/processed_logfiles/"
processed_logfiles_path = "proc_log_files.txt"
#############
errorsBucket = "generated_files"

##coonection errors object in bucket
dirToSaveConnectionErrors = "connection_errors/"
pathToConnectionErrors = dirToSaveConnectionErrors + timeDir + ".txt"

dirToSaveJsonErrors = "json_errors/"
pathToSaveJsonErrors = dirToSaveJsonErrors + timeDir + ".txt"

dirToSaveProgrammingErrors = "programming_errors/"
pathToSaveProgrammingErrors = dirToSaveProgrammingErrors + timeDir + ".txt"

dirToSaveDownloadErrors = "download_errors/"
pathToSaveDownloadErrors = dirToSaveDownloadErrors + timeDir + ".txt"

pathToUpdateErrorsDir = "update_errors/"
updateErrorsFilePath = pathToUpdateErrorsDir + timeDir + ".txt"

pathToInitRdfErrorsDir = "tripling_errors/"
initRdfErrorsFilePath = pathToInitRdfErrorsDir + timeDir + ".txt"

parsing_errorsDir = "parsing_errors/"
pathToSaveParsingErrors = parsing_errorsDir + timeDir + ".txt"

if not os.path.isdir(dirToSaveConnectionErrors):
    os.makedirs(dirToSaveConnectionErrors) 
if not os.path.isdir(processed_logfiles_dir):
    os.makedirs(processed_logfiles_dir)
if not os.path.isdir(dirToSaveJsonErrors):
    os.makedirs(dirToSaveJsonErrors)   
if not os.path.isdir(dirToSaveProgrammingErrors):
    os.makedirs(dirToSaveProgrammingErrors)
if not os.path.isdir(dirToSaveDownloadErrors):
    os.makedirs(dirToSaveDownloadErrors)
if not os.path.isdir(pathToInitRdfErrorsDir):
    os.makedirs(pathToInitRdfErrorsDir)
if not os.path.isdir(pathToUpdateErrorsDir):
    os.makedirs(pathToUpdateErrorsDir)
if not os.path.exists(parsing_errorsDir):
    os.makedirs(parsing_errorsDir)


def getChardetEncoding(rawdata):
    ch = chardet.detect(rawdata)
    return (ch['encoding'])

def getDocumentEncoding(contentType, rawdata):
    _encoding = None
    if(contentType is None):
        _encoding = getChardetEncoding(rawdata)
        return _encoding

    contentTypeLower = contentType.lower().strip()
    if("charset" in contentTypeLower):
        #print("charset_ENCODING ", _encoding)
        encodSplit = contentTypeLower.split("=")
        encodIndex = len(encodSplit)-1
        if(len(encodSplit) > encodIndex):
            _encoding = encodSplit[encodIndex]
            return _encoding
    if(_encoding is None):
        _encoding = getChardetEncoding(rawdata)
    return _encoding


def getContentType(pageInfo):
    contentType = ""
    #there are literally different keys for content type:
    if("Content-Type" in pageInfo.keys()):
        contentType = pageInfo["Content-Type"]
    elif("Content-type" in pageInfo.keys()):
        contentType = pageInfo["Content-type"]
    elif("content-type" in pageInfo.keys()):
        contentType = pageInfo["content-type"]
    elif("content-Type" in pageInfo.keys()):
        contentType = pageInfo["content-Type"]
    elif("contentType" in pageInfo.keys()):
        contentType = pageInfo["contentType"]
    elif("contenttype" in pageInfo.keys()):
        contentType = pageInfo["contenttype"]
    elif("Contenttype" in pageInfo.keys()):
        contentType = pageInfo["Contenttype"]
    elif("Content type" in pageInfo.keys()):
        contentType = pageInfo["Content type"]
    elif("Content Type" in pageInfo.keys()):
        contentType = pageInfo["Content Type"]
    return contentType


def isDesiredContent(cType, od):
    isDesired = True
    isKnownType = False
    for ct in desiredFileTypes:
        if (ct in cType):
            isKnownType = True
            break

    if(not isKnownType):
        for ct in (undesiredFileTypes + undesiredFileExtensions):
            if (ct in cType):
                isDesired = False
                break
    return isDesired



def getUrlSHA(redirectedTo):
    return hashlib.sha224(redirectedTo.encode("utf-8")).hexdigest()



def printException(pathToErrorFile, errString=""):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    err= (time.strftime("%d/%m/%Y_%H:%M:%S") + " " + errString + ' {}_EXCEPTION_IN_({},_LINE_{}_"{}"):_{}_'.format(exc_type, filename, lineno, line.strip(), exc_obj) + "\n\n")
    #TODO!
    data_dict = dict()
    data_dict["bucket"] = errorsBucket
    data_dict["object"] = pathToErrorFile
    data_dict["errdata"] = err
    os.system('python2 storage/insertErrorObj.py ' + json.dumps(json.dumps(data_dict)))

    '''
    data_dict["folder"] = splittedPath[0]+"/"
    data_dict["filename"] = splittedPath[1]
    data.append(json.dumps(data_dict))
    jsn = json.dumps(data)
    os.system("python2 fabfile_test.py " + jsn)
    '''


def saveStatistics(note):
    data=[]
    data_dict = {}
    data_dict["data"] = note
    data_dict["folder"] = processed_logfiles_dir
    data_dict["filename"] = processed_logfiles_path
    data.append(json.dumps(data_dict))
    #send str repr
    jsn = json.dumps(data)
    os.system("python2 fabfile.py " + jsn)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
#dont process strings that contain illegal chars for xml
#http://stackoverflow.com/questions/1707890/fast-way-to-filter-illegal-xml-unicode-chars-in-python
def containsXMLinvalidchars(s6ne):
    includesIllegalChar = None
    _illegal_unichrs = [(0x00, 0x08), (0x0B, 0x0C), (0x0E, 0x1F), 
                        (0x7F, 0x84), (0x86, 0x9F), 
                        (0xFDD0, 0xFDDF), (0xFFFE, 0xFFFF)] 
    if sys.maxunicode >= 0x10000:  # not narrow build 
            _illegal_unichrs.extend([(0x1FFFE, 0x1FFFF), (0x2FFFE, 0x2FFFF), 
                                     (0x3FFFE, 0x3FFFF), (0x4FFFE, 0x4FFFF), 
                                     (0x5FFFE, 0x5FFFF), (0x6FFFE, 0x6FFFF), 
                                     (0x7FFFE, 0x7FFFF), (0x8FFFE, 0x8FFFF), 
                                     (0x9FFFE, 0x9FFFF), (0xAFFFE, 0xAFFFF), 
                                     (0xBFFFE, 0xBFFFF), (0xCFFFE, 0xCFFFF), 
                                     (0xDFFFE, 0xDFFFF), (0xEFFFE, 0xEFFFF), 
                                     (0xFFFFE, 0xFFFFF), (0x10FFFE, 0x10FFFF)]) 
    _illegal_ranges = ["%s-%s" % (chr(low), chr(high)) for (low, high) in _illegal_unichrs] 
    
    #_illegal_xml_chars_RE = re.compile('[%s]' % ''.join(_illegal_ranges)) 
    #return _illegal_xml_chars_RE.match(s6ne)
    for (low, high) in _illegal_unichrs:
        for x in range(low, high):
            if chr(x) in s6ne:
                return 1
            
    return None

def specialReplacements(s6ne):
    prune0 = s6ne.strip().replace('&amp;', ' ').replace('&quot;', ' ').replace('&apos;', ' ').replace('&lt;', ' ').replace('&gt;', ' ').replace('\n', ' ').replace('\t', ' ').replace('&nbsp;', ' ')
    multiSpaces="\s{2,}"
    prune1 = re.sub(multiSpaces, ' ', prune0)
    multiSpaces="-{2,}"
    prune2 = re.sub(multiSpaces, '-', prune1)
    prune3 = prune2.replace("Ãµ","õ").replace("Ã•","Õ").replace("Ã","Õ").replace("Ã¼","ü").replace("Ã", "Ü").replace("Ãœ", "Ü").replace("Ã¤","ä").replace("Ã„", "Ä").replace("Ã", "Ä").replace("Ã–", "Ö").replace("Ã¶","ö").replace("", "™")
    return prune3

def replaceWith(repl, s6ne):
    p = s6ne.replace("¦", repl).replace(';', repl).replace(':', repl).replace('(', repl).replace(')', repl)
    r = p.replace('?', repl).replace('!', repl).replace(',', repl).replace(' | ', repl).replace('&', repl)
    s = r.replace('@', repl).replace('˙', repl).replace('˚', repl).replace('ˇ', repl)
    t = s.replace('ˆ', repl).replace('/', repl).replace('\\', repl).replace('{', repl).replace('}', repl)
    u = t.replace('[', repl).replace(']', repl).replace('¬', repl).replace('_', repl).replace('~', repl)
    v = u.replace('#', repl).replace('%', repl)
    w = v.replace('<', repl).replace('>', repl).replace('=', repl).replace('+', repl).replace('*', repl)
    x = w.replace('˝', repl).replace('"', repl).replace('¨', repl).replace('»', repl).replace('`', repl)
    return x

def replaceToPunkts(s6ne):
    #set avoids double items
    sentences = set()
    prune3 = specialReplacements(s6ne)
    prune4 = replaceWith(".", prune3)
    laused = prune4.split(".")
    for s6n in laused:
        #s6ne = s6n.encode("utf-8")
        s6ne = str(s6n)#.encode('utf-8')
        #detect illegal chars for xml
        if(containsXMLinvalidchars(s6ne)is None):
        #if there is no letters:
            if(re.search('[a-zA-Z]', s6ne) is not None):
                if(len(s6ne) > 2): 
                    if(not is_number(s6ne)):
                        sentences.add(s6ne)
    return list(sentences)  