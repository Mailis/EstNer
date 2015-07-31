#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()

import downloadJsons
import downloadErrors
import authenticate_gce


if __name__ == '__main__':
    try:
        ###
        ### Download json-objects from cloud storage
        #CLIENT
        client = authenticate_gce.getMyAuthService('storage', 'v1')
        downloadJsons.getJsonObjects(client)
        ###
        ### Download generated error-objects from cloud storage
        downloadErrors.getErrorObjects(client)
    except:
        pass
    
    
    
    
    
    
    
    
    
    