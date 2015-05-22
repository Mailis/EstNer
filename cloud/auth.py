#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import os
import io
import sys
import time
import datetime
import subprocess
import json
import requests
import httplib2
from urllib import urlretrieve as urr
from urllib import urlopen as urlopen
import linecache
from oauth2client import client as oauth2_client
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
from apiclient.http import MediaIoBaseDownload
import getObj

MASTERINSTANCE_NAME = "meister-crawl"
METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'
DEFAULT_ZONE = 'europe-west1-b'
DATA_PROJECT_ID = "fluted-volt-94414" # "estnetcloud" #
PROJECT_ID = "fluted-volt-94414" # "estrdf" #
DATASET = "uploaded_logfiles"
#bigquery table name
TABLE = "crawl1/"
#bucket name of stored json-objects
BUCKET_NAME = 'downloaded_jsons2'
WORKER_INSTANCES = []

nr_of_log_rows = 0
line_counter = 0
nr_of_worker_cpu = 2 #relates to the to be posted list size
postListSize = 100 #defines the to be posted list size
timeDir = time.strftime("%d_%m_%Y")
proxyurl = 'http://130.211.58.132/phpservice.php'

dirToSaveStatistics = "statistics/"
dirToSaveDownloadErrors = "downloading_errors/"
pathToSaveDownloadErrors = dirToSaveDownloadErrors + timeDir + ".txt"
downloads  = "downloaded_files/"
downloadsDir = downloads + timeDir + "/"
authErrorsDirPath = "auth_errors/"+timeDir+".txt"
#create dir if does not exist
if (not os.path.isdir(dirToSaveStatistics)) & (not os.path.exists(dirToSaveStatistics)):
    os.makedirs(dirToSaveStatistics)
if (not os.path.isdir(dirToSaveDownloadErrors)) & (not os.path.exists(dirToSaveDownloadErrors)):
    os.makedirs(dirToSaveDownloadErrors)
if (not os.path.isdir(downloadsDir)) & (not os.path.exists(downloadsDir)):
    os.makedirs(downloadsDir)
    
'''
    Lists file types, where one cannot find entities
'''
desiredFileTypes = ['excel', 'json', 'html', 'xml', 'pdf', 'plain', 'text']#
undesiredFileTypes = ['image', 'no-type', 'javascript', 'flash', 'dns']
undesiredFileExtensions = ['jpg', 'jpeg', 'gif', 'png', 'bmp', 'ico', 'swf', 'js', 'css', 'js', 'css', 'ShockwaveFlash', 'dns']
undesiredFileName = ['robots.txt', '/robots.txt']
    
    
def printException(pathToErrorFile, errString=""):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    err= (time.strftime("%d/%m/%Y_%H:%M:%S") + " " + errString + ' {}_EXCEPTION_IN_({},_LINE_{}_"{}"):_{}_'.format(exc_type, filename, lineno, line.strip(), exc_obj) + "\n\n")
    #TODO!*done
    jf = open(pathToErrorFile, 'a')
    jf.write(err)#
    jf.close()
    
def saveStatistics(note):
    jf = open(dirToSaveStatistics+timeDir+".txt", 'a')
    jf.write(str(datetime.datetime.now()) + "\n" + note)
    jf.close() 
    
def getListOfWorkerIPs():
    global WORKER_INSTANCES
    global MASTERINSTANCE_NAME
    credentials = GoogleCredentials.get_application_default()
    compute = build('compute', 'v1', credentials=credentials)
    result = compute.instances().list(project=PROJECT_ID, zone=DEFAULT_ZONE).execute()
    all_INSTANCES = result['items']
    ipList = []
    print("MASTERINSTANCE_NAME " + MASTERINSTANCE_NAME + "\n\n")
    for instance in all_INSTANCES:
        wwwname = instance['name']
        if(wwwname != MASTERINSTANCE_NAME):
            WORKER_INSTANCES.append(instance)
            accessConfigs = instance['networkInterfaces'][0]['accessConfigs'][0]
            if ("natIP" in accessConfigs):
                ipList.append(accessConfigs["natIP"])
    return ipList
    
