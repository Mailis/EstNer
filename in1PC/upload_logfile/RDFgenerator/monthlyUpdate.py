#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

from multiprocessing import Pool
import os
from os import listdir
from urllib import request as ur
from urllib.parse import urlparse
import json
import time
import datetime
import hashlib
import initRdf
import commonVariables as comm
import downloadFilesFromLog as dffl
import fileparser



def addChangedContent(jsonFilePath):
    existingFileDict = json.load(open(jsonFilePath));
    #rasi is sha224
    for key in existingFileDict.keys():
        #if key is currently not a base_url, it is filename
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
            
            page = ur.urlopen(fileUrl)
            pageread = page.read()
            fileContentSha224 = (hashlib.sha224(pageread).hexdigest())
            #check if content is changed meanwhile
            if(fileContentSha224 not in fileSHAs):#data has changed!!!
                pageInfo = dict(page.info())
                statusCode = page.getcode()
                page.close()
                contentType = comm.getContentType(pageInfo)
                isDesiredType = comm.isDesiredContent(contentType, od)
                if(isDesiredType):
                    #>sha224(localFilename) is key
                    newDataDict = dffl.insertNewContentToDict(key, fileUrl, pageInfo, fileContentSha224, statusCode)
                    if(newDataDict):
                        existingFileDict[key].update(newDataDict)
                        baseUrl = existingFileDict["base_url"]
                        succ = dffl.downLoadFile(pageread, key, baseUrl)
                        if(succ):#... save metadata for downloaded file
                            pathToSaveMetadata = comm.jsonsDir + baseUrl + ".json"
                            dffl.saveJsonToFile(pathToSaveMetadata, existingFileDict)
                            #after downloading send the file to estner: 
                            if("excel" in contentType):
                                fileparser.spreadURLsByContentType(fileUrl, None, contentType, od, filePath = succ)
                            else:
                                fileparser.spreadURLsByContentType(fileUrl, pageread, contentType, od)
            else:
                page.close()
                
#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''#''''''''''''

start = datetime.datetime.now()
nrOfJobs=""
if __name__ == "__main__":    
    try:
        od = initRdf.OntologyData('/var/www/html/mag/rdf_files/')
        initRdf.RdfFilesCreator(od)
        
        jsons=comm.jsonsDir
        jobs = []
        
        #fList = list of jsonfiles, where the metadata for downloaded files are saved 
        for filename in listdir(jsons):
            if(filename != "errors.txt"):
                jobs.append(jsons+filename)
            
        nrOfJobs=str(len(jobs))
        pool = Pool(processes=os.cpu_count())
        pool.map(addChangedContent, jobs)
    except Exception as e:
        comm.printException(comm.updateErrorsFilePath, errString="update")
    
    

#save statistics of monthly updates!
monthly_updates_dir = "../../statistics/monthly_updates/"
if not os.path.isdir(monthly_updates_dir):
        os.makedirs(monthly_updates_dir)
monthly_updates_path = monthly_updates_dir + time.strftime("%d_%m_%Y") + ".txt"
end = datetime.datetime.now() 
span = end-start
#print("SPAN: ", span)  
#print("totalseconds: ", span.total_seconds())  
jf = open(monthly_updates_path, 'a', encoding='utf-8')
jf.write(time.strftime("%d/%m/%Y") + " " + nrOfJobs + " " + str(span) + " " + str(comm.chunksize) + "\n")
jf.close()




