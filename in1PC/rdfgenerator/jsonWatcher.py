'''
Created on Mar 12, 2015
http://brunorocha.org/python/watching-a-directory-for-file-changes-with-python.html
'''
#import sys
import os
import logging
import time
import json
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler#LoggingEventHandler
from urllib.request import urlretrieve as urr
import commonVariables as comm

 

class DownloadsHandler(PatternMatchingEventHandler):
    patterns = ["*.json"]
    downloadsDir = comm.downloadsDir
    def process(self, event):
        """
        event.event_type 
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """
        # the file will be processed there
        filePath = event.src_path
        #open json file
        jsonToDict = json.load(open(filePath));
        base_url = jsonToDict['base_url']#becomes folderName
        for fname_key in jsonToDict.keys():
            if (fname_key != 'base_url'):#fname_key(sha of file url) becomes local filename
                for csha in jsonToDict[fname_key].keys():
                    #excel type is already downloaded
                    if("excel" not in jsonToDict[fname_key][csha]['Content-Type']):
                        file_url = jsonToDict[fname_key][csha]['file_url']
                        timeDir = jsonToDict[fname_key][csha]['timeDir']
                        dirPath = self.downloadsDir + base_url + "/"
                        try:
                            #create dir if does not exist
                            if not os.path.isdir(dirPath):
                                os.makedirs(dirPath)
                            try:
                                urr(file_url, dirPath + fname_key)
                                #print(timeDir, base_url, , file_url)
                            except:
                                comm.printException(comm.pathToSaveDownloadErrors, filePath)
                                pass
                        except:
                            comm.printException(comm.pathToSaveDownloadErrors, filePath)
                            pass
        #print (filePath, event.event_type)  # print now only for debug

    def on_modified(self, event):
        self.process(event)

    def on_created(self, event):
        self.process(event)
        
        
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    #sys.argv[1] if len(sys.argv) > 1 else '.'
    jsonsDirPath = comm.jsonsDir
    event_handler = DownloadsHandler()
    
    observer = Observer()
    observer.schedule(event_handler, jsonsDirPath, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    
    
    
    
