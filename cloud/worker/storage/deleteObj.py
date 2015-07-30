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


def delObj(client, bucket_name, object_name):
    try:
        client.objects().delete(
        bucket=bucket_name,
        object=object_name).execute()
    except oauth2_client.AccessTokenRefreshError:
        #TODO! save error somewhere
        print ("The credentials have been revoked or expired, please re-run"
          "the application to re-authorize")