def getListOfWorkerInstances():
    credentials = GoogleCredentials.get_application_default()
    compute = build('compute', 'v1', credentials=credentials)
    result = compute.instances().list(project=PROJECT_ID, zone=DEFAULT_ZONE).execute()
    all_INSTANCES = result['items']
    ipList = []
    for instance in all_INSTANCES:
        wwwname = instance['name']
        if(wwwname != MASTERINSTANCE_NAME):
            accessConfigs = instance['networkInterfaces'][0]['accessConfigs'][0]
            ipList.append(instance)
    return ipList


def doDownloadJob(jsonToDict, itemname):
    try:
        base_url = jsonToDict['base_url']#becomes folderName
        for fname_key in jsonToDict.keys():
            if (fname_key != 'base_url'):#fname_key(sha of file url) becomes local filename
                for csha in jsonToDict[fname_key].keys():
                    #excel type is already downloaded
                    #if("excel" not in jsonToDict[fname_key][csha]['Content-Type']):
                    file_url = jsonToDict[fname_key][csha]['file_url']
                    timeDir = jsonToDict[fname_key][csha]['timeDir']
                    dirPath = downloadsDir + base_url + "/"
                    try:
                        #create dir if does not exist
                        if (not os.path.isdir(dirPath)) & (not os.path.exists(dirPath)):
                            os.makedirs(dirPath)
                        try:
                            urr(file_url, dirPath + fname_key)
                            #print(timeDir, base_url, , file_url)
                        except:
                            printException(pathToSaveDownloadErrors, itemname)
                            pass
                    except:
                        printException(pathToSaveDownloadErrors, itemname)
                        pass
    except:
        printException(pathToSaveDownloadErrors, itemname)
        pass
    

def processObject(client, itemname):
    try:
        # Get Payload Data
        req = client.objects().get_media(
                    bucket = BUCKET_NAME,
                    object=itemname)                    # optional
        fileExists = True
        try:
            resp = req.execute()
        except:
            fileExists = False
            pass
            
        if (fileExists):
            # The BytesIO object may be replaced with any io.Base instance.
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, req, chunksize=1024*1024)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            jsonToDict = json.loads(fh.getvalue())#json.loads(fh.getvalue())#return value
            #print ("RETURNED VALUE: " + jsonToDict)
            doDownloadJob(jsonToDict, itemname)
        
    except oauth2_client.AccessTokenRefreshError:
        printException(dirToSaveDownloadErrors+timeDir+".txt", errString="False credentials")
        pass

    

def listOfJsonObjects(client):
    try:
        # Get Metadata
        req = client.objects().list(bucket=BUCKET_NAME)            
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
        printException(dirToSaveDownloadErrors+timeDir+".txt", errString="False credentials")
        pass

def postListToWorker(wip, urlsList):
    pikkus = len(urlsList)
    dik = dict(zip(range(pikkus),urlsList))
    address = "http://"+wip
    #print("ADDreSS " + address + " \n")
    #print("DATA " + json.dumps(dik) + " \n")
    requests.post(address, data={'data':json.dumps(dik)})
    
    
def postRows(multiplerows):
    pikkus = len(multiplerows)
    dik = dict(zip(range(pikkus),multiplerows))
    requests.post(proxyurl, data={'data':json.dumps(dik)})
    
    
