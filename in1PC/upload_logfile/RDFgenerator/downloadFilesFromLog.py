#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 25, 2015
http://kaira.sgo.fi/2014/05/saving-and-loading-data-in-python-with.html?showComment=1424895576114#c1010617980067477531
'''
import os.path, sys
import json, time
import hashlib
from urllib import request as ur
from urllib.parse import urlparse
from urllib import error as urr

import fileparser
import commonVariables as comm

comm.timeDir = time.strftime("%d_%m_%Y")

'''

'''    
def saveJsonToFile(saveToPath, dictnry):
    out_file = open(saveToPath, "w")
    # Save the dictionary into this file
    # (the 'indent=4' is optional, but makes it more readable)
    json.dump(dictnry, out_file, indent=4)
    # Close the file
    out_file.close()

def insertNewContentToDict(localFilename, page_redirected, page_info, page_sha254, page_status):
    try:
        newDict = dict()
        newDict[page_sha254] = page_info
        newDict[page_sha254]["localFilename"] = localFilename
        newDict[page_sha254]["file_url"] = page_redirected
        newDict[page_sha254]["sha224"] = page_sha254
        newDict[page_sha254]["status"] = page_status
        newDict[page_sha254]["timeDir"] = comm.timeDir
        return newDict
    except:
        comm.printException(comm.pathToSaveJsonErrors)
        pass
    
def insertNewSubFileToDict(localFilename, page_redirected, page_info, page_sha254, page_status):
    try:
        newDict = dict()
        newDict[localFilename] = dict()
        newDict[localFilename][page_sha254] = page_info
        newDict[localFilename][page_sha254]["localFilename"] = localFilename
        newDict[localFilename][page_sha254]["file_url"] = page_redirected
        newDict[localFilename][page_sha254]["sha224"] = page_sha254
        newDict[localFilename][page_sha254]["status"] = page_status
        newDict[localFilename][page_sha254]["timeDir"] = comm.timeDir
        return newDict
    except:
        comm.printException(comm.pathToSaveJsonErrors)
        pass

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
        comm.printException(comm.pathToSaveJsonErrors)
        pass
                
def saveMetadata(url, od):
    if not os.path.isdir(comm.jsonsDir):
        os.makedirs(comm.jsonsDir)
        
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
        #base_url becomes also jsonFile name (pathToSaveMetadata)
        baseUrl = (urlparse(url)).netloc
        sha224_ = (hashlib.sha224(pageread).hexdigest())
        _encoding = None
        #print("-----------------------------------------------------")
        #print("url ", redirectedTo)
        #print("contentType ", contentType.lower())
        if("charset" in contentType.lower()):
            #print("charset_ENCODING ", _encoding)
            encodSplit = (contentType.lower().strip()).split("=")
            encodIndex = len(encodSplit)-1
            if(len(encodSplit) > encodIndex):
                _encoding = encodSplit[encodIndex]
        #print("ENCODING ", _encoding)
        pathToSaveMetadata = comm.jsonsDir + baseUrl + ".json"
        isDesiredType = comm.isDesiredContent(contentType, od)
        #print("isDesiredType ", isDesiredType)#
        
        if(isDesiredType):
            #if this file does not exist yet in locale storage, create
            #if this base-url path does not exist:
            if not os.path.isfile(pathToSaveMetadata):
                #print("excel in contentType ", ("excel" in contentType))#
                #create directory for the downloads from this base_url and save file into it
                #downloadedFilePath = downLoadFile(pageread, localFilename, baseUrl)
                #print("downloadedFilePath ", downloadedFilePath)
                #if(downloadedFilePath):
                    #print()#
                infoDict_tmp = dict()
                infoDict_tmp["base_url"] = baseUrl
                infoDict = insertValuesToDict(infoDict_tmp, localFilename, redirectedTo, pageInfo, sha224_, statusCode )
                saveJsonToFile(pathToSaveMetadata, infoDict)
                #after downloading send the file to estner:
                if("excel" in contentType):
                    try:
                        dirToSaveDownloads = comm.downloadsDir + baseUrl
                        if not os.path.isdir(dirToSaveDownloads):
                            os.makedirs(dirToSaveDownloads)
                        fileparser.spreadURLsByContentType(redirectedTo, None, contentType, od, _encoding, filePath = (dirToSaveDownloads + "/" + localFilename))
                    except:
                        comm.printException(comm.pathToSaveProgrammingErrors, "create_dir_for_excel")
                        pass
                else:
                    fileparser.spreadURLsByContentType(redirectedTo, pageread, contentType, od, _encoding)
                    pass
            #if this file does exist already, upload new version
            else:
                #print("ELSE excel in contentType ", ("excel" in contentType))#
                someNewData = False
                # Open the json file (<baseUrl>.json) for reading
                # and comparing sha224 values of sha saved in json and in opened file
                in_file = open(pathToSaveMetadata, "r")
                # Load the contents from the file, which creates a new dictionary
                existingFileDict = json.load(in_file)
                # Close the file... we don't need it anymore  
                in_file.close()
                #(url): e.g. http://www.temtec.ee/top.html
                #(existingFileDict_tmp['base_url']) e.g. www.temtec.ee
                if(existingFileDict['base_url'] in url):#same file resource was requested
                    #print("BASE URL ", existingFileDict['base_url'])
                    #dict has two 1-level keys: 'base_url' and sha244 of a file name
                    fNameKey = [k for k in existingFileDict.keys() if k != 'base_url']
                    #print("  fNameKey", fNameKey)
                    #print("  localFilename", localFilename)
                    #print("  localFilename in fNameKey", (localFilename in fNameKey))
                    #this list may contain 'localFilename'
                    if (localFilename in fNameKey):
                        #if earlier saved file's sha does not equal to current sha, 
                        #the contents of file has changed.
                        #Saved file's sha is saved into key, find it or not:
                        shaKeys = existingFileDict[localFilename].keys()
                        if(sha224_ not in shaKeys):#file has changed
                            #search for date, if it same, update existing sha key
                            replaceSha = ""
                            #if there is same timedDir under some sha key, get this sha and replace
                            for sk in shaKeys:
                                savedDate = existingFileDict[localFilename][sk]["timeDir"]
                                if(savedDate == comm.timeDir):
                                    replaceSha = sk
                                    break
                            if(replaceSha != ""):#delete sha, because of same day date
                                del existingFileDict[localFilename][replaceSha]
                                #print("REPLACING!")
                            #add new value with new content_sha-key under filename_sha-key
                            #filename-url is same, but content is changed
                            #so add new content-sha
                            newDataDict = insertNewContentToDict(localFilename, redirectedTo, pageInfo, sha224_, statusCode)
                            if(newDataDict):
                                existingFileDict[localFilename].update(newDataDict)
                                someNewData = True
                            
                    else:#new file (resource) from same domain (or 'base_url') requested
                        #add new value with new filename_sha-key for that base-resource
                        newDataDict = insertNewSubFileToDict(localFilename, redirectedTo, pageInfo, sha224_, statusCode)
                        if(newDataDict):
                            existingFileDict.update(newDataDict)
                            someNewData = True
                if someNewData:
                    #download also
                    #succ = downLoadFile(pageread, localFilename, baseUrl)
                    #if(succ):#... save metadata for downloaded file
                    saveJsonToFile(pathToSaveMetadata, existingFileDict)
                    #after downloading send the file to estner: 
                    if("excel" in contentType):
                        try:
                            dirToSaveDownloads = comm.downloadsDir + baseUrl
                            if not os.path.isdir(dirToSaveDownloads):
                                os.makedirs(dirToSaveDownloads)
                            fileparser.spreadURLsByContentType(redirectedTo, None, contentType, od, _encoding, filePath = (dirToSaveDownloads + "/" + localFilename))
                        except:
                            comm.printException(comm.pathToSaveProgrammingErrors, "create_dir_for_excel")
                            pass
                    else:
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

