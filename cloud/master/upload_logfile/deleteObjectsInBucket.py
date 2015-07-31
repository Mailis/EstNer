#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import commonVariables as comm
import json
import httplib2
from oauth2client import client as oauth2_client
from googleapiclient.discovery import build

import authenticate_gce
 

def deleteAllObjectsIn(bucket_name, client):
    req = client.objects().list(bucket=comm.jsonsDir)            
    # If you have too many items to list in one request, list_next() will
    # automatically handle paging with the pageToken.
    while req is not None:
        resp = req.execute()
        #print json.dumps(resp, indent=2)
        #print ("----------------------------------")
        if resp and 'items' in resp:
            for item in (resp["items"]):
                object_name = (item["name"])
                
                try:
                    client.objects().delete(
                        bucket=bucket_name,
                        object=object_name).execute()
                except:
                    try:
                        print(object_name)
                        #for cl in client.objects():
                        #   cl.delete(bucket_name + "/" + object_name)
                    except:
                        pass
                
            req = client.objects().list_next(req, resp)
    
    
    
if __name__ == '__main__':
    client = authenticate_gce.getMyAuthService('storage', 'v1')
    bucket_name = comm.jsonsDir
    deleteAllObjectsIn(bucket_name, client)
    #bucket_name2 = comm.errorsBucket
    #deleteAllObjectsIn(bucket_name2, client)
    
    
    
    
    
    