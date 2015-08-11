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

METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'


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
        comm.printException(comm.pathToSaveauthErrors, errString="AUTHENTICATION RESPONSE STATUS: " + resp.status)
        pass