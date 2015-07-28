#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()


import os, sys, json
import time
import datetime
from urllib.request import urlretrieve as urr
from os import listdir
import json
import commonVariables as comm 

nrOfDownloads = 0

def dowloadFromJsons(ajadir):
    nrOfDownloads = 0
    jsons=comm.jsonsDir
    """loop over every file in jsons-folder"""
    for filePath in listdir(jsons):
            if(filePath != "errors.txt"):
                #open json file:
                #'jsons' is a folder where json-files are saved
                #'filePath' is a filename in this folder
                ##'jsons'-folder lives in the folder "datadownload"
                ##'downloaded_files'-folder lives also in the folder "datadownload"
                try:
                    """load json-file into directory-type"""
                    jsonToDict = json.load(open(jsons+filePath));
                except:
                    continue
                #'base_url' is the hostname, before "/"-slashes, in json-file
                #'base_url' is the json-file name ('filePath'), followed by an extension '.json'
                #'base_url' is also a directory name in 'downloaded_files'-folder
                base_url = jsonToDict['base_url']#becomes folderName
                for fname_key in jsonToDict.keys():
                    #At first level, there are two sorts of keys in json-file:
                    #1. base-url
                    #2. sha(s) of filename(s), (sha of file full url, including "/"-slashes)
                    ##As the file content may change over time, every sha(filename)-element contains
                    ##1. sha(s) of a content(s)
                    ###Every sha of a content contains
                    ###1. metadata of a file/content
                    if (fname_key != 'base_url'):#fname_key(sha of file url) becomes local filename
                        #'jsonToDict[fname_key].keys()' is a list of sha(content) of a current sha(filename)
                        #loop over every sha(content) of a sha(filename)
                        #here, csha is the sha(filecontent)
                        for csha in jsonToDict[fname_key].keys():
                            contentKeyExists=False
                            """check if metadata contains key 'Content-Type'"""
                            try:
                               if ('Content-Type' in jsonToDict[fname_key][csha]):
                                   contentKeyExists=True
                            except:
                                contentKeyExists=False
                                pass
                            """Get the time the json-file was made"""
                            timeDir = jsonToDict[fname_key][csha]['timeDir']
                                                   #download only today's changes!
                            if(contentKeyExists) & (ajadir == timeDir):
                                #excel type is already downloaded
                                if("excel" not in jsonToDict[fname_key][csha]['Content-Type']):
                                    """Full URL of a file"""
                                    file_url = jsonToDict[fname_key][csha]['file_url']
                                    """'dirPath' is the path of a folder of a file currently wants to be downloaded"""
                                    dirPath = comm.downloadsDir + base_url + "/"
                                    try:
                                        """create folder for this 'date/base_url' if does not exist"""
                                        if (not os.path.isdir(dirPath)) & (not os.path.exists(dirPath)):
                                            os.makedirs(dirPath)
                                        try:
                                            #download the file into that folder
                                            #fname_key is the sha(filename)
                                            #resulting path of a file will become 'date/base_url/sha(filename)'
                                            urr(file_url, dirPath + fname_key)
                                            nrOfDownloads += 1
                                            #print(timeDir, base_url, , file_url)
                                            
                                        except:
                                            comm.printException(comm.pathToSaveDownloadErrors, filePath)
                                            pass
                                    except:
                                        comm.printException(comm.pathToSaveDownloadErrors, filePath)
                                        pass
    return nrOfDownloads



def measureDownloadsTime(path_to_stat_file, ajadir):
    start = datetime.datetime.now()
    currTime = time.strftime("%H:%M:%S")
    nrOfDownloads = dowloadFromJsons(ajadir)
    end = datetime.datetime.now() 
    span = end-start
    try:
        jf = open(path_to_stat_file, 'a', encoding='utf-8')
        jf.write(currTime + " " + str(nrOfDownloads) + " " + str(span) + " " + "\n")
        jf.close()
    except:
        comm.printException(comm.pathToSaveDownloadErrors, errString="download")
        pass


def getDocumentEncoding(contentType):
    _encoding = 'utf-8'
    contentTypeLower = contentType.lower().strip()
    if("charset" in contentTypeLower):
        #print("charset_ENCODING ", _encoding)
        encodSplit = contentTypeLower.split("=")
        encodIndex = len(encodSplit)-1
        if(len(encodSplit) > encodIndex):
            _encoding = encodSplit[encodIndex]
    return _encoding





