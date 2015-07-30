#!/usr/local/bin/python2
# -*- coding: utf-8 -*-
'''
Created on Apr 8, 2015
https://cloud.google.com/storage/docs/json_api/v1/objects/get
'''
# enable debugging
import cgitb
cgitb.enable()

import io
import sys
import json
import httplib2
import googleapiclient.discovery as api_discovery
from oauth2client import client as oauth2_client
from apiclient.http import MediaIoBaseDownload
from googleapiclient.errors import HttpError
import codecs

import commonvariables as comm

import insertObj
import deleteObj
 
if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')


_API_VERSION = "v1"
METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'
 

def insertNewContentToDict(localFilename, page_redirected, page_info, page_sha254, page_status, commTimeDir):
    try:
        newDict = dict()
        newDict[page_sha254] = page_info
        newDict[page_sha254]["localFilename"] = localFilename
        newDict[page_sha254]["file_url"] = page_redirected
        newDict[page_sha254]["sha224"] = page_sha254
        newDict[page_sha254]["status"] = page_status
        newDict[page_sha254]["timeDir"] = commTimeDir
        return newDict
    except:
        comm.printException(comm.pathToSaveJsonErrors)
        pass

def insertNewSubFileToDict(localFilename, page_redirected, page_info, page_sha254, page_status, commTimeDir):
    try:
        newDict = dict()
        newDict[localFilename] = dict()
        newDict[localFilename][page_sha254] = page_info
        newDict[localFilename][page_sha254]["localFilename"] = localFilename
        newDict[localFilename][page_sha254]["file_url"] = page_redirected
        newDict[localFilename][page_sha254]["sha224"] = page_sha254
        newDict[localFilename][page_sha254]["status"] = page_status
        newDict[localFilename][page_sha254]["timeDir"] = commTimeDir
        return newDict
    except:
        comm.printException(comm.pathToSaveJsonErrors)
        pass


def updateExistingObj(existingFileDict, client, _BUCKET_NAME, _FILE1_NAME):
    deleteObj.delObj(client, _BUCKET_NAME, _FILE1_NAME)
    jsondata = json.dumps(existingFileDict, indent=4)
    insertObj.insertNewObject(client, _BUCKET_NAME, _FILE1_NAME, jsondata)

'''
Check, if the json-object of a document exists.
If exists, check whether its content had changed meanwhile or not.
If some changes occured or new doc accessed, update its meta data or save new object
return boolean value to indicate changes/no changes
'''
def main(argv):
    #load json-formatted meta data into dictionary
    aadress = json.loads(argv["address"])
    _BUCKET_NAME = aadress["bucket"].encode()
    _FILE1_NAME = aadress["object"].encode()
    jsondata = argv["jsondata"].encode()
    localFilename = argv["localFilename"].encode() #SHA of url for local storage
    commTimeDir = argv["timeDir"].encode() #current time when the file was accessed
    redirectedTo=argv["redirectedTo"].encode()
    url = redirectedTo
    pageInfo = argv["pageInfo"] #dict object
    sha224_ = argv["sha224_"].encode()
    statusCode = argv["statusCode"] #int object
    
    #google-python-api code, get access to storage bucket
    http = httplib2.Http()
    token_uri = '%s/%s/token' % (METADATA_SERVER, SERVICE_ACCOUNT)
    resp, content = http.request(token_uri, method='GET',
                                 body=None,
                                 headers={'Metadata-Flavor': 'Google'})
    #google-python-api code, authenticate credentials
    if resp.status == 200:
        d = json.loads(content)
        access_token = d['access_token']  # Save the access token
        credentials = oauth2_client.AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        client = api_discovery.build('storage', _API_VERSION, http=credentials.authorize(http))

        #save info about whether to extract new entities or not
        someNewData = False
        #try to open existing object
        try:
            #google-python-api code,  Get Metadata of bucket object
            req = client.objects().get(
                    bucket=_BUCKET_NAME,
                    object=_FILE1_NAME) # optional
            try:
                resp = req.execute()
            #if it was impossible to open this object, it means
            #this object does not exist yes, therefore this doc is 'new data'
            except HttpError:
                someNewData = True
            except:
                someNewData = True
            
            #in the case, when object exists,
            #it should be checked whether its content had changed or not
            if (someNewData is False):#there is a file with this name in this bucket already
                #google-python-api code, Get Payload Data: get object in bucket
                req = client.objects().get_media(
                    bucket=_BUCKET_NAME,
                    object=_FILE1_NAME)    # optional
                # The BytesIO object may be replaced with any io.Base instance.
                fh = io.BytesIO()
                #google-python-api code
                downloader = MediaIoBaseDownload(fh, req, chunksize=1024*1024)
                done = False
                #download object
                while not done:
                    status, done = downloader.next_chunk()
                #status: an object is downloaded
                
                #load json-object into dict
                existingFileDict = json.loads(fh.getvalue())#return dict()-type value
                '''
                #Debugging
                #print ("RETURNED VALUE: " + existingFileDict)
                print ("STR ")
                print (type(existingFileDict) is str)--false
                print ("DICT ")
                print (type(existingFileDict) is dict)--true
                print ("LIST ")
                print (type(existingFileDict) is list)--false
                '''
                #'existingFileDict' is a dict of downloaded object
                #'base_url' is a host name of current web document
                #if url (file name of current web document) contains 'base_url',
                #it means that this doc may already processed
                if(existingFileDict['base_url'] in url):#same host name was requested
                    #dict has two 1-level keys: 'base_url' and sha244 of a file name
                    #check if this doc is also processed earlier:
                    #get list of hashes of filenames in this (downloaded/already existing) json-object
                    fNameKey = [k for k in existingFileDict.keys() if k != 'base_url']
                    #this list may contain 'localFilename'
                    #'localFilename' is a hash of fileUrl of a current document
                    #true if current fileName in the list of existing filenames of a host
                    if (localFilename in fNameKey):
                        #if earlier saved file's content sha does not equal to current doc content sha, 
                        #the contents of file has changed.
                        #Saved (downloaded/already existing) file's sha is saved into key, find it or not:
                        shaKeys = existingFileDict[localFilename].keys()
                        #true if current doc's content hash is not found
                        if(sha224_ not in shaKeys):#file has changed
                            #search for date, if it same, update existing sha key
                            #this for avoiding redundant info
                            replaceSha = ""
                            #if there is same timedDir under some sha key, get this sha and replace
                            #loop over all content hashes (these are keys in json-file)
                            for sk in shaKeys:
                                savedDate = existingFileDict[localFilename][sk]["timeDir"]
                                #compare saved date to current date
                                if(savedDate == commTimeDir):#same date has found
                                    replaceSha = sk
                                    break # no need to search further
                            #true if the same date was found
                            if(replaceSha != ""):#delete sha, because of same day date
                                del existingFileDict[localFilename][replaceSha]
                            #add new value with new content_sha-key under filename_sha-key
                            #filename-url is same, but content is changed
                            #so add/update new content-sha
                            newDataDict = insertNewContentToDict(localFilename, redirectedTo, pageInfo, sha224_, statusCode, commTimeDir)
                            if(newDataDict):
                                existingFileDict[localFilename].update(newDataDict)
                                updateExistingObj(existingFileDict, client, _BUCKET_NAME, _FILE1_NAME)
                                someNewData = True
                            
                    #current fileName was NOT in the list of existing filenames of a host
                    else:#new file (resource) from same domain (or 'base_url') requested
                        #add new value with new filename_sha-key for that base-resource
                        newDataDict = insertNewSubFileToDict(localFilename, redirectedTo, pageInfo, sha224_, statusCode, commTimeDir)
                        if(newDataDict):
                            existingFileDict.update(newDataDict)
                            updateExistingObj(existingFileDict, client, _BUCKET_NAME, _FILE1_NAME)
                            someNewData = True
            #current host was NOT accessed/processed so far
            else:#inserts new file into bucket
                insertObj.insertNewObject(client, _BUCKET_NAME, _FILE1_NAME, jsondata)

            #return info about whether to send doc to parser and extract new entities or not
            print (someNewData)
        except oauth2_client.AccessTokenRefreshError:
            errstr = ("oauth2_client.AccessTokenRefreshError_False_credentials")
            comm.printException(comm.pathToSaveJsonErrors, errstr)
            pass
    else:
        errstr = "Cannot_access_google_storage_" + (str(False) + str(resp.status))
        comm.printException(comm.pathToSaveJsonErrors, errstr)
        pass


if __name__ == '__main__':
    #receive json-object of doc's meta data
    d = json.loads(sys.argv[1])
    main(d)
# [END all]
