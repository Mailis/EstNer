#!/usr/bin/python
# -*- coding: utf-8 -*-

import commonVariables as comm
import os


def importExcelFiles(WORKER_INSTANCES):
    list_len = len(WORKER_INSTANCES)
    if list_len > 0:
        for instance in WORKER_INSTANCES:
            wwwip = instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']#download excels            
            try:
                #excels_url ="http://146.148.115.150/downloaded_files/"
                excels_url = "http://" + wwwip + "/downloaded_files/"
                dest = comm.downloadsDir_for_excels
                os.system('wget  -r --no-parent -nH --cut-dirs=1 --reject "index.html*" ' + excels_url + " -P " + dest)
            except:
                comm.printException(comm.pathToSaveDownloadErrors, errString="collecting excels")
                pass
            
            
            
            
            
