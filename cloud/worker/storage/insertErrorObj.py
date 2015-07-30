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

import insertObj
import deleteObj

_API_VERSION = "v1"

METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'



def main(argv):
    _BUCKET_NAME = argv["bucket"].encode()
    _COMPOSITE_FILE_NAME = argv["object"].encode()
    _FILE1_NAME = _COMPOSITE_FILE_NAME + "errTEmp.txt"
    #_FILE2_NAME = "tmp.txt"
    errdata = argv["errdata"].encode()#"TEINE URR\n"#

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
        #check if file exists
        fileExists = True
        try:
            # Get Metadata
            req = client.objects().get(
                    bucket=_BUCKET_NAME,
                    object=_COMPOSITE_FILE_NAME) # optional
            try:
                resp = req.execute()
            except:
                fileExists = False
                
            if (fileExists is False):
                insertObj.insertNewObject(client, _BUCKET_NAME, _COMPOSITE_FILE_NAME, errdata)
            else:
                insertObj.insertNewObject(client, _BUCKET_NAME, _FILE1_NAME, errdata)
                try:
                    composite_object_resource = {
                            'contentType': 'text/plain',  # required
                            'contentLanguage': 'et',
                            'metadata': {'my-key': 'my-value'},
                    }
                    compose_req_body = {
                            'sourceObjects': [
                                    {'name': _FILE1_NAME},
                                    {'name': _COMPOSITE_FILE_NAME}],
                            'destination': composite_object_resource
                    }
                    req = client.objects().compose(
                            destinationBucket=_BUCKET_NAME,
                            destinationObject=_COMPOSITE_FILE_NAME,
                            body=compose_req_body)
                    resp = req.execute()
                    print (json.dumps(resp, indent=2))
                    deleteObj.delObj(client, _BUCKET_NAME, _FILE1_NAME)
                except oauth2_client.AccessTokenRefreshError:
                    print ("The credentials have been revoked or expired, please re-run the application to re-authorize")
                    pass
            
        except oauth2_client.AccessTokenRefreshError:
            #TODO! save error somewhere
            print ("False credentials")
            pass
    else:
        print (resp.status)


if __name__ == '__main__':
    d = json.loads(sys.argv[1])
    main(d)
# [END all]


