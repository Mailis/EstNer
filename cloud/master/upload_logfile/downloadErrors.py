#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()
#downloadErrors.py
import io
from oauth2client import client as oauth2_client
from apiclient.http import MediaIoBaseDownload
import commonVariables as comm


errorsBucket = comm.errorsBucket

def processObject(client, itemname):
    try:
        #try to access json object in Google Compute Storage
        # Get Payload Data
        req = client.objects().get_media(
                    bucket = errorsBucket,
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
            #print (fh.getvalue())
            #load accessed json-object into dictionary
            jsonFile = fh.getvalue()
            #print(jsonFile)
            jf = open("../" + errorsBucket + "/" + itemname.encode(), 'w')
            jf.write(jsonFile)
            jf.close()
            #store error message into respective errors bucket
    except oauth2_client.AccessTokenRefreshError:
        pass

def getErrorObjects(client):
    try:
        # Get Metadata
        req = client.objects().list(bucket=errorsBucket)            
        # If you have too many items to list in one request, list_next() will
        # automatically handle paging with the pageToken.
        
        while req is not None:
            resp = req.execute()
            if resp and 'items' in resp:
                for item in (resp["items"]):
                    itemname = (item["name"])
                    processObject(client,itemname)
                req = client.objects().list_next(req, resp)
    except oauth2_client.AccessTokenRefreshError as e:
        return(str(e))

    












