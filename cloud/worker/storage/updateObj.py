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
        #TODO! save error somewhere
        #comm.printException(comm.pathToSaveJsonErrors)
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
        #TODO! save error somewhere
        #comm.printException(comm.pathToSaveJsonErrors)
        pass


def updateExistingObj(existingFileDict, client, _BUCKET_NAME, _FILE1_NAME):
    deleteObj.delObj(client, _BUCKET_NAME, _FILE1_NAME)
    jsondata = json.dumps(existingFileDict, indent=4)
    insertObj.insertNewObject(client, _BUCKET_NAME, _FILE1_NAME, jsondata)


def main(argv):
    aadress = json.loads(argv["address"])
    _BUCKET_NAME = aadress["bucket"].encode()
    _FILE1_NAME = aadress["object"].encode()
    jsondata = argv["jsondata"].encode()
    url = argv["url"].encode() #url that came in from BQ table
    localFilename = argv["localFilename"].encode() #SHA of url for local storage
    commTimeDir = argv["timeDir"].encode() #current time when the file was accessed
    redirectedTo=argv["redirectedTo"].encode()
    pageInfo = argv["pageInfo"] #dict object
    sha224_ = argv["sha224_"].encode()
    statusCode = argv["statusCode"] #int object
    
    
    http = httplib2.Http()
    token_uri = '%s/%s/token' % (METADATA_SERVER, SERVICE_ACCOUNT)
    resp, content = http.request(token_uri, method='GET',
                                 body=None,
                                 headers={'Metadata-Flavor': 'Google'})
    
    if resp.status == 200:
        d = json.loads(content)
        access_token = d['access_token']  # Save the access token
        credentials = oauth2_client.AccessTokenCredentials(access_token, 'my-user-agent/1.0')
        client = api_discovery.build('storage', _API_VERSION, http=credentials.authorize(http))

        #save info about whether to extract new entities or not
        someNewData = False
        try:
            # Get Metadata
            req = client.objects().get(
                    bucket=_BUCKET_NAME,
                    object=_FILE1_NAME) # optional
            try:
                resp = req.execute()
            except HttpError:
            	someNewData = True
            except:
            	someNewData = True
            
            if (someNewData is False):#there is a file with this name in this bucket already
                # Get Payload Data
                req = client.objects().get_media(
                    bucket=_BUCKET_NAME,
                    object=_FILE1_NAME)    # optional
                # The BytesIO object may be replaced with any io.Base instance.
                fh = io.BytesIO()
                downloader = MediaIoBaseDownload(fh, req, chunksize=1024*1024)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                existingFileDict = json.loads(fh.getvalue())#return dict()-type value
                #print ("RETURNED VALUE: " + existingFileDict)
                '''
                print ("STR ")
                print (type(existingFileDict) is str)--false
                print ("DICT ")
                print (type(existingFileDict) is dict)--true
                print ("LIST ")
                print (type(existingFileDict) is list)--false
                '''
                if(existingFileDict['base_url'] in url):#same file resource was requested
                    #dict has two 1-level keys: 'base_url' and sha244 of a file name
                    fNameKey = [k for k in existingFileDict.keys() if k != 'base_url']
                    #this list may contain 'localFilename'
                    if (localFilename in fNameKey):
                        #if earlier saved file's sha does not equal to current sha, 
                        #the contents of file has changed.
                        #Saved file's sha is saved into key, find it or not:
                        shaKeys = existingFileDict[localFilename].keys()
                        if(sha224_ not in shaKeys):#file has changed
                            #search for date, if it same, update existing sha key
                            replaceSha = ""
                            #if there is same timedDir under some sha key, get this sha and replace
                            for sk in shaKeys:
                                savedDate = existingFileDict[localFilename][sk]["timeDir"]
                                if(savedDate == commTimeDir):
                                    replaceSha = sk
                                    break
                            if(replaceSha != ""):#delete sha, because of same day date
                                del existingFileDict[localFilename][replaceSha]
                            #add new value with new content_sha-key under filename_sha-key
                            #filename-url is same, but content is changed
                            #so add new content-sha
                            newDataDict = insertNewContentToDict(localFilename, redirectedTo, pageInfo, sha224_, statusCode, commTimeDir)
                            if(newDataDict):
                                existingFileDict[localFilename].update(newDataDict)
                                updateExistingObj(existingFileDict, client, _BUCKET_NAME, _FILE1_NAME)
                                someNewData = True
                            
                    else:#new file (resource) from same domain (or 'base_url') requested
                        #add new value with new filename_sha-key for that base-resource
                        newDataDict = insertNewSubFileToDict(localFilename, redirectedTo, pageInfo, sha224_, statusCode, commTimeDir)
                        if(newDataDict):
                            existingFileDict.update(newDataDict)
                            updateExistingObj(existingFileDict, client, _BUCKET_NAME, _FILE1_NAME)
                            someNewData = True

            else:#inserts new file into bucket
                insertObj.insertNewObject(client, _BUCKET_NAME, _FILE1_NAME, jsondata)

            #return info about whether to extract new entities or not
            print (someNewData)
        except oauth2_client.AccessTokenRefreshError:
            #TODO! save error somewhere
            #print ("False credentials")
            pass
    else:
        #TODO! save error somewhere
        #print (str(False) + str(resp.status))
        pass


if __name__ == '__main__':
    #data = (sys.argv[1]).decode('utf-8')
    #print("data isDict",type(data) is dict)
    #print("data isStr",type(data) is str)
    #print(sys.argv[1])
    d = json.loads(sys.argv[1])
    #print("d isDict",type(d) is dict)
    #print("d isStr",type(d) is str)
    main(d)
# [END all]
