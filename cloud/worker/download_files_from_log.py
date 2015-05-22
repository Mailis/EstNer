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
from urllib import request as ur
from urllib.parse import urlparse
from urllib import error as urr
import subprocess

import fileparser
import commonvariables as comm
 

comm.timeDir = time.strftime("%d_%m_%Y")

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




               
def saveMetadata(url, od):
    try:
        page = ur.urlopen(url)
        statusCode = page.getcode()
        redirectedTo = page.geturl()
        pageread = page.read()
        pageInfo = dict(page.info())
        page.close()
        localFilename = comm.getUrlSHA(redirectedTo)
        contentType = comm.getContentType(pageInfo)
        #print(url)
        #print(contentType)
        baseUrl = (urlparse(url)).netloc
        sha224_ = (hashlib.sha224(pageread).hexdigest())
        _encoding = ""
        #print("-----------------------------------------------------")
        #print("url ", redirectedTo)
        #print("contentType ", contentType.lower())
        if("charset" in contentType.lower()):
            #print("charset_ENCODING ", _encoding)
            encodSplit = (contentType.lower().strip()).split("=")
            encodIndex = len(encodSplit)-1
            if(len(encodSplit) > encodIndex):
                _encoding = encodSplit[encodIndex]
        #print("isDesiredType ", isDesiredType)#
        
        isDesiredType = comm.isDesiredContent(contentType, od)
        if(isDesiredType):
            jsonsDir = comm.jsonsDir
            jsonsFile = baseUrl + ".json"
            jsonsPath = dict()
            jsonsPath["object"] = jsonsFile#'test14.txt'#
            jsonsPath["bucket"] = jsonsDir#'statistika'#
            pathToSaveMetadata_ = json.dumps(jsonsPath)
            #if this file does not exist yet in locale storage, create
            #if this base-url path does not exist:
            infoDict_tmp = dict()
            infoDict_tmp["base_url"] = baseUrl
            infoDict = insertValuesToDict(infoDict_tmp, localFilename, redirectedTo, pageInfo, sha224_, statusCode )
            jsondata = json.dumps(infoDict, indent=4)
            insertJson = dict()
            insertJson["jsondata"] = jsondata
            insertJson["url"] = url
            insertJson["localFilename"] = localFilename
            insertJson["timeDir"] = comm.timeDir
            insertJson["redirectedTo"] = redirectedTo
            insertJson["pageInfo"] = pageInfo
            insertJson["sha224_"] = sha224_
            insertJson["statusCode"] = statusCode
            insertJson["address"] = pathToSaveMetadata_

            someNewData = False
            errr=""
            try:#save json-metadata 
                #get info back about whether is here some new data
                #os.system('python2 storage/updateObj.py ' + json.dumps(json.dumps(insertJson)))
                jd = json.dumps(insertJson)
                p = subprocess.Popen(["python2", "storage/updateObj.py", jd], stdout=subprocess.PIPE)
                out, err = p.communicate()
                someNewData  = out.decode()
                errr = str(err).lower()
            except:
                errstr = errr if ((errr != "") & (errr != "none")) else "storage-updateObj.py-ERROR"
                comm.printException(comm.pathToSaveJsonErrors, errstr)
                pass

            if someNewData:
                #print("prindib yltse?")
                #-download also
                #-succ = downLoadFile(pageread, localFilename, baseUrl)
                #-after downloading send the file to estner: 
                if("excel" in contentType):
                    try:
                        dirToSaveDownloads = comm.downloadsDir + baseUrl
                        if not os.path.isdir(dirToSaveDownloads):
                            os.makedirs(dirToSaveDownloads)
                        #go on to next steps:
                        fileparser.spreadURLsByContentType(redirectedTo, None, contentType, od, _encoding, filePath = (dirToSaveDownloads + "/" + localFilename))
                    except:
                        comm.printException(comm.pathToSaveProgrammingErrors, "mkdir_and_download_excel")
                        pass
                else:
                    #go on to next steps:
                    fileparser.spreadURLsByContentType(redirectedTo, pageread, contentType, od, _encoding)
    #save errors                    
    except urr.HTTPError as e:
        errStr = (url + " HTTPError " + str(e.code) + " " + str(e.reason) + " \n" )
        comm.printException(comm.pathToSaveJsonErrors, errStr)
        pass
    except urr.URLError as e:
        errStr = (url + " URLError " + str(e.reason) + " \n" )
        comm.printException(comm.pathToSaveJsonErrors, errStr)
        pass
    except IOError as e:
        errStr = (url + " " + str("I/O_erRror({0}):_{1}".format(e.errno, e.strerror)) + "\n")
        comm.printException(comm.pathToSaveJsonErrors, errStr)
        pass
    except ValueError:
        errStr = (url + " ValueError_Could_not_convert_data_to_an_integer.\n") 
        comm.printException(comm.pathToSaveJsonErrors, errStr)
        pass
    except TypeError:
        errStr = (url + " TypeError\n")  
        comm.printException(comm.pathToSaveJsonErrors, errStr)
        pass
    except:
        errStr = (url + " Unexpected_error:_" + (str(sys.exc_info()[0])) + "\n")
        comm.printException(comm.pathToSaveJsonErrors, errStr)
        pass




