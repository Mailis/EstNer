#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
import os.path, os
import time, collections
import hashlib
import linecache
import sys, stat, re
import codecs
import json

# enable debugging
import cgitb
cgitb.enable()


if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')


chunksize=60

'''
    Lists file types, where one cannot find entities
'''
desiredFileTypes = ['excel', 'json', 'html', 'xml', 'pdf', 'plain', 'text']#
undesiredFileTypes = ['image', 'no-type', 'javascript', 'flash', 'dns', 'ttf']
undesiredFileExtensions = ['jpg', 'jpeg', 'gif', 'png', 'bmp', 'ico', 'swf', 'js', 'css', 'js', 'css', 'ShockwaveFlash', 'dns', 'ttf']
undesiredFileName = ['robots.txt', '/robots.txt']

'''
    Directories and paths so save rdf-files, errors, statistics etc.
'''
timeDir = time.strftime("%d_%m_%Y")
#some target paths for saving

downloadsDir = "downloaded_files/"+timeDir+"/"
if (not os.path.isdir(downloadsDir)) & (not os.path.exists(downloadsDir)):
    os.makedirs(downloadsDir)

jsonsDir = "downloaded_jsons2"

pathToRDFdir = "rdf_files/"

processed_logfiles_dir = "statistics/processed_logfiles/"
processed_logfiles_path = "proc_log_files.txt"
#############
errorsBucket = "generated_errors2"

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


def replaceToPunkts(s6ne):
    sentences = set()
    prune1 = s6ne.strip().replace('\n', ' ').replace('\t', ' ').replace('&nbsp;', ' ')
    multiSpaces="\s{2,}"
    prune2 = re.sub(multiSpaces, ' ', prune1)
    prune3 = prune2.replace(';', '.').replace(':', '.').replace('(', '.').replace(')', '.').replace('?', '.').replace('!', '.').replace(',', '.').replace(' | ', '.').replace('|', '.').replace('/', '.').replace('\\', '.').replace('{', '.').replace('}', '.').replace('[', '.').replace(']', '.').replace('¬', '.').replace('_', '.').replace('~', '.').replace('#', '.').replace('%', '.').replace('`', '.').replace('"', '.').replace('<', '.').replace('>', '.').replace('=', '.').replace('+', '.')
    laused = prune3.split(".")
    for s6n in laused:
        if re.match("^[a-zA-Z0-9_äöüõÕÜÖÄ]*$", s6n)
            if(len(s6ne) > 2) & (not is_number(s6ne)):
                sentences.add(s6ne)
    return list(sentences)
