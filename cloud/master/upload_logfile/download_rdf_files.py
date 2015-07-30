#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# enable debugging
import cgitb
cgitb.enable()

import os, sys
import json
import time
from urllib.request import urlretrieve as urr
import linecache
from os import listdir
from rdflib import Graph

import commonVariables as comm


#/home/ubuntu/Desktop/empty_g/parseg.py
#dirToSaveRDFfiles = "/var/www/html/master/rdf_files/"

#dirToSaveStatistics = "/var/www/html/master/statistics/"
def mergeRDFfiles():
    
    try:
        for dname in rdfFnames:
            g_old_path = comm.pathToRDFdir + dname + ".rdf" #file: /var/www/html/master/rdf_files/ORG.rdf
            rdf_file_dir = comm.pathToRDFdir + dname #dir: /var/www/html/master/rdf_files/ORG
            
            g_new = Graph()
            for rdf_file in listdir(rdf_file_dir):
                tmp_path = rdf_file_dir + "/" + rdf_file #/var/www/html/master/rdf_files/ORG/<worker-1>.rdf
                try:
                    g_new.parse(tmp_path)
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, errString="cannot merge RDF")
                    pass
            if (os.path.exists(g_old_path)):
                try:
                    g_new.parse(g_old_path)
                    g_new.serialize(g_old_path, format='pretty-xml', encoding='utf-8') 
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, errString="cannot merge RDF")
                    pass   
                #delete used files
                os.system("sudo rm -r " + rdf_file_dir+"/*")
            else:
                try:
                    g_new.serialize(g_old_path, format='pretty-xml', encoding='utf-8') 
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, errString="cannot merge RDF")
                    pass
    except:
        comm.printException(comm.pathToSaveDownloadErrors, errString="merge RDF")
        pass
    



if __name__ == '__main__':
    rdfFnames = comm.rdfFnames

    www_data = json.loads(sys.argv[1])
    ip = www_data["ip"]
    remoteName = www_data["name"]
    mylargefile = www_data["statfile"]

    input_file_url = "http://" + ip + "/rdf_files/"
    inp=("INPUT " + str(input_file_url))
    for fname in rdfFnames:
        input = input_file_url + fname + ".rdf"
        outputDir = comm.pathToRDFdir + fname + "/"
        if not os.path.isdir(outputDir):
            os.makedirs(outputDir)
        output = outputDir + remoteName + ".rdf"
        try:
            urr(input, output)
        except:
            pass
    
    mergeRDFfiles()
    



