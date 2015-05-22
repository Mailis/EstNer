#!/usr/bin/python
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
#from oauth2client.client import GoogleCredentials
#from oauth2client.client import flow_from_clientsecrets
#from oauth2client.client import FlowExchangeError

from oauth2client.client import SignedJwtAssertionCredentials
CLIENT_EMAIL = '238914372761-b8v8vhchp68pcj4ck2iijc1rsgvk520f@developer.gserviceaccount.com'
myP12 = "nltk-0b617369aad3.p12"
CREDENTIALS = ""
PRIVATE_KEY =""

from apiclient.http import MediaIoBaseDownload

CLIENTSECRET_LOCATION = 'nltk-4ff3713805f4.json'
SCOPES = [
    'https://www.googleapis.com/auth/drive.file',
    'email',
    'profile',
    'https://www.googleapis.com/auth/bigquery',
    'https://www.googleapis.com/auth/cloud-platform',
    'https://www.googleapis.com/auth/compute',
    'https://www.googleapis.com/auth/devstorage.full_control',
    'https://www.googleapis.com/auth/logging.write',
    'https://www.googleapis.com/auth/userinfo.email',

]


METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'
DEFAULT_ZONE = 'europe-west1-b'
DATA_PROJECT_ID = "estnetcloud" #"fluted-volt-94414" # 
PROJECT_ID = "estrdf" #"fluted-volt-94414" # 
DATASET = "uploaded_logfiles"
#bigquery table name
TABLE = "crawl1/"
#bucket name of stored json-objects
BUCKET_NAME = 'downloaded_jsons'

nr_of_log_rows = 60
nr_of_worker_cpu = 16
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
    
    

def doDownloadJob(jsonToDict, itemname):
    try:
        base_url = jsonToDict['base_url']#becomes folderName
        for fname_key in jsonToDict.keys():
            if (fname_key != 'base_url'):#fname_key(sha of file url) becomes local filename
                for csha in jsonToDict[fname_key].keys():
                    #excel type is already downloaded
                    if("excel" not in jsonToDict[fname_key][csha]['Content-Type']):
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
    queryString = 'SELECT url, basic_url, redirect, contenttype FROM [uploaded_logfiles.'+TABLE+'] LIMIT '+str(nr_of_log_rows)+';'
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
    prepareRequest(datarows)



def importRDFfiles():
    #credentials = GoogleCredentials.get_application_default()
    compute = build('compute', 'v1', credentials=CREDENTIALS)
    result = compute.instances().list(project=PROJECT_ID, zone=DEFAULT_ZONE).execute()
    instance_list = result['items']
    inst_str = "number of log rows: " + str(nr_of_log_rows) + "\n"
    inst_str += "length of POST list: " + str(nr_of_worker_cpu) + "\n"

    list_len = len(instance_list)-1
    inst_str += "number of worker instaces: " + str(list_len) + "\n" 
    if list_len > 0:
        for instance in instance_list:
            wwwname = instance['name']
            inst_str += "\n" + wwwname + ": " + instance['name'] + " machineType: " + instance['machineType']
            if wwwname != 'alivemaster':
                wwwip = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']
                www_data = dict()
                www_data['ip'] = wwwip
                www_data['name'] = wwwname
                subprocess.Popen(["python3", "download_rdf_files.py", json.dumps(www_data)], stdout=subprocess.PIPE)
                excels_url = "http://" + wwwip + "/getExcelFilePaths.php"
                response = urlopen(excels_url);
                excelfilepaths = json.loads(response.read())
                for excelfile in excelfilepaths:
                    splitted = excelfile.split("/")
                    folders = "/".join(splitted[0:-1])
                    if (not os.path.isdir(folders)) & (not os.path.exists(folders)):
                        os.makedirs(folders)
                    os.system("wget http://" + wwwip + "/" + excelfile + " -O " + excelfile)
                #out, err = p.communicate()
                #someNewData  = out.decode()
                #print(someNewData)
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
        #credentials = oauth2_client.AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        AUTH_HTTP = CREDENTIALS.authorize(http)
        return build(service_name, service_version, http=AUTH_HTTP)
        
    else:
        printException(authErrorsDirPath, errString="AUTHENTICATION RESPONSE STATUS: " + resp.status)
        pass
    
    
    
if __name__ == '__main__':
    
    #credentials = GoogleCredentials.get_application_default()
    with open(myP12) as f:
        PRIVATE_KEY = f.read()
    CREDENTIALS = SignedJwtAssertionCredentials(CLIENT_EMAIL, PRIVATE_KEY, 'https://www.googleapis.com/auth/sqlservice.admin')
    compute = build('compute', 'v1', credentials=CREDENTIALS)
    result = compute.instances().list(project=PROJECT_ID, zone=DEFAULT_ZONE).execute()
    instance_list = result['items']
    print(instance_list)


    start = datetime.datetime.now()
    #print(start)
    #bigquery table
    TABLE = (json.loads(sys.argv[1]))["tablename"]
    #print(TABLE)
    bq = getMyAuthService()
    runBqQuery(bq, 0)
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
    
    
    
    
    
    
