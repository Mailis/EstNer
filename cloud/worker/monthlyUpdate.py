#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()

import sys
import os
import io
import json
import time
import linecache
import hashlib
import requests
from multiprocessing import Pool
import httplib2
from oauth2client import client as oauth2_client
from googleapiclient.discovery import build
from apiclient.http import MediaIoBaseDownload
import init_rdf
#import download_files_from_log as dffl

pathToRDFdir = "rdf_files/"
jsonsDir = "datadownload_jsons"
errorsBucket = "generated_files"
timeDir = time.strftime("%d_%m_%Y")
pathToUpdateErrorsDir = "update_errors/"
updateErrorsFilePath = pathToUpdateErrorsDir + timeDir + ".txt"
 
#od = init_rdf.OntologyData(pathToRDFdir)
#init_rdf.RdfFilesCreator(od)



METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'

def debug(note):
    jf = open("updateTestPy.txt", 'a')
    jf.write(str(note))
    jf.close()

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
    


#read json-object, saved into parameter 'jsonToDict'
def readJsonObject(jsonToDict, itemname):
    #base_url is a hostname of a web document
    base_url = jsonToDict['base_url']#becomes folderName
    #hash is sha224
    for key in jsonToDict.keys():
        #if key is currently not a base_url, it is filename
        #filename can contain one or more  content SHAs
        if(key != 'base_url'):#key is sha of file's URL, elsewhere saved into variable localFilename 
            #structure:
            #sha of filename
            ###sha of file content
            ######metadata of file + (filename , sha(file content), human-readable file url, accessed date) 
            ###sha of file another (updated) content
            ######metadata...
            fileSHAs = list(jsonToDict[key].keys())#list of SHA's of file content at time of accessing this file
            arbitrFileSha = fileSHAs[0]#this is only for getting file URL
            fileUrl = jsonToDict[key][arbitrFileSha]["file_url"]
            canOpenUrl = True
            debug(fileUrl)

def detectChanges(itemname):
    try:
        #try to access json object in Google Compute Storage
        # Get Payload Data
        req = client.objects().get_media(
                    bucket = jsonsDir,
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
            #start reading json-object
            readJsonObject(jsonToDict, itemname)
    #store error message into respective errors bucket
    except oauth2_client.AccessTokenRefreshError:
        printException(updateErrorsFilePath, errString="False credentials")
        pass
    

#authenticate Google Compute Engine Service
#uses google-python-api methods
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
        printException(updateErrorsFilePath, errString="AUTHENTICATION RESPONSE STATUS: " + resp.status)
        pass
    
 

   
if __name__ == "__main__":
    data = json.loads((json.loads(sys.argv[1]))["data"])
    jobs = list(data.values())
    nrOfJobs=len(jobs)
    client = getMyAuthService('storage', 'v1')
    #debug("nrOfJobs " + str(nrOfJobs))
    ''''''
    if(nrOfJobs > 0):
        pool = Pool(2)#(processes=os.cpu_count())
        pool.map(detectChanges, jobs)
        pool.close()
        pool.join()
    
        
        
        
        