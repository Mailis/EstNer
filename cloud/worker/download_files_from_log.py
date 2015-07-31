#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# enable debugging
import cgitb
cgitb.enable()
'''
Created on Feb 25, 2015
http://kaira.sgo.fi/2014/05/saving-and-loading-data-in-python-with.html?showComment=1424895576114#c1010617980067477531
'''
import os, os.path, sys
import json, time
import hashlib
import requests
#from urllib import request as ur
from urllib.parse import urlparse
from urllib import error as urr
import subprocess

import fileparser
from storage import commonvariables as comm
 

comm.timeDir = time.strftime("%d_%m_%Y")

#method 'insertValuesToDict'
#creates the mteta data structure for accessed document
#it writes metadata into directory type 
#which is later serialized as json-string
#and saved into file '<hostname>.json'.
#this structure holds the system together:
#the document's URL and access-date is used in downloading processes 
#and while monthly updating with documet's content-hash and filename-hash
#doc's metadata is used in sorting/filtering through datasets: 
#datasets can be filtered e.g by 
#(part of) hostname
#content type
#accessed date, etc.
def insertValuesToDict(dictnry, localFilename, page_redirected, page_info, page_sha254, page_status ):
    try:
        dictnry[localFilename] = dict()
        dictnry[localFilename][page_sha254] = page_info
        dictnry[localFilename][page_sha254]["localFilename"] = localFilename
        dictnry[localFilename][page_sha254]["file_url"] = page_redirected
        dictnry[localFilename][page_sha254]["sha224"] = page_sha254
        dictnry[localFilename][page_sha254]["status"] = page_status
        dictnry[localFilename][page_sha254]["timeDir"] = comm.timeDir
        return dictnry
    except:
        comm.printException(comm.pathToSaveJsonErrors, "insertValuesToDict")
        pass


'''
'saveMetadata' is a core method of this file.
It tries to open document at some URL. If it is successful,
thihs method generates specially structured json-file for doc's metadata.
The json-file is then saved into Google Cloud Storage.
This metadata is used later for
1. downloading processed files
2. monthly checking for updates
3. for browsing datasets: this structure enables to browse datasets e.g. by
    a). download date;
    b). inserting part of URL-string;
    c). content type;
    d...etc, according to other metadata.
After saving metadata, the program continues with parsing accessed documents and then 
with Estner for extracting entities, then saving the entities into rdf files.
'''                     
def saveMetadata(url, od):
    
    #save the result of trying of opening a page into variable 'canOpen'
    canOpen = True
    try:
        #try to open document at URL
        redirectedTo = requests.get(url).url
    except:
        #it was not possible to open this web document
        canOpen = False
        #save exception (error of getting web document)
        errStr = (url + " Cannot_open_web-source \n" )
        comm.printException(comm.pathToSaveJsonErrors, errStr)
        #continue without terminating a program
        pass
    #continue only if 'canOpen' is still true
    if canOpen is True:
        print("can open: " + str(canOpen))
        if not os.path.isdir(comm.jsonsDir):
            os.makedirs(comm.jsonsDir)
        try:
            #in following, use only the URL, where one was redirected, if at all
            page = requests.get(redirectedTo)
            statusCode = page.status_code
            #textual content of a doc
            pageread = page.text
            #get doc's metadata
            pageInfo = dict(page.headers)
            #generate filename for local storage:
            #it will be the hash of doc URL
            localFilename = comm.getUrlSHA(redirectedTo)
            #important metadata: content type
            contentType = page.headers['content-type']
            #base_url denotes host name, 
            #all documents that are from the same host, will be saved into same json-file
            #base_url becomes also json-file name (pathToSaveMetadata)
            baseUrl = (urlparse(redirectedTo)).netloc
            #generate hash of the content of  doc.
            #this hash is used later for detecting whether the doc's content has changed or not.
            # this chnge-detection happens in cases of 
            #1. monthly update
            #2. current method, when appears, that this URL have processed earlier
            sha224_ = (hashlib.sha224(pageread.encode('utf-8')).hexdigest())
            #important data for parsers: encoding
            _encoding = page.encoding
            #_encoding = comm.getDocumentEncoding(contentType, pageread)
            #print("-----------------------------------------------------")
            
            #exclude doc types where it is not possible to find textual  content: e.g images, videos
            isDesiredType = comm.isDesiredContent(contentType, od)
            #continue only witj desired types
            if(isDesiredType):
                #jsonsDir is actually a so called 'bucket' name in Google Cloud Storage
                jsonsDir = comm.jsonsDir
                print(jsonsDir)
                #jsonsFile becomes a so called 'object' inside a bucket
                #object's name is URL's host name and extension is '.json'
                jsonsFile = baseUrl + ".json"
                #build dictionary of address of object of this meta data
                jsonsPath = dict()
                jsonsPath["object"] = jsonsFile#'hostname.json'#
                jsonsPath["bucket"] = jsonsDir#e.g. 'datadownload_json'#
                pathToSaveMetadata_ = json.dumps(jsonsPath)
                #save meta data into dictionary structure
                infoDict_tmp = dict()
                infoDict_tmp["base_url"] = baseUrl
                infoDict = insertValuesToDict(infoDict_tmp, localFilename, redirectedTo, pageInfo, sha224_, statusCode )
                #convert dictionary into json-string
                jsondata = json.dumps(infoDict, indent=4)
                #dict for sending collected data to 'updateObj.py'
                insertJson = dict()
                insertJson["jsondata"] = jsondata
                insertJson["localFilename"] = localFilename
                insertJson["redirectedTo"] = redirectedTo
                insertJson["pageInfo"] = pageInfo
                insertJson["sha224_"] = sha224_
                insertJson["statusCode"] = statusCode
                insertJson["timeDir"] = comm.timeDir
                insertJson["address"] = pathToSaveMetadata_
    
                #variable 'someNewData' is for storing knowledge about
                #whether this doc at this url 
                #is processed earlier:
                #1. if Yes and doc's content has changed, then 'someNewData' becomes True; else remains False
                #2. if No, then 'someNewData' becomes True 
                someNewData = False
                #string for saving a unique error message
                errr=""
                try:
                    #convert dictionary into json-string for sending argument to 'updateObj.py'
                    jd = json.dumps(insertJson)
                    #get info back about whether here is some new data
                    #'p' is a returned boolean value of 'someNewData'
                    #communication with google-python-api-client is done using older version, python2.7
                    p = subprocess.Popen(["python2", "storage/updateObj.py", jd], stdout=subprocess.PIPE)
                    out, err = p.communicate()
                    someNewData  = out.decode()
                    errr = str(err).lower()
                    print("\nsomeNewData " + str(someNewData))
                    print("\nerrr " + str(errr))
                except:
                    errstr = errr if ((errr != "") & (errr != "none")) else "storage-updateObj.py-ERROR"
                    comm.printException(comm.pathToSaveJsonErrors, errstr)
                    pass
                
                #continue with parsing of doc only when new data was detected
                if someNewData: 
                    sendFileToParser(contentType, baseUrl, redirectedTo, od, _encoding, localFilename, pageread)
        #record errors                    
        except urr.HTTPError as e:
            errStr = (redirectedTo + " HTTPError " + str(e.code) + " " + str(e.reason) + " \n" )
            comm.printException(comm.pathToSaveJsonErrors, errStr)
            pass
        except urr.URLError as e:
            errStr = (redirectedTo + " URLError " + str(e.reason) + " \n" )
            comm.printException(comm.pathToSaveJsonErrors, errStr)
            pass
        except IOError as e:
            errStr = (redirectedTo + " " + str("I/O_erRror({0}):_{1}".format(e.errno, e.strerror)) + "\n")
            comm.printException(comm.pathToSaveJsonErrors, errStr)
            pass
        except ValueError:
            errStr = (redirectedTo + " ValueError_Could_not_convert_data_to_an_integer.\n") 
            comm.printException(comm.pathToSaveJsonErrors, errStr)
            pass
        except TypeError:
            errStr = (redirectedTo + " TypeError\n")  
            comm.printException(comm.pathToSaveJsonErrors, errStr)
            pass
        except:
            errStr = (redirectedTo + " Unexpected_error:_" + (str(sys.exc_info()[0])) + "\n")
            comm.printException(comm.pathToSaveJsonErrors, errStr)
            pass


''' 
send read doc content for parsing, 
where every content type uses different parser
'''
def sendFileToParser(contentType, baseUrl, redirectedTo, od, _encoding, localFilename, pageread):
    contentType = contentType.lower()
    #it is possible to read excel-type and pdf only after downloading this excel-doc
    if(("excel" in contentType) or ("pdf" in contentType)):
        try:
            dirToSaveDownloads = comm.downloadsDir + baseUrl
            if not os.path.isdir(dirToSaveDownloads):
                os.makedirs(dirToSaveDownloads)
            fileparser.spreadURLsByContentType(redirectedTo, None, contentType, od, _encoding, filePath = (dirToSaveDownloads + "/" + localFilename))
        except:
            comm.printException(comm.pathToSaveProgrammingErrors, "create_dir_for_excel_and_send_file_to_parser")
            pass
    else:
        try:
            fileparser.spreadURLsByContentType(redirectedTo, pageread, contentType, od, _encoding)
        except:
            comm.printException(comm.pathToSaveProgrammingErrors, "send_file_to_parser")
            pass
        
        
        