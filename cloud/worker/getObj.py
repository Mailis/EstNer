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
_BUCKET_NAME = '--statistika'
_FILE1_NAME = '..test1.txt'
_FILE2_NAME = '--test2.txt'
_COMPOSITE_FILE_NAME = 'test-composite.txt'


def main(argv):
    #print (argv)
    #print(argv["object"])
    #print(argv["bucket"])
    _BUCKET_NAME = argv["bucket"]
    _FILE1_NAME = argv["object"]
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
                print (False)
            except:
            	fileExists = False
                print (False)
            
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
                print (fh.getvalue())#return value
        
        except oauth2_client.AccessTokenRefreshError:
            print ("False credentials")
    else:
        print (False + str(resp.status))


if __name__ == '__main__':
    #data = (sys.argv[1]).decode('utf-8')
    #print("data isDict",type(data) is dict)
    #print("data isStr",type(data) is str)
    print(sys.argv[1])
    d = json.loads(sys.argv[1])
    #print("d isDict",type(d) is dict)
    #print("d isStr",type(d) is str)
    main(d)
# [END all]
