#!/usr/bin/python2
# -*- coding: utf-8 -*-
'''
Created on Apr 8, 2015
https://cloud.google.com/storage/docs/json_api/v1/objects/insert#examples
'''
# enable debugging
import cgitb
cgitb.enable()

import io
from oauth2client import client as oauth2_client
from apiclient.http import MediaIoBaseUpload


def insertNewObject(client, _BUCKET_NAME, _FILE1_NAME, jsondata):
    try:
        ## The BytesIO object may be replaced with any io.Base instance.
        media = MediaIoBaseUpload(io.BytesIO(jsondata), 'text/plain')
        req = client.objects().insert(
                bucket=_BUCKET_NAME,
                name=_FILE1_NAME,
                media_body=media)
        resp = req.execute()
        #print (json.dumps(resp, indent=2))
    except oauth2_client.AccessTokenRefreshError:
        print ("The credentials have been revoked or expired, please re-run"
          "the application to re-authorize")
