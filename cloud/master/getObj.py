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
 
_API_VERSION = "v1"

METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'

# Define sample variables.
_BUCKET_NAME = 'uploaded_logfiles'
_FILE1_NAME = 'crawl.log'


def getBucketFile(_BUCKET_NAME, _FILE1_NAME):
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
        
        try:
            # Get Metadata
            req = client.objects().get(
                    bucket=_BUCKET_NAME,
                    object=_FILE1_NAME)                    # optional
            fileExists = True
            try:
                resp = req.execute()
            except HttpError:
            	fileExists = False
                print (str(fileExists))
            except:
            	fileExists = False
                print (str(fileExists))
            
            if (fileExists):
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
                returnValue = json.loads(fh.getvalue())#return value
                #print ("RETURNED VALUE: " + returnValue)
                ''''''
                print ("STR ")
                print (type(returnValue) is str)
                print ("DICT ")
                print (type(returnValue) is dict)
                print ("LIST ")
                print (type(returnValue) is list)
                
        
        except oauth2_client.AccessTokenRefreshError:
            print ("False credentials")
    else:
        print (str(False) + str(resp.status))


# [END all]
