#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

#import getpass
#print("USER: " + getpass.getuser())

#print("Content-Type: text/plain;charset=utf-8")

'''
Created on Feb 24, 2015
http://pymotw.com/2/multiprocessing/mapreduce.html
'''

import os, sys, json, time
from multiprocessing import Pool

import initRdf
import downloadFilesFromLog
import datetime
from urllib.request import urlsplit
from urllib.request import urlretrieve as urr
from os import listdir
import json
import commonVariables as comm
import commonMethods as commeth 

nrOfDownloads = commeth.nrOfDownloads

od=None

ajadir = comm.timeDir

def isNeededUrl(url):
    neededUrl = True
    fileName =  (((urlsplit(url).path).lower()).split("/"))[-1]
    if(fileName in comm.undesiredFileName):
        neededUrl = False
    if(neededUrl):        
        extSplit = (fileName.split("."))
        lastIndex = len(extSplit)-1
        if(lastIndex > 0):
            extension = (extSplit[lastIndex])
            if(extension in comm.undesiredFileExtensions):
                neededUrl = False
    if(neededUrl):
        for udft in comm.undesiredFileTypes:
            if(udft in url):
                neededUrl = False
                break
    return neededUrl


def sendUrl(url):
    global od
    downloadFilesFromLog.saveMetadata(url, od)

 


'''
http://crawler.archive.org/articles/user_manual/glossary.html#discoverypath
logfile row structure description:
line[0] timestamp
line[1] status code
line[2] size of the downloaded document in bytes
line[3] url of downloaded file (document)
line[4]
  R - Redirect
  E - Embed
  X - Speculative embed (aggressive/Javascript link extraction)
  L - Link
  P - Prerequisite (as for DNS or robots.txt before another URI)
line[5] basic url, reference
line[6] content type of basic url, line[5]
line[7] the id of the worker thread that downloaded this document
line[8] timespan+download_time, diff to line[0]
line[9] sha1
line[10] -
line[11] content-size

#there is only line[3] and line[5] that are needed
#there is content-type only for line[5] given
#content type for line[3] has to be asked while making request
'''

#for recording statistics
#record that some logfile is already processed
processed_logfiles_dir = "../statistics/processed_logfiles/"
processed_logfiles_path = processed_logfiles_dir+"proc_log_files.txt"
if not os.path.isdir(processed_logfiles_dir):
        os.makedirs(processed_logfiles_dir)
	
        
nrOfJobs=""
logfileName =""
'''
'''

start = datetime.datetime.now()
currTime = time.strftime("%d/%m/%Y_%H:%M:%S")
'''
'''

if __name__ == "__main__":
    #print("The Python version is %s.%s.%s" % sys.version_info[:3])
    #http://stackoverflow.com/questions/6335839/python-how-to-read-n-number-of-lines-at-a-time

    logfile = json.loads(sys.argv[1])
    logfileName = logfile
    #print(os.getcwd())
    #logfile = "/var/www/html/logfiles/crawl_detail3.log"
    #logfileName = logfile
    od = initRdf.OntologyData(comm.pathToRDFdir)
    initRdf.RdfFilesCreator(od)
    nr_of_log_rows = 0
    co=0#for debugging
    jobs = []
    with open(logfile) as f:
        for line in f:
            nr_of_log_rows += 1 #for statistics
    #for line in logs:
            co+=1
            if (co > 0):#&(co <= 500000):
                splitted = line.split()
                tyyp = splitted[6]
                #disable unwanted content types
                if( tyyp not in comm.undesiredFileTypes):
                    action = splitted[4]
                    #print(tyyp)
                    #call parser for every line
                    if "P" in action:#dns or robots.txt, send basic url
                        url = splitted[5]
                        neededUrl = isNeededUrl(url)
                        if(neededUrl):
                            jobs.append(url)
                    else:#send url of file
                        url = splitted[3]
                        neededUrl = isNeededUrl(url)
                        if(neededUrl):
                            jobs.append(url)
    
    print("{} download jobs queued".format(len(jobs))  + "\n")
    nrOfJobs=len(jobs)

    pool = Pool(processes=os.cpu_count())
    pool.map(sendUrl, jobs)
    pool.close()
    pool.join()


#FINALLY add triples from lists, that left over. 
#In the file 'getEntities',
#when chunking shared lists, it starts to create RDF-s, when list size exceeds chunksize (e.g. 25 items),
#but when there are eventually less items in lists than chunksize, the items in it were not tripled so far.
#print("PER")
if(od.sharedList_per._callmethod('__len__') > 0):
    #print(od.sharedList_per._callmethod('__len__'))
    try:
        perManager = initRdf.PeopleManager(od)
        perManager.addTriples(od.sharedList_per)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_ORG_entities")
#print("ORG")
if(od.sharedList_org._callmethod('__len__') > 0):
    #print(od.sharedList_org._callmethod('__len__'))
    try:
        orgManager = initRdf.OrganizationManager(od)
        orgManager.addTriples(od.sharedList_org)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_ORG_entities_leftover")
#print("LOC")
if(od.sharedList_loc._callmethod('__len__') > 0):
    #print(od.sharedList_loc._callmethod('__len__'))
    try:
        locManager = initRdf.LocationManager(od)
        locManager.addTriples(od.sharedList_loc)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_LOC_entities_leftover")

#statistics
end = datetime.datetime.now() 
span = end-start

jf = open(processed_logfiles_path, 'a', encoding='utf-8')
jf.write(currTime + " " + logfileName.replace(" ", "").replace("..", "") + " " + str(nrOfJobs) + " " + str(span) + " " + str(comm.chunksize) + " " + str(nr_of_log_rows) + " ")
jf.close()
''''''
#print("SPAN: ", span)  
print("totalseconds: ", span.total_seconds())  

''''''
commeth.measureDownloadsTime(processed_logfiles_path, ajadir)







