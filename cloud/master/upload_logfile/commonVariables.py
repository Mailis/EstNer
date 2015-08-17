#!/usr/bin/python2
# -*- coding: utf-8 -*-
# enable debugging
import cgitb
cgitb.enable()
import os
import time
import sys
import linecache
import codecs
import datetime

if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')


#variabless for authentication against GCE
MASTERINSTANCE_NAME = "master"
DEFAULT_ZONE = 'europe-west1-b'
PROJECT_ID = "estn-1006" # 
METADATA_SERVER = ('http://metadata/computeMetadata/v1/instance/service-accounts')
SERVICE_ACCOUNT = 'default'

rdfFnames = ["ORG", "PER", "LOC"]

chunksize=500

#directory where the system software is located in server
parentDir = "/var/www/html/"

'''
    Lists file types, where one cannot find entities
'''
desiredFileTypes = ['excel', 'json', 'html', 'xml', 'pdf', 'plain', 'text']#
undesiredFileTypes = ['image', 'no-type', 'javascript', 'flash', 'dns', 'ttf', 'js', 'css', 'video', "audio", 'zip', "video", "mpeg", "x-font-otf", "x-font-woff"]
undesiredFileExtensions = ['jpg', 'jpeg', 'gif', 'png', 'bmp', 'ico', 'swf', 'js', 'css', 'php', 'ShockwaveFlash', 'dns', 'ttf', "video", "audio", "mpeg"]
undesiredFileName = ['robots.txt', '/robots.txt']

'''
    Directories and paths so save errors and statistics etc.
'''
timeDir = time.strftime("%d_%m_%Y")
#GCE bucket where workers store json-metadata-files
jsonsDir = "datadownload_jsons"
#downloaded datasets
downloadsDir_for_excels = parentDir + "datadownload/downloaded_files/"
downloadsDir = parentDir + "datadownload/downloaded_files/"+timeDir+"/"
#create folders for datasets (and jsons)
if not os.path.isdir(downloadsDir):
    os.makedirs(downloadsDir)
#local path for json-objects
jsonsDir_local = parentDir + "datadownload/jsons/"
if not os.path.isdir(jsonsDir_local):
    os.makedirs(jsonsDir_local)
    
    
#path for saving monthly update statistics
monthly_updates_dir = parentDir + "statistics/monthly_updates"
if not os.path.isdir(monthly_updates_dir):
    os.makedirs(monthly_updates_dir)
monthly_updates_path = monthly_updates_dir + "/" + time.strftime("%d_%m_%Y") + ".txt"    

#path for saving times when some post request was made
postreq_dir = parentDir + "statistics/postrequests"
if not os.path.isdir(postreq_dir):
    os.makedirs(postreq_dir)
postreq_path = postreq_dir + "/" + time.strftime("%d_%m_%Y") + ".txt"    
    
    

#for recording statistics
#record that some logfile is already processed
processed_logfiles_dir = parentDir + "statistics/processed_logfiles/"
if not os.path.isdir(processed_logfiles_dir):
    os.makedirs(processed_logfiles_dir)

#folder for saving collected rdf_files
outp_temp_rdf = "/var/www/html/outputf/"
pathToRDFdir = parentDir + "rdf_files/"
#create folder for rdf-files
if not os.path.isdir(pathToRDFdir):
    os.makedirs(pathToRDFdir)   
    
#backups
rdf_copypath = parentDir + "rdf_copy/"
#create folder for rdf-files
if not os.path.isdir(rdf_copypath):
    os.makedirs(rdf_copypath) 


#paths for errors (saved in GCE bucket 'generated_files')
errorsBucket = "generated_files"

dirToSaveConnectionErrors = parentDir + errorsBucket + "/connection_errors/"
pathToConnectionErrors = dirToSaveConnectionErrors + timeDir + ".txt"

dirToSaveJsonErrors = parentDir + errorsBucket + "/json_errors/"
pathToSaveJsonErrors = dirToSaveJsonErrors + timeDir + ".txt"

dirToSaveProgrammingErrors = parentDir + errorsBucket + "/programming_errors/"
pathToSaveProgrammingErrors = dirToSaveProgrammingErrors + timeDir + ".txt"

dirToSaveDownloadErrors = parentDir + errorsBucket + "/download_errors/"
pathToSaveDownloadErrors = dirToSaveDownloadErrors + timeDir + ".txt"

dirToSaveAuthErrors = parentDir + errorsBucket + "/auth_errors/"
pathToSaveauthErrors = dirToSaveAuthErrors + timeDir + ".txt"

pathToUpdateErrorsDir = parentDir + errorsBucket + "/update_errors/"
updateErrorsFilePath = pathToUpdateErrorsDir + timeDir + ".txt"

pathToInitRdfErrorsDir = parentDir + errorsBucket + "/tripling_errors/"
initRdfErrorsFilePath = pathToInitRdfErrorsDir + timeDir + ".txt"

parsing_errorsDir = parentDir + errorsBucket + "/parsing_errors/"
pathToSaveParsingErrors = parsing_errorsDir + timeDir + ".txt"

if not os.path.isdir(dirToSaveConnectionErrors):
    os.makedirs(dirToSaveConnectionErrors)     
if not os.path.isdir(dirToSaveAuthErrors):
    os.makedirs(dirToSaveAuthErrors) 
if not os.path.isdir(dirToSaveJsonErrors):
    os.makedirs(dirToSaveJsonErrors)   
if not os.path.isdir(dirToSaveProgrammingErrors):
    os.makedirs(dirToSaveProgrammingErrors)
if not os.path.isdir(dirToSaveDownloadErrors):
    os.makedirs(dirToSaveDownloadErrors)
if not os.path.isdir(pathToInitRdfErrorsDir):
    os.makedirs(pathToInitRdfErrorsDir)
if not os.path.isdir(pathToUpdateErrorsDir):
    os.makedirs(pathToUpdateErrorsDir)
if not os.path.exists(parsing_errorsDir):
    os.makedirs(parsing_errorsDir)
  
#create date object of dirname
#incomming string 'ajas6ne'
#has format "Y_m_d"
#e.g. "2013_ 7_20"
def makeDateObj(ajas6ne):
    numbrid = ajas6ne.split("_")
    return datetime.datetime(int(numbrid[0]), int(numbrid[1]), int(numbrid[2]))



def printException(pathToErrorFile, errString=""):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    err= (errString + ' {}_EXCEPTION_IN_({},_LINE_{}_"{}"):_{}_'.format(exc_type, filename, lineno, line.strip(), exc_obj) + "\n\n")  
    jf = open(pathToErrorFile, 'a')
    jf.write(err)#
    jf.close() 
    
def measureDownloadsTime(path_to_stat_file, ajadir):
    start = datetime.datetime.now()
    currTime = time.strftime("%H:%M:%S")
    nrOfDownloads = 0#dowloadFromJsons(ajadir)
    end = datetime.datetime.now() 
    span = end-start
    try:
        jf = open(path_to_stat_file, 'a', encoding='utf-8')
        jf.write(currTime + " " + str(nrOfDownloads) + " " + str(span) + " " + "\n")
        jf.close()
    except:
        printException(pathToSaveDownloadErrors, errString="download")
        pass   
     
def saveStatistics(dirname, note):
    filename = dirname.split('/')[-1]
    fname = "".join(filename.split('.')) + ".txt"
    jf = open(processed_logfiles_dir+fname, 'a')
    jf.write(str(datetime.datetime.now()) + "\n" + note)
    jf.close()
    
    