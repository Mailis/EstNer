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

timeDir = time.strftime("%d_%m_%Y")
pathToErrorFile="/var/www/html/master/downloading_errors/"
#create dir if does not exist
if (not os.path.isdir(pathToErrorFile)) & (not os.path.exists(pathToErrorFile)):
    os.makedirs(pathToErrorFile)

def printException(pathToErrorFile, errString=""):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    err= (time.strftime("%d/%m/%Y_%H:%M:%S") + " " + errString + ' {}_EXCEPTION_IN_({},_LINE_{}_"{}"):_{}_'.format(exc_type, filename, lineno, line.strip(), exc_obj) + "\n\n")
    #TODO!*done
    jf = open(pathToErrorFile+timeDir+".txt", 'a')
    jf.write(err)#
    jf.close()


#/home/ubuntu/Desktop/empty_g/parseg.py
dirToSaveRDFfiles = "/var/www/html/master/rdf_files/"
rdfFnames = ["ORG", "PER", "LOC"]
dirToSaveStatistics = "/var/www/html/master/statistics/"
def mergeRDFfiles():
    global rdfFnames
    global dirToSaveRDFfiles
    
    try:
        for dname in rdfFnames:
            g_old_path = dirToSaveRDFfiles + dname + ".rdf" #/var/www/html/master/rdf_files/ORG.rdf
            rdf_file_dir = dirToSaveRDFfiles + dname #/var/www/html/master/rdf_files/ORG
            
            g_new = Graph()
            for rdf_file in listdir(rdf_file_dir):
                tmp_path = rdf_file_dir + "/" + rdf_file #/var/www/html/master/rdf_files/ORG/<worker-1>.rdf
                try:
                    g_new.parse(tmp_path)
                except:
                    printException(pathToErrorFile, errString="cannot merge RDF")
                    pass
            if (os.path.exists(g_old_path)):
                try:
                    g_new.parse(g_old_path)
                    g_new.serialize(g_old_path, format='pretty-xml', encoding='utf-8') 
                except:
                    printException(pathToErrorFile, errString="cannot merge RDF")
                    pass   
                #delete used files
                os.system("sudo rm -r " + rdf_file_dir+"/*")
            else:
                try:
                    g_new.serialize(g_old_path, format='pretty-xml', encoding='utf-8') 
                except:
                    printException(pathToErrorFile, errString="cannot merge RDF")
                    pass
    except:
        printException(pathToErrorFile, errString="merge RDF")
        pass
    for dname in rdfFnames:
        g_old_path = dirToSaveRDFfiles + dname + ".rdf" 
        if (os.path.exists(g_old_path)):
            g_old = Graph()
            g_old.parse(g_old_path)   
            jf = open(dirToSaveStatistics+timeDir+".txt", 'a')
            jf.write(dname + " nr of triples: " + str(len(g_old)) + "\n")
            jf.close() 



if __name__ == '__main__':
    global rdfFnames
    global dirToSaveRDFfiles

    www_data = json.loads(sys.argv[1])
    ip = www_data["ip"]
    remoteName = www_data["name"]

    if not os.path.isdir(dirToSaveRDFfiles):
        os.makedirs(dirToSaveRDFfiles)

    input_file_url = "http://" + ip + "/rdf_files/"
    inp=("INPUT " + str(input_file_url))
    for fname in rdfFnames:
        input = input_file_url + fname + ".rdf"
        outputDir = dirToSaveRDFfiles + fname + "/"
        if not os.path.isdir(outputDir):
            os.makedirs(outputDir)
        output = outputDir + remoteName + ".rdf"
        try:
            urr(input, output)
        except:
            pass
    
    mergeRDFfiles()


