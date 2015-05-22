#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()


#print("Content-Type: text/plain;charset=utf-8")

'''
Created on Feb 24, 2015
'''

import socket
import os, sys, json, time
from multiprocessing import Pool

import init_rdf
import download_files_from_log
import datetime
from urllib.parse import unquote
from urllib.request import urlsplit
from urllib.request import urlretrieve as urr
from os import listdir

import commonvariables as comm 


def isNeededUrl(url):
    neededUrl = True
    fileName =  ((((urlsplit(url).path).lower()).split("/"))[-1]).lower()
    if(fileName in comm.undesiredFileName):
        neededUrl = False
    if(neededUrl):        
        extSplit = (fileName.split("."))
        lastIndex = len(extSplit)-1
        if(lastIndex > 0):
            extension = (extSplit[lastIndex])
            if(extension in comm.undesiredFileExtensions):
                neededUrl = False
    if(neededUrl):
        for udft in comm.undesiredFileTypes:
            if(udft in fileName):
                neededUrl = False
                break
    return neededUrl

'''
'''

def sendUrl(url):
    download_files_from_log.saveMetadata(url, od)

def downloadFromJsons():
    jsons=comm.jsonsDir
    for filePath in listdir(jsons):
            if(filePath != "errors.txt"):
                #open json file
                try:
                    loadisSuccsessful = 1
                    try:
                        jsonToDict = json.load(open(jsons+filePath));
                    except:
                        loadisSuccsessful = 0
                        errString="Loading json for data download error"
                        comm.printException(comm.pathToSaveDownloadErrors, filePath, errString)
                        pass
                    if (loadisSuccsessful == 1):
                        base_url = jsonToDict['base_url']#becomes folderName
                        for fname_key in jsonToDict.keys():
                            if (fname_key != 'base_url'):#fname_key(sha of file url) becomes local filename
                                for csha in jsonToDict[fname_key].keys():
                                    #excel type is already downloaded
                                    if("excel" not in jsonToDict[fname_key][csha]['Content-Type']):
                                        file_url = jsonToDict[fname_key][csha]['file_url']
                                        timeDir = jsonToDict[fname_key][csha]['timeDir']
                                        dirPath = comm.downloadsDir + base_url + "/"
                                        try:
                                            #create dir if does not exist
                                            if (not os.path.isdir(dirPath)) & (not os.path.exists(dirPath)):
                                                os.makedirs(dirPath)
                                            try:
                                                urr(file_url, dirPath + fname_key)
                                                #print(timeDir, base_url, , file_url)
                                            except:
                                                comm.printException(comm.pathToSaveDownloadErrors, filePath)
                                                pass
                                        except:
                                            comm.printException(comm.pathToSaveDownloadErrors, filePath)
                                            pass
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, filePath)
                    pass

'''
http://crawler.archive.org/articles/user_manual/glossary.html#discoverypath
logfile row structure description:
line[0] timestamp
line[1] status code
line[2] size of the downloaded document in bytes
line[3] url of downloaded file (document)
line[4]
  R - Redirect
  E - Embed
  X - Speculative embed (aggressive/Javascript link extraction)
  L - Link
  P - Prerequisite (as for DNS or robots.txt before another URI)
line[5] basic url, reference
line[6] content type of basic url, line[5]
line[7] the id of the worker thread that downloaded this document
line[8] timespan+download_time, diff to line[0]
line[9] sha1
line[10] -
line[11] content-size

#there is only line[3] and line[5] that are needed
#there is content-type only for line[5] given
#content type for line[3] has to be asked while making request
'''
       
nrOfJobs=""
logfileName ="logifaili nimi"

'''
'''
od = init_rdf.OntologyData(comm.pathToRDFdir)
init_rdf.RdfFilesCreator(od)
'''
'''

start = datetime.datetime.now()


timeDir = time.strftime("%d_%m_%Y")+ "/"
'''
piddir="processs/" + timeDir
if (not os.path.isdir(piddir)) & (not os.path.exists(piddir)): 
    os.makedirs(piddir)
'''

if __name__ == "__main__":
    #print(sys.argv[1])
    #print(datalist)
    #typed = (type(datalist) is dict)
    data = json.loads((json.loads(sys.argv[1]))["data"])
    #data = sys.argv[1]
    
    jobs = list(data.values())
     
    nrOfJobs=len(jobs)
    pool = Pool(processes=os.cpu_count())
    pool.map(sendUrl, jobs)
    pool.close()
    pool.join()
   

#FINALLY add triples from lists, that left over. 
#In the file 'getEntities',
#when chunking shared lists, it starts to create RDF-s, when list size exceeds chunksize (e.g. 25 items),
#but when there are eventually less items in lists than chunksize, the items in it were not tripled so far.
#print("PER")

if(od.sharedList_per._callmethod('__len__') > 0):
    #print(od.sharedList_per._callmethod('__len__'))
    try:
        perManager = init_rdf.PeopleManager(od)
        perManager.addTriples(od.sharedList_per)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_ORG_entities")
        pass


if(od.sharedList_org._callmethod('__len__') > 0):
    #print(od.sharedList_org._callmethod('__len__'))
    try:
        orgManager = init_rdf.OrganizationManager(od)
        orgManager.addTriples(od.sharedList_org)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_ORG_entities_leftover")
        pass

if(od.sharedList_loc._callmethod('__len__') > 0):
    #print(od.sharedList_loc._callmethod('__len__'))
    try:
        locManager = init_rdf.LocationManager(od)
        locManager.addTriples(od.sharedList_loc)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_LOC_entities_leftover")
        pass







