#!/usr/bin/python
# -*- coding: utf-8 -*-
# enable debugging
import requests
import commonVariables as comm
import json

#the size of the list sent to each worker, 
#depends on the number of CPUs of a  worker
#defines the size of list of URLs.
#size depends on maximum nr of CPUs in a worker.
#it becomes twice as nr of CPUs
#this is for balancing workload among workers.
def defPostListSize(worker_counter, ipList_tuple):
    nr_of_worker_cpu = ipList_tuple[worker_counter][1]
    return (2*int(nr_of_worker_cpu)) 

#this method is called, when the URLs-list is full and ready 
#for posting to a worker in order       
def postListToWorker(wip, urlsList):
    pikkus = len(urlsList)
    dik = dict(zip(range(pikkus),urlsList))
    address = "http://"+wip
    try:
        requests.post(address, data={'data':json.dumps(dik), 'chunksize':json.dumps(comm.chunksize)})
        return 1
    except:
        comm.printException(comm.pathToConnectionErrors, errString='ConnectionError_to_worker_' + wip)
        return 0
        pass

 
def deleteRDFsInWorkers(ipList):
    #delete RDF-files and download excel-files in each worker
    for workerip in ipList:
        worker_address = "http://" + workerip + "/delete_rdf_files.php"
        try:
            requests.post(worker_address)
        except:
            comm.printException(comm.pathToConnectionErrors, errString='ConnectionError_to_worker_' + workerip)
            continue 
        
def deleteRDFsInWorker(workerip):
    #delete RDF-files and download excel-files in a worker
    worker_address = "http://" + workerip + "/delete_rdf_files.php"
    try:
        requests.post(worker_address)
    except:
        comm.printException(comm.pathToConnectionErrors, errString='ConnectionError_to_worker_' + workerip)
        
        
    
def detectConnection(ipList, worker_counter, urlsList):
    connected = 0
    while connected is 0:
        connected = postListToWorker(ipList[worker_counter], urlsList)
        if(connected == 0):
            worker_counter += 1
    return worker_counter
            
            
            