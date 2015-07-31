#!/usr/bin/python2
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()

import json
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials
import commonVariables as comm



if __name__ == '__main__':
    WORKER_INSTANCES = []
    
    credentials = GoogleCredentials.get_application_default()
    compute = build('compute', 'v1', credentials=credentials)
    result = compute.instances().list(project=comm.PROJECT_ID, zone=comm.DEFAULT_ZONE).execute()
    all_INSTANCES = result['items']
    ipList = []
    #print("MASTERINSTANCE_NAME " + MASTERINSTANCE_NAME + "\n\n")
    for instance in all_INSTANCES:
        wwwname = instance['name']
        if(wwwname != comm.MASTERINSTANCE_NAME):
            WORKER_INSTANCES.append(instance)
            #print(instance)
    print (json.dumps(WORKER_INSTANCES))
   
