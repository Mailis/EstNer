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



      
nrOfJobs=""

od = init_rdf.OntologyData(comm.pathToRDFdir)
init_rdf.RdfFilesCreator(od)

start = datetime.datetime.now()
timeDir = time.strftime("%d_%m_%Y")+ "/"


if __name__ == "__main__":
    
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