def prepareRequest(datarows):
    distinct_urls = set()
    multiplerows = []
    for row in datarows:
        rida = {}
        rida["url"] = ""
        rida["basic_url"] = ""
        count=0
        for cell in row['f']:
            if count==0:
                urll = cell['v']
                if(urll not in distinct_urls):
                    distinct_urls.add(urll)
                    rida["url"] = urll
            elif count==1:
                burl = cell['v']
                if(burl not in distinct_urls):
                    distinct_urls.add(burl) 
                    rida["basic_url"] = burl
                
            elif count==2:
                rida['redirect'] = cell['v'].encode('ascii','ignore')
            elif count==3:
                rida['contenttype'] = cell['v'].encode('ascii','ignore')
            count += 1
 
        if('no-type' not in rida['contenttype']) and (rida["url"] != "") and (rida["basic_url"] != ""):
            #print(rida)
            multiplerows.append(rida)
            if(len(multiplerows) >= (2*nr_of_worker_cpu)):
                postRows(multiplerows)
                del multiplerows[:]    
                
        #dont let memory to grow too buzy
        if (len(distinct_urls) > 1000):
            distinct_urls = set() 
           
    #ylejaagi postitamine:
    if(len(multiplerows) > 0):
        postRows(multiplerows)
        del multiplerows[:]    
     
        
        
def runBqQuery (bq, currentRow = 0):
    
    jobCollection = bq.jobs()
    queryString = 'SELECT url, basic_url, redirect, contenttype FROM ['+DATASET+'.'+TABLE+'] LIMIT '+str(nr_of_log_rows)+';'
    jobData = {
      'configuration': {
        'query': {
          'query': queryString,
        }
      }
    }

    insertResponse = jobCollection.insert(projectId=DATA_PROJECT_ID,
                                         body=jobData).execute()

    # Get query results. Results will be available for about 24 hours.    
    queryReply = jobCollection.getQueryResults(
                      projectId=DATA_PROJECT_ID,
                      jobId=insertResponse['jobReference']['jobId'],
                      startIndex=currentRow).execute()
    datarows = (queryReply['rows'])
    #print(datarows)
    #print(len(datarows))
    #prepareRequest(datarows)



def importRDFfiles():
    global WORKER_INSTANCES
    inst_str = "number of log rows: " + str(nr_of_log_rows) + "\n"
    inst_str = "number of processed rows: " + str(line_counter) + "\n"
    inst_str += "length of POST list: " + str(nr_of_worker_cpu) + "\n"

    list_len = len(WORKER_INSTANCES)
    inst_str += "number of worker instaces: " + str(list_len) + "\n" 
    #print("WORKERS " + str(WORKER_INSTANCES))
    if list_len > 0:
        for instance in WORKER_INSTANCES:
            wwwname = instance['name']
            inst_str += "\nworkername: " + wwwname + " machineType: " + instance['machineType']
            wwwip = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
            www_data = dict()
            www_data["ip"] = wwwip
            www_data["name"] = wwwname
            subprocess.Popen(["python3", "download_rdf_files.py", json.dumps(www_data)])
            '''
            #download excels            
            try:
                excels_url = "http://" + wwwip + "/getExcelFilePaths.php"
                response = urlopen(excels_url);
                #print(response)
                ''' '''
                #note ="EXCELPATH " + str(response) + "\n"
                excelfilepaths = json.loads(response.read())
                if(len(excelfilepaths)> 0):
                    for excelfile in excelfilepaths:
                        splitted = excelfile.split("/")
                        folders = "/".join(splitted[0:-1])
                        if (not os.path.isdir(folders)) & (not os.path.exists(folders)):
                            os.makedirs(folders)
                        getPath = "http://" + wwwip + "/" + excelfile
                        urr(getPath, excelfile)
                        #os.system("wget http://" + wwwip + "/" + excelfile + " -O " + excelfile)
                #out, err = p.communicate()
                #someNewData  = out.decode()
                #print(someNewData)           
            except:           
                pass
            '''
        #add info about instances
        saveStatistics(inst_str + "\n\n")
    else:
        printException(dirToSaveDownloadErrors+timeDir+".txt", errString='No instances to list.')
    
    


