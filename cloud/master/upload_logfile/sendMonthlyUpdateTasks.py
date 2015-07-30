#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import os
from os import walk
import hashlib
import time
import datetime
import subprocess
import json
import requests
import postToWorker
import commonVariables as comm
import importRemoteFiles
import downloadDocs

WORKER_INSTANCES = []
worker_counter = 0
nrOfChanges = 0

#path for saving monthly update statistics
monthly_updates_dir = comm.monthly_updates_dir
#one time-named directory for all json-files
timedir = comm.timeDir


                



     

    
'''  
'''  
def importRDFfiles():
    global WORKER_INSTANCES
    list_len = len(WORKER_INSTANCES)
    #print("WORKERS " + str(WORKER_INSTANCES))
    try:
        if list_len > 0:
            for instance in WORKER_INSTANCES:
                wwwname = instance['name']
                wwwip = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
                www_data = dict()
                www_data["ip"] = wwwip
                www_data["name"] = wwwname
                www_data["statfile"] = ""
                subprocess.Popen(["python3", comm.parentDir + "upload_logfile/download_rdf_files.py", json.dumps(www_data)])
        else:
            comm.printException(comm.updateErrorsFilePath, errString='No instances to list.')
    except:
        comm.printException(comm.updateErrorsFilePath, errString='Importing_RDFs.')
                

            
#start to search for changed content,
#comparing content hash saved in json-file to the 
#content of web document at current moment
def detectChanges(jsonFilePath, listOfUrls):
    global nrOfChanges
    global worker_counter
    #print(jsonFilePath)
    #print("--------------------")
    #print(str(len(listOfUrls)))
    #print("--------------------")
    jsonDict = dict()
    #json-files may be incorrectly formed,
    #in that case one cannot load it into dictionary
    isValidJsonFile=True
    try:
        #open json file
        #load file into dictionary-type:
        jsonDict = json.load(open(jsonFilePath))
    except:
        isValidJsonFile=False
        pass
    #print(str(isValidJsonFile))
    #get URL from the current dict
    if(isValidJsonFile):
        #hash is sha224
        for key in jsonDict.keys():
            #if key is currently not a base_url, it is filename
            #under filename-key, there can be among other metadata
            #one or more  content SHAs
            #URL to that file (document) in web
            if(key != 'base_url'):#key is sha of file's URL, elsewhere saved into variable localFilename 
                #structure:
                #sha of filename
                ###sha of file content
                ######metadata of file + (filename , sha(file content), 
                ###### human-readable file url (under key 'file_url'), accessed date) 
                ###sha of file another (updated) content
                ######metadata...
                fileSHAs = list(jsonDict[key].keys())#list of SHA's of file content at time of accessing this file
                arbitrFileSha = fileSHAs[0]#this is only for getting file URL
                fileUrl = jsonDict[key][arbitrFileSha]["file_url"]
                redirectedTo=0
                try:
                    redirectedTo = requests.get(fileUrl).url
                except:
                    comm.printException(comm.updateErrorsFilePath, errString="open_url")
                    continue #continue with next URL in loop
                if(redirectedTo!=0):
                    #print(str(redirectedTo))
                    #read the doc's content at current moment
                    try:
                        pageread = (requests.get(redirectedTo)).text
                    except:
                        comm.printException(comm.updateErrorsFilePath, errString="pageread1")
                        try:
                            pageread = ((requests.get(redirectedTo)).text.encode('utf-8').strip())
                        except Exception as e:
                            comm.printException(comm.updateErrorsFilePath, errString="pageread2")
                            print(e)
                            continue
                    #get hash of this doc
                    fileContentSha224 = (hashlib.sha224(pageread.encode('utf-8')).hexdigest())
                    #check if content is changed meanwhile
                    if(fileContentSha224 not in fileSHAs):#data has changed!!!
                        #collect number of changes
                        nrOfChanges += 1
                        #as a content of this doc has changed, send its URL to the worker
                        #for extracting entities
                        #fill the list of URLs
                        listOfUrls.append(fileUrl)
                        ''''''
                        postListSize = postToWorker.defPostListSize(worker_counter, ipList_tuple)
                        #send certain amount of URLs to each worker, then empty the list of URLS
                        if(len(listOfUrls) == postListSize):
                            #send list of urls to worker
                            worker_counter = postToWorker.detectConnection(ipList, worker_counter, listOfUrls)
                            #empty list of object names
                            #to prepare it for the next worker
                            del listOfUrls[:] 
                            #prepare next worker
                            worker_counter += 1
                            if (worker_counter > (len(ipList)-1)):#last worker in the workers list
                                #start over from first worker in the workers list
                                worker_counter = 0
                        
    
'''    
'''
def makePostProcessDownloads():
    global WORKER_INSTANCES
    start = datetime.datetime.now()
    currTime = time.strftime("%d/%m/%Y_%H:%M:%S")
    importRDFfiles()
    end = datetime.datetime.now()
    downloadDocs.saveUpdateStatistics(currTime, start, end, action="download_RDFs")
    
    start = datetime.datetime.now()
    currTime = time.strftime("%d/%m/%Y_%H:%M:%S")
    importRemoteFiles.importExcelFiles(WORKER_INSTANCES)
    end = datetime.datetime.now()
    downloadDocs.saveUpdateStatistics(currTime, start, end, action="download_Excels")
    

                        
def getListOfWorkerIPs(worker_instances):
    for instance in worker_instances:
        #get nr of CPUs in this VM
        cpuAmount = (((instance['machineType'])).split("/")[-1])[-1]
        accessConfigs = instance['networkInterfaces'][0]['accessConfigs'][0]
        if ("natIP" in accessConfigs):
            #save IP and respective cpu amount into tuple
            ip = accessConfigs["natIP"]
            ipList.append(ip)
            ipList_tuple.append(ip, cpuAmount)
    return (ipList, ipList_tuple)
    
    
    
if __name__ == '__main__':
    worker_counter = 0
    try:
        #list for collecting IP-addresses of workers
        ipList = []
        ipList_tuple = []
        #collect nr of changed contents into variable 'nrOfChanges'
        nrOfChanges = 0
        #save starting time for measuring how much time the process takes
        #this is later saved into '../statistics/monthly_updates/<logfilename>.txt'
        start = datetime.datetime.now()
        currTime = time.strftime("%d/%m/%Y_%H:%M:%S")
        #dir of json-files
        jsonFiles=comm.jsonsDir_local
        try:
            p = subprocess.Popen(["python2", comm.parentDir + "upload_logfile/getworkers.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            #print((out.decode()))
            WORKER_INSTANCES = json.loads(out.decode())
            #print(WORKER_INSTANCES)
            #tuple of ip list and list of tuple of ip and amount of cpus
            ipList_and_tuple = getListOfWorkerIPs(WORKER_INSTANCES)
            ipList = ipList_and_tuple[0]
            ipList_tuple = ipList_and_tuple[1]
        except Exception as e:
            comm.printException(comm.updateErrorsFilePath, errString="subprocess_to_getworkers.py" + str(e))
            pass
        #if there is at least 1 ip n the list
        lenIpList = len(ipList)
        
        
        if (lenIpList>0):
            #the list of doc URLs that is going to send to worker
            listOfUrls = []
            #loop over all json-files
            for (dirpath, dirnames, filenames) in walk(jsonFiles):
                for fname in filenames:
                    #start to search for changed content,
                    #comparing content hash saved in json-file to the 
                    #content of web document at current moment
                    #print(os.path.join(dirpath, fname))
                    jsonpath = ""
                    try:
                        jsonpath = os.path.join(dirpath, fname)
                    except:
                        comm.printException(comm.updateErrorsFilePath, errString="make_jsonpath")
                        break
                    if(jsonpath is not ""):
                        try:
                            detectChanges(os.path.join(dirpath, fname), listOfUrls)
                        except:
                            comm.printException(comm.updateErrorsFilePath, errString="start_detect")
            
            #post rest of the list to the worker
            if(len(listOfUrls) > 0):
                #if this was the last worker, use first in workers list, else use next
                if(worker_counter == (len(ipList)-1)):#last worker was recently used
                    worker_counter = 0
                else:
                    worker_counter += 1
                 
                #send list of object names to worker    
                worker_counter = postToWorker.detectConnection(ipList, worker_counter, listOfUrls)
                
            else:
                comm.printException(comm.updateErrorsFilePath, errString="no_json-files_for_updating")
            
            #save finishing time of update process for measuring how much time the process took
            end = datetime.datetime.now()
            span = end-start
            try:
                jf = open(comm.monthly_updates_path, 'a')
                jf.write("update-process " + currTime + " " + str(span) + " " + str(nrOfChanges) + " " + str(lenIpList) + " ")
                jf.close()
            except:
                comm.printException(comm.updateErrorsFilePath, errString="update")
                pass
            
            
            #download updated RDFs and excel-files
            makePostProcessDownloads()
            #download new json-files and error-files
            
            start = datetime.datetime.now()
            currTime = time.strftime("%d/%m/%Y_%H:%M:%S")
            try:
                p = subprocess.Popen(["python2", comm.parentDir + "upload_logfile/post_update_downloads.py"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
            except Exception as e:
                comm.printException(comm.updateErrorsFilePath, errString="POSTUPDATEerror_" + str(e))
                pass
            end = datetime.datetime.now()
            downloadDocs.saveUpdateStatistics(currTime, start, end, action="download_errors_and_jsons")
            #download updated datasets
            downloadDocs.downloadDocuments(timedir)
            
            ###
            ###
            #delete RDF-files and download excel-files in each worker
            postToWorker.deleteRDFsInWorkers(ipList)
           
        else:
            comm.printException(comm.updateErrorsFilePath, errString='No_instances_to_list.')
        
        
    except:
        comm.printException(comm.updateErrorsFilePath, errString="update_main")
        pass
        

    
    