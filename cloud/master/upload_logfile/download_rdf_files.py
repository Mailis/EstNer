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
            #temporary dirs ORG, LOC, PER
            rdf_file_dir = comm.pathToRDFdir + dname #dir: /var/www/html/master/rdf_files/ORG
            g_copy_path = comm.rdf_copypath + dname + ".rdf" #file: /var/www/html/master/rdf_copy/ORG.rdf
            
            g_new = Graph()
            g_new_for_copy = Graph()
            for rdf_file in listdir(rdf_file_dir):
                tmp_path = rdf_file_dir + "/" + rdf_file #/var/www/html/master/rdf_files/ORG/<worker-1>_<date_dir>.rdf
                try:
                    g_new.parse(tmp_path)#load temporary file into graph
                    g_new_for_copy.parse(tmp_path)#load temporary file into graph
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, errString="cannot load temporary file into graph")
                    pass
            if (os.path.exists(g_old_path)):#there is an existing oath to rdf-file
                try:
                    g_new.parse(g_old_path) #load old file into graph, adding it to new graph
                    g_new.serialize(g_old_path, format='pretty-xml', encoding='utf-8') 
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, errString="cannot merge RDF")
                    pass   
                #delete used files
                os.system("sudo rm -r " + rdf_file_dir+"/*")
            else:#no existing path to RDF files yet
                try:
                    g_new.serialize(g_old_path, format='pretty-xml', encoding='utf-8') 
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, errString="cannot create RDF")
                    pass
                
                
                
            ##BACKUP RDF files
            if (os.path.exists(g_copy_path)): #there is an existing oath to rdf-file
                try:
                    g_new_for_copy.parse(g_copy_path) #load old file into graph, adding it to new graph
                    g_new_for_copy.serialize(g_copy_path, format='pretty-xml', encoding='utf-8') #save into file
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, errString="cannot merge backup  RDF")
                    pass   
            else:#no existing path to RDF files yet
                try:
                    g_new_for_copy.serialize(g_copy_path, format='pretty-xml', encoding='utf-8')  #save into file
                except:
                    comm.printException(comm.pathToSaveDownloadErrors, errString="cannot create backup RDF")
                    pass
    except:
        comm.printException(comm.pathToSaveDownloadErrors, errString="merge RDF")
        pass
    



if __name__ == '__main__':
    rdfFnames = comm.rdfFnames

    www_data = json.loads(sys.argv[1])
    ip = www_data["ip"]
    remoteName = www_data["name"]
    #mylargefile = www_data["statfile"]

    input_file_url = "http://" + ip + "/rdf_files/"#parent folder of incoming path of RDF
    #new file system
    #temporary target folder to download file system of rdf_files' folder of a worker
    outp = comm.outp_temp_rdf
    if not os.path.isdir(outp): #make dirs ORG, PER, LOC in master's dir 'rdf_files'
        os.makedirs(outp)
    #the resulting filesystem becomes
    #/var/www/html/outputf/
    #/var/www/html/outputf/<ip>/
    #/var/www/html/outputf/<ip>/rdf_files/
    #/var/www/html/outputf/<ip>/rdf_files/<datetime>/
    ls = os.system('wget -r --no-parent --reject "index.html*" --directory-prefix=' + outp + ' ' + input_file_url)
    
     
    #walk through temporary filesystem of rdf_files' folder of a worker
    #in outp = "/var/www/html/outputf/"
    #get subfolders of 'outputf/.../rdf_files/'
    f_subfolder = outp + "/" + ip + "/rdf_files/"
    date_folders = os.listdir(f_subfolder)
    
    for date_dir in date_folders:#/var/www/html/outputf/<ip>/rdf_files/<date_dir>/
        remote_date_dir_path =  input_file_url + date_dir
    
        for fname in rdfFnames:
            #rdf URL in worker machine
            #/var/www/html/outputf/<ip>/rdf_files/<date_dir>/<fname>.rdf
            #/var/www/html/outputf/<ip>/rdf_files/<date_dir>/LOC.rdf
            #/var/www/html/outputf/<ip>/rdf_files/<date_dir>/ORG.rdf
            #/var/www/html/outputf/<ip>/rdf_files/<date_dir>/PER.rdf
            inputf = remote_date_dir_path + "/" + fname + ".rdf"
            #create
            #rdf dirs' paths in master machine: 
            #/var/www/html/rdf_files/<fname>/
            #e.g.
            #/var/www/html/rdf_files/LOC/
            #/var/www/html/rdf_files/ORG/
            #/var/www/html/rdf_files/PER/
            outputDir = comm.pathToRDFdir + fname + "/"
            if not os.path.isdir(outputDir): #make dirs ORG, PER, LOC in master's dir 'rdf_files'
                os.makedirs(outputDir)
            
            #rdf file path in master machine:
            #/var/www/html/rdf_files/<fname>/<remoteName>_<date_dir>_.rdf
            #e.g.
            #/var/www/html/rdf_files/rdf_files/ORG/worker1_08_2015_09_10.rdf
            #old was: output = outputDir + remoteName + ".rdf" 
            output = outputDir + remoteName + "_"  + date_dir + "_" + ".rdf"
            try:
                urr(inputf, output)
            except:
                pass
    
    mergeRDFfiles()
    