def getMyAuthService(service_name = 'bigquery', service_version = 'v2'):
    http = httplib2.Http()
    token_uri = '%s/%s/token' % (METADATA_SERVER, SERVICE_ACCOUNT)
    resp, content = http.request(token_uri, method='GET',
                                 body=None,
                                 headers={'Metadata-Flavor': 'Google'})
    if resp.status == 200:
        d = json.loads(content)
        access_token = d['access_token']  # Save the access token
        credentials = oauth2_client.AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        AUTH_HTTP = credentials.authorize(http)
        return build(service_name, service_version, http=AUTH_HTTP)
        
    else:
        printException(authErrorsDirPath, errString="AUTHENTICATION RESPONSE STATUS: " + resp.status)
        pass

def isNeededUrl(url):
    neededUrl = True
    fileName =  (url.lower().split("/"))[-1]
    if(fileName in undesiredFileName):
        neededUrl = False
    if(neededUrl):        
        extSplit = (fileName.split("."))
        lastIndex = len(extSplit)-1
        if(lastIndex > 0):
            extension = (extSplit[lastIndex])
            if(extension in undesiredFileExtensions):
                neededUrl = False
    if(neededUrl):
        for udft in undesiredFileTypes:
            if(udft in url):
                neededUrl = False
                break
    return neededUrl
        
    
def processline(line): 
    splitted = line.split()
    tyyp = splitted[6]#content type
    #disable unwanted content types
    if( tyyp not in undesiredFileTypes):
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
                url = splitted[5]
            else:#send url of file
                url = splitted[3]
                
        if(url != ""):
            neededUrl = isNeededUrl(url)
            if(neededUrl):
                return url  
        else:
            return ""  


def defPostListSize():
    global postListSize
    defsize = 2*nr_of_worker_cpu 
    if(defsize > postListSize):  # <
        postListSize = defsize   
        
         
if __name__ == '__main__':
    ipList = getListOfWorkerIPs()

    #getObj.getBucketFile('uploaded_logfiles', 'crawl.log')
    #print(WORKER_INSTANCES)

    start = datetime.datetime.now()
    #print(start)
    TABLE = (json.loads(sys.argv[1]))["tablename"]
    mylargefile = "logfiles/" + TABLE
    worker_counter = 0
    #delete_counter = 0
    urlsList = []
    defPostListSize()
    #avoid double work
    distinct_urls = set()
    with open(mylargefile) as f:
        for line in f:
            nr_of_log_rows += 1 #for statistics
            plineUrl = processline(line)
            if(plineUrl != "")&(plineUrl not in distinct_urls):
                distinct_urls.add(plineUrl)
                #delete_counter += 1
                line_counter += 1
                urlsList.append(plineUrl)
                if(len(urlsList) == postListSize):
                    #send list of urls to worker
                    #print("WORKERS " + str(worker_counter))
                    postListToWorker(ipList[worker_counter], urlsList)
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
        postListToWorker(ipList[worker_counter], urlsList)
        
    #bigquery table
    #print(TABLE)
    #bq = getMyAuthService()
    #runBqQuery(bq, 0)
    

    #the time spent
    end = datetime.datetime.now()
    span = end-start
    #save statistics!
    note = "creating RDFs: \n"+"span totalseconds: " + str(span.total_seconds()) + " \n\n"
    saveStatistics(note)
    print("totalseconds: ", span.total_seconds()) 
    
    ###
    ###
    #List instances, aggregate all rdf files into 3 files in alivemaster
    start = datetime.datetime.now()
    importRDFfiles()
    end = datetime.datetime.now()
    span = end-start
    #save statistics!
    note = "importing-aggregating RDF files: \n"+"span totalseconds: " + str(span.total_seconds()) + " \n\n"
    saveStatistics(note)

    ###
    ###
    #Download web pages, which metadata are saved in json/object in cloud storage, save them to alivemaster
    #list of json objects
    start = datetime.datetime.now()
    storage_service = getMyAuthService('storage', 'v1')

    listOfJsonObjects(storage_service)

    #the time spent
    end = datetime.datetime.now()
    span = end-start
    #save statistics!
    note = "downloading files: \n"+"span totalseconds: " + str(span.total_seconds()) + " \n---------\n\n"
    saveStatistics(note)
''' '''   
    
    
    
    
    
