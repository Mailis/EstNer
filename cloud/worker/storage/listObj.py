'''
Created on Apr 8, 2015
https://cloud.google.com/storage/docs/json_api/v1/objects/list
'''
# enable debugging
import cgitb
cgitb.enable()

import sys
import json
import httplib2
import googleapiclient.discovery as api_discovery
from oauth2client import client as oauth2_client


_API_VERSION = "v1"

METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'

# Define sample variables.
_BUCKET_NAME = 'statistika'
_FILE1_NAME = 'test1.txt'
_FILE2_NAME = 'test2.txt'
_COMPOSITE_FILE_NAME = 'test-composite.txt'


def main(argv):
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
            fields_to_return = 'nextPageToken,items(bucket,name,metadata(my-key))'
            req = client.objects().list(
            bucket=_BUCKET_NAME,
            fields=fields_to_return,    # optional
            maxResults=42)              # optional

            # If you have too many items to list in one request, list_next() will
            # automatically handle paging with the pageToken.
            while req is not None:
                resp = req.execute()
                print (json.dumps(resp, indent=2))
                req = client.objects().list_next(req, resp)
                    
        except oauth2_client.AccessTokenRefreshError:
            print ("The credentials have been revoked or expired, please re-run"
              "the application to re-authorize")
    else:
        print (resp.status)


if __name__ == '__main__':
    main(sys.argv)
# [END all]

