#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import commonVariables as comm
import validationFuncs as valide
import importRemoteFiles
import os
from os import walk
import shutil
import io
import sys
import datetime
import subprocess
import json
import time
import postToWorker
from urllib import urlretrieve as urr
from oauth2client import client as oauth2_client
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from apiclient.http import MediaIoBaseDownload
import authenticate_gce
import downloadJsons
import downloadErrors



'''
The main task of this file is to 
parse log file rows and 
send tasks to worker instances and then 
collect generated data while 
saving statistics about actions and 
storing also thrown errors

logfile is explained at
http://crawler.archive.org/articles/user_manual/glossary.html#discoverypath

incoming logfile row structure description:
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

#there is only line[3], line[4] and line[5] that are needed
#there is content-type only for line[5] given
#content type for line[3] has to be asked while making request
'''

WORKER_INSTANCES = []

timeDir = comm.timeDir

#get the IP addresses of workers, google compute virtual machines
def getListOfWorkerIPs():    
    global WORKER_INSTANCES
    
    credentials = GoogleCredentials.get_application_default()
    compute = build('compute', 'v1', credentials=credentials)
    result = compute.instances().list(project=comm.PROJECT_ID, zone=comm.DEFAULT_ZONE).execute()
    all_INSTANCES = result['items']
    ipList = []
    ipList_tuple = []
    #print("MASTERINSTANCE_NAME " + MASTERINSTANCE_NAME + "\n\n")
    for instance in all_INSTANCES:
        wwwname = instance['name']
        if(wwwname != comm.MASTERINSTANCE_NAME):
            WORKER_INSTANCES.append(instance)
            accessConfigs = instance['networkInterfaces'][0]['accessConfigs'][0]
            #get nr of CPUs in this VM
            cpuAmount = (((instance['machineType'])).split("/")[-1])[-1]
            accessConfigs = instance['networkInterfaces'][0]['accessConfigs'][0]
            if ("natIP" in accessConfigs):
                #save IP and respective cpu amount into tuple
                ip = accessConfigs["natIP"]
                ipList.append(ip)
                ipList_tuple.append((ip, cpuAmount))
    return (ipList, ipList_tuple)


#process each line in log-file
#filters which one of two URLs to send to the worker:
#if column at index 4 does not contain X, it check whether it contains P
#if it contains P, it takes hostname-URL from column 5,  
#otherwise file-URL from column 3
def processline(line): 
    splitted = line.split()
    tyyp = (splitted[6]).lower()#content type
    
    
    if(valide.isValideType(tyyp)):
        action = splitted[4] 
        '''
        R - Redirect
        E - Embed
        X - Speculative embed (aggressive/Javascript link extraction)
        L - Link
        P - Prerequisite (as for DNS or robots.txt before another URI)
        '''
        #print(tyyp)
        #call parser for every line
        url = ""
        if "X" not in action:
            if "P" in action:#dns or robots.txt, send basic url
                url = splitted[5] #base_url aka host name
            else:#send url of file
                url = splitted[3] #file-path followed to host name 
                
        if(url != ""):
            neededUrl = valide.isNeededUrl(url)
            if(neededUrl):
                return url  
        else:
            return ""
        
       
 
#RDF files are imported from worker instances to the master instance, when 
#extracting entities and RDFizing is ready.
#As it uses a list of workers, this method also writes info about these into statistics-file
def importRDFfiles():
    global WORKER_INSTANCES
    inst_str = "number of log rows: " + str(nr_of_log_rows) + "\n"
    inst_str += "number of processed rows: " + str(line_counter) + "\n"
    inst_str += "length of POST list: " + str(postListSize) + "\n"

    list_len = len(WORKER_INSTANCES)
    inst_str += "number of worker instaces: " + str(list_len) + "\n" 
    #print("WORKERS " + str(WORKER_INSTANCES))
    if list_len > 0:
        for instance in WORKER_INSTANCES:
            wwwname = instance['name']
            inst_str += "\nworkername: " + wwwname + "\nmachineType: " + instance['machineType'] + "\n"
            wwwip = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            www_data = dict()
            www_data["ip"] = wwwip
            www_data["name"] = wwwname
            www_data["statfile"] = mylargefile
            p = subprocess.Popen(["python3", "download_rdf_files.py", json.dumps(www_data)])
            #Wait for process to terminate.
            out, err = p.communicate()
        #add info about instances
        comm.saveStatistics(mylargefile, inst_str + "\n\n")
    else:
        comm.printException(comm.pathToSaveDownloadErrors, errString='No instances to list.')
 

#downloading starts, when RDFizing process is ready
#Uses dictionary-type of json-file (read from bucket)
#it only downloads the doc's which date is the same 
#as current.process's start date (variable 'ajadir')
def doDownloadJob(jsonToDict, itemname):
    global nrOfDownloads
    try:
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
                    #Get the time the json-file was made
                    timeDir = jsonToDict[fname_key][csha]['timeDir']
                    #download only changes that are no  older than 
                    #the date of start of current process!
                    process_start_date = comm.makeDateObj(ajadir)
                    json_model_date = comm.makeDateObj(timeDir)
                    #continueonly if 
                    #date in model is younger or equal to a 
                    #date of a process start
                    if(contentKeyExists) & (json_model_date >= process_start_date):
                        #excel type is already downloaded
                        if("excel" not in jsonToDict[fname_key][csha]['Content-Type']):
                            #full URL of a file
                            file_url = jsonToDict[fname_key][csha]['file_url']
                            dirPath = comm.downloadsDir + base_url + "/"
                            try:
                                #create folder for this 'date/base_url' if does not exist
                                if (not os.path.isdir(dirPath)) & (not os.path.exists(dirPath)):
                                    os.makedirs(dirPath)
                                try:
                                    #download the file into that folder
                                    #fname_key is the sha(filename)
                                    #resulting path of a file will become 'date/base_url/sha(filename)'
                                    urr(file_url, dirPath + fname_key)
                                    nrOfDownloads += 1
                                except:
                                    comm.printException(comm.pathToSaveDownloadErrors, itemname)
                                    pass
                            except:
                                comm.printException(comm.pathToSaveDownloadErrors, itemname)
                                pass
    except:
        comm.printException(comm.pathToSaveDownloadErrors, itemname)
        pass   
    

def processObject(client, itemname):
    try:
        #try to access json object in Google Compute Storage
        # Get Payload Data
        req = client.objects().get_media(
                    bucket = comm.jsonsDir,
                    object=itemname)
        #store info whether a json-object exists in the bucket or not
        fileExists = True
        try:
            resp = req.execute()
        except:
            fileExists = False
            pass
            
        #continue only when the object exists
        if (fileExists):
            # The BytesIO object may be replaced with any io.Base instance.
            fh = io.BytesIO()
            #prepare for reading a json-object
            downloader = MediaIoBaseDownload(fh, req, chunksize=1024*1024)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            #load accessed json-object into dictionary
            jsonToDict = json.loads(fh.getvalue())#json.loads(fh.getvalue())#return value
            #print ("RETURNED VALUE: " + jsonToDict)
            doDownloadJob(jsonToDict, itemname)
    #store error message into respective errors bucket
    except oauth2_client.AccessTokenRefreshError:
        comm.printException(comm.pathToSaveDownloadErrors, errString="False credentials")
        pass


#retrieve json-objects from bucket,
#process each object for later downloadings
def listOfJsonObjects(client):
    try:
        # Get Metadata
        req = client.objects().list(bucket=comm.jsonsDir)            
        # If you have too many items to list in one request, list_next() will
        # automatically handle paging with the pageToken.
        while req is not None:
            resp = req.execute()
            #print json.dumps(resp, indent=2)
            #print ("----------------------------------")
            if resp and 'items' in resp:
                for item in (resp["items"]):
                    #print(item["name"])
                    itemname = (item["name"])
                    processObject(client, itemname)
                
                req = client.objects().list_next(req, resp)
    except oauth2_client.AccessTokenRefreshError:
        comm.printException(comm.pathToSaveDownloadErrors, errString="False credentials")
        pass


  
        
if __name__ == '__main__':
    nr_of_log_rows = 0
    line_counter = 0
    nrOfDownloads = 0
    ipList_and_tuple = getListOfWorkerIPs()
    ipList = ipList_and_tuple[0]
    ipList_tuple = ipList_and_tuple[1]
    ajadir = comm.timeDir
    
    #getObj.getBucketFile('uploaded_logfiles', 'crawl.log')
    #print(WORKER_INSTANCES)#
    #print(len(ipList))
    #print("  tuple  ")#
    #print(ipList_tuple)#
    #print("  ipList  ")#
    #print(ipList)#
    if (len(ipList)>0):
        start = datetime.datetime.now()
        #print("start ", start)
        mylargefile = (json.loads(sys.argv[1]))["logfilename"]
        worker_counter = 0
        #delete_counter = 0
        urlsList = []
        #avoid double work,
        #post only distinct URLs
        distinct_urls = set()
        with open(mylargefile) as f:
            for line in f:
                nr_of_log_rows += 1 #for statistics
                plineUrl = processline(line)
                if(plineUrl is not None)&(plineUrl != ""):
                    if(plineUrl not in distinct_urls)&('icomoon' not in plineUrl.lower())&('hobekivi' not in plineUrl.lower()):
                        distinct_urls.add(plineUrl)
                        #delete_counter += 1
                        line_counter += 1
                        urlsList.append(plineUrl)
                        postListSize = postToWorker.defPostListSize(worker_counter, ipList_tuple)
                        #send certain amount of URLs to each worker, then empty the list of URLS
                        if(len(urlsList) == postListSize):
                            #post the list until connected to worker is successful
                            worker_counter = postToWorker.detectConnection(ipList, worker_counter, urlsList)
                            
                            #postreq_dir
                            jf = open(comm.postreq_path, 'a')
                            jf.write(time.strftime("%d/%m/%Y_%H:%M:%S") + " just posted to: " + str(ipList[worker_counter]) + "\n")
                            jf.close()
                            
                            
                            del urlsList[:] #empty list of urls
                            #prepare next worker
                            worker_counter += 1
                            if (worker_counter > (len(ipList)-1)):
                                #start over from first worker in list
                                worker_counter = 0
                #dont let memory to grow too buzy
                if (len(distinct_urls) > 1000):
                    distinct_urls = set()  
        #ylejaagi postitamine
        if(len(urlsList) > 0):
            #send list of urls to worker
            worker_counter = postToWorker.detectConnection(ipList, worker_counter, urlsList)
        
        #start of statistics!
        comm.saveStatistics(mylargefile, "###########################\n chunksize: "+ str(comm.chunksize)+"\n")
        
        #the time spent
        end = datetime.datetime.now()
        span = end-start
        #save statistics!
        note = "creating RDFs: \n"+"time spent (h:m:s.mm): " + str(span) + " \n\n"
        comm.saveStatistics(mylargefile, note)
        #print("totalseconds: ", span.total_seconds()) 
        
        ###
        ###
        #List instances, aggregate all rdf files into 3 files in master
        start = datetime.datetime.now()
        importRDFfiles()
        ##delete folder, where RDF-files where collected (in master VM)
        #the aggregated RDF-files are in folder rdf_files
        
        for (dirpath, dirnames, filenames) in walk(comm.pathToRDFdir):
            for dire in dirnames:
                direpath = os.path.join(dirpath, dire)
                if(os.path.isdir(direpath)):
                    shutil.rmtree(direpath)
        for (dirpath, dirnames, filenames) in walk(comm.outp_temp_rdf):
            for dire in dirnames:
                direpath = os.path.join(dirpath, dire)
                if(os.path.isdir(direpath)):
                    shutil.rmtree(direpath)
        ''''''
        end = datetime.datetime.now()
        span = end-start
        #save statistics!
        note = "importing-aggregating RDF files: \n"+"time spent (h:m:s.mm): " + str(span) + " \n\n"
        comm.saveStatistics(mylargefile, note)
    
        ###
        ###
        #Download web documents, which metadata are saved in json/object in cloud storage, save them to alivemaster
        #list of json objects
        start = datetime.datetime.now()
        ###CLIENT
        client = authenticate_gce.getMyAuthService('storage', 'v1')
    
        listOfJsonObjects(client)
        importRemoteFiles.importExcelFiles(WORKER_INSTANCES)
        #the time spent
        end = datetime.datetime.now()
        span = end-start
        #save statistics!
        note = "downloading files: \n"+"time spent (h:m:s.mm): " + str(span) + " \nNumber of downloads: " + str(nrOfDownloads) + "\n" 
        comm.saveStatistics(mylargefile, note)
        
        #store info about state of current rdf graph sizes
        filedic = dict()
        filedic["statfile"] = mylargefile
        subprocess.Popen(["python3", "amountOfTriples.py", json.dumps(filedic)])
        
        #end of statistics!
        comm.saveStatistics(mylargefile, "\n--------------------------- ")
        
        
        #delete RDF-files and download excel-files in each worker
        postToWorker.deleteRDFsInWorkers(ipList)
        ###
        ###
        try:
            # Download json-objects from cloud storage
            downloadJsons.getJsonObjects(client)
        except:
            comm.printException(comm.pathToSaveDownloadErrors, errString="downloadJsons")
            pass
        
        ###
        ###
        try:
            ###
            ### Download generated error-objects from cloud storage
            downloadErrors.getErrorObjects(client)
        except:
            comm.printException(comm.pathToSaveDownloadErrors, errString="downloadErrors")
            pass
        
        
    else:
        print("no worker instances")


