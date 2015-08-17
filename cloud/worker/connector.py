#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()

#print("Content-Type: text/plain;charset=utf-8")

'''
Created on Feb 24, 2015
'''

import os, sys, json, time
import datetime
from multiprocessing import Pool

from storage import commonvariables as comm
import download_files_from_log
import init_rdf



def sendUrl(url):
    download_files_from_log.saveMetadata(url, od)



def setNewRDFdir():
    ajastr = comm.pathToRDFbaseDir + time.strftime("%d_%m_%Y_%H_%M") + "/"
    if not os.path.isdir(ajastr):
        os.makedirs(ajastr)
    #change rdf-dir variable
    comm.pathToRDFdir = ajastr
    
minute_start = -1
rdfInterval=2
dirs=sorted(os.listdir(comm.pathToRDFbaseDir))
if len(dirs)==0:#if no RDF-dirs are created yet   
    minute_start = int(time.strftime("%M")) 
    setNewRDFdir()#changes variable 'comm.pathToRDFdir'
else:#if there are already some dir
    comm.pathToRDFdir = comm.pathToRDFbaseDir + dirs[-1] + "/"#take newest dir
        

od = None
nrOfJobs=""
start = datetime.datetime.now()
timeDir = time.strftime("%d_%m_%Y")+ "/"


if __name__ == "__main__":
    minute = int(time.strftime("%M"))
    if( ( minute%rdfInterval is 0) & (minute_start != minute)):
        setNewRDFdir()#changes variable 'comm.pathToRDFdir'
    '''
    setNewRDFdir()
    '''
    od = init_rdf.OntologyData()  
    init_rdf.RdfFilesCreator(od)
    
    '''
    #
    #DEBUGGING
    #jf = open("/var/www/html/ch.txt", 'a')
    #jf.write(str(datetime.datetime.now()) + "\nCOUNTER: " +  str(counter) + "\n\n")
    #jf.write(str(datetime.datetime.now()) + "\nDATA: " +  str(data) + "\n\n")
    #jf.close()
    
    dat = json.loads(sys.argv[1])
    data = (json.loads(json.loads(sys.argv[1])))["data"]
    item = []
    for d in data:
        item.extend(d.values())
    print(item)
    #data = json.loads((json.loads(sys.argv[1]))["data"])
    #jobs = list(data.values())
    jobs = item
    nrOfJobs=len(jobs)
    pool = Pool(processes=os.cpu_count())
    pool.map(sendUrl, jobs)
    pool.close()
    pool.join()
    #endof debugging
    '''
    data0 = None
    data = None
    #
    try:
        data =  json.loads((  json.loads(sys.argv[1])  )["data"])
        data0 =  json.loads(sys.argv[1]) 
        #data =  json.loads((data0)["data"]) 
        comm.chunksize =  int(json.loads((data0)["chunksize"])) 
        
        #jf = open("/var/www/html/ch.txt", 'a')
        #jf.write(str(datetime.datetime.now()) + "\nCHUNKSIZE: " +  str(comm.chunksize) + "\n\n")
        #jf.close()
        
    except:
        comm.printException(comm.pathToSaveProgrammingErrors, "load_DATA_in_connector")
        pass

    if(data is not None):
        jobs = list(data.values())
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
        perManager = init_rdf.PeopleManager(od)
        perManager.addTriples(od.sharedList_per)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_ORG_entities")
        pass


if(od.sharedList_org._callmethod('__len__') > 0):
    #print(od.sharedList_org._callmethod('__len__'))
    try:
        orgManager = init_rdf.OrganizationManager(od)
        orgManager.addTriples(od.sharedList_org)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_ORG_entities_leftover")
        pass

if(od.sharedList_loc._callmethod('__len__') > 0):
    #print(od.sharedList_loc._callmethod('__len__'))
    try:
        locManager = init_rdf.LocationManager(od)
        locManager.addTriples(od.sharedList_loc)
    except:
        comm.printException(comm.initRdfErrorsFilePath, "get_LOC_entities_leftover")
        pass






