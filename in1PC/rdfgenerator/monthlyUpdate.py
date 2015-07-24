#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

from multiprocessing import Pool
import os
from os import walk
from urllib import request as ur
from urllib.parse import urlparse
import json
import time
import datetime
import hashlib
import initRdf
import commonVariables as comm
import downloadFilesFromLog as dffl
import commonMethods as commeth
import fileparser


monthly_updates_dir = "../statistics/monthly_updates"
if not os.path.isdir(monthly_updates_dir):
    os.makedirs(monthly_updates_dir)
monthly_updates_path = monthly_updates_dir + "/" + time.strftime("%d_%m_%Y") + ".txt"

start = datetime.datetime.now()
currTime = time.strftime("%d/%m/%Y_%H:%M:%S")
timedir = comm.timeDir
nrOfDownloads = commeth.nrOfDownloads

def addChangedContent(jsonFilePath):
    nrOfChanges = 0
    existingFileDict = dict()
    isValidJsonFile=True
    try:
        #open json file
        existingFileDict = json.load(open(jsonFilePath))
    except:
        isValidJsonFile=False
    
    if(isValidJsonFile):
        #hash is sha224
        for key in existingFileDict.keys():
            #if key is currently not a base_url, it is filenamef
            #filename can contain one or more  content SHAs
            if(key != 'base_url'):#key is sha of file's URL, elsewhere saved into variable localFilename 
                #structure:
                #sha of filename
                ###sha of file content
                ######metadata of file + (filename , sha(file content), human-readable file url, accessed date) 
                ###sha of file another (updated) content
                ######metadata...
                fileSHAs = list(existingFileDict[key].keys())#list of SHA's of file content at time of accessing this file
                arbitrFileSha = fileSHAs[0]#this is only for getting file URL
                fileUrl = existingFileDict[key][arbitrFileSha]["file_url"]
                canOpenUrl = True
                page=0
                try:
                    page = ur.urlopen(fileUrl)
                except:
                    break
                if(page!=0):
                    pageread = page.read()
                    fileContentSha224 = (hashlib.sha224(pageread).hexdigest())
                    #check if content is changed meanwhile
                    if(fileContentSha224 not in fileSHAs):#data has changed!!!
                        pageInfo = dict(page.info())
                        statusCode = page.getcode()
                        page.close()
                        contentType = comm.getContentType(pageInfo)
                        _encoding = commeth.getDocumentEncoding(contentType)
                        isDesiredType = comm.isDesiredContent(contentType)
                        if(isDesiredType):
                            #>localFilename = sha224(fileURL/filename) is key
                            newDataDict = dffl.insertNewContentToDict(key, fileUrl, pageInfo, fileContentSha224, statusCode)
                            if(newDataDict):
                                nrOfChanges += 1
                                existingFileDict[key].update(newDataDict)
                                baseUrl = existingFileDict["base_url"]
                                pathToSaveMetadata = comm.jsonsDir + baseUrl + ".json"
                                dffl.saveJsonToFile(pathToSaveMetadata, existingFileDict)
                                #send the file to parser: 
                                dffl.sendFileToParser(contentType, baseUrl, fileUrl, od, _encoding, key, pageread)
                                return int(nrOfChanges)
                    else:
                        page.close()
    return 0
                
#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#

nrOfJobs = 0 
if __name__ == "__main__":   
    
    try:
        od = initRdf.OntologyData(comm.pathToRDFdir)
        initRdf.RdfFilesCreator(od)
        jsons=comm.jsonsDir
        jobs = []
        #jsonsList = list of jsonfiles, where the metadata for downloaded files are saved 
        jsonsList = []
        dirpath = ""
        for (dirpath0, dirnames, filenames) in walk(jsons):
            dirpath = dirpath0
            jsonsList.extend(filenames) #collect all json-files into list
            break
        for filename in jsonsList:
            jobs.append(dirpath+filename)
            nrOfJobs += 1
             
        #pool of processes
        pool = Pool(processes=os.cpu_count())
        #search for changes
        nrOfChanges_ = pool.map(addChangedContent, jobs)
        
        pool.close()
        pool.join()
    except:
        comm.printException(comm.updateErrorsFilePath, errString="update")
        pass
    
    
#import getpass
#print("USER: " + getpass.getuser())
#save statistics of monthly updates!

end = datetime.datetime.now() 
span = end-start##
try:
   jf = open(monthly_updates_path, 'a', encoding='utf-8')
   jf.write(currTime + " " + str(nrOfJobs) + " " + str(span) + " " + str(comm.chunksize) + " " + str(sum(nrOfChanges_)) + " ")
   jf.close()
except:
   comm.printException(comm.updateErrorsFilePath, errString="update")
   pass
''''''
try:
    commeth.measureDownloadsTime(monthly_updates_path, timedir)
except:
   comm.printException(comm.updateErrorsFilePath, errString="update")
   pass




