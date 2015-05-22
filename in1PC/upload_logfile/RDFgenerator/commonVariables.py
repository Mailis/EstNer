import os.path, os
import time, collections
import hashlib
import linecache
import sys, stat
import codecs

if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')


chunksize=100

'''
    Lists file types, where one cannot find entities
'''
desiredFileTypes = ['excel', 'json', 'html', 'xml', 'pdf', 'plain', 'text']#
undesiredFileTypes = ['image', 'no-type', 'javascript', 'flash', 'dns']
undesiredFileExtensions = ['jpg', 'jpeg', 'gif', 'png', 'bmp', 'ico', 'swf', 'js', 'css', 'js', 'css', 'ShockwaveFlash', 'dns']
undesiredFileName = ['robots.txt', '/robots.txt']

'''
    Directories and paths so save errors and statistics etc.
'''
timeDir = time.strftime("%d_%m_%Y")
#some target paths for saving
'''
stat.S_ISUID: Set user ID on execution.
stat.S_ISGID: Set group ID on execution.
stat.S_ENFMT: Record locking enforced.
stat.S_ISVTX: Save text image after execution.
stat.S_IREAD: Read by owner.
stat.S_IWRITE: Write by owner.
stat.S_IEXEC: Execute by owner.
stat.S_IRWXU: Read, write, and execute by owner.
stat.S_IRUSR: Read by owner.
stat.S_IWUSR: Write by owner.
stat.S_IXUSR: Execute by owner.
stat.S_IRWXG: Read, write, and execute by group.
stat.S_IRGRP: Read by group.
stat.S_IWGRP: Write by group.
stat.S_IXGRP: Execute by group.
stat.S_IRWXO: Read, write, and execute by others.
stat.S_IROTH: Read by others.
stat.S_IWOTH: Write by others.
stat.S_IXOTH: Execute by others.
'''
downloadsDir = "../../datadownload/downloaded_files/"+timeDir+"/"
jsonsDir = "../../datadownload/jsons/"
pathToSaveJsonErrors = jsonsDir + "errors.txt"

pathToRDFdir = "../../rdf_files/"


dirToSaveProgrammingErrors = "../generated_files/programming_errors/"
pathToSaveProgrammingErrors = dirToSaveProgrammingErrors + timeDir + ".txt"

dirToSaveDownloadErrors = "../generated_files/download_errors/"
pathToSaveDownloadErrors = dirToSaveDownloadErrors + timeDir + ".txt"

pathToUpdateErrorsDir = "../generated_files/update_errors/"
updateErrorsFilePath = pathToUpdateErrorsDir + timeDir + ".txt"

pathToInitRdfErrorsDir = "../generated_files/tripling_errors/"
initRdfErrorsFilePath = pathToInitRdfErrorsDir + timeDir + ".txt"

parsing_errorsDir = "../generated_files/parsing_errors/"
pathToSaveParsingErrors = parsing_errorsDir + timeDir + ".txt"

if not os.path.isdir(pathToRDFdir):
    os.makedirs(pathToRDFdir)   
if not os.path.isdir(downloadsDir):
    os.makedirs(downloadsDir)
if not os.path.isdir(jsonsDir):
    os.makedirs(jsonsDir)
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
'''
os.chmod(pathToRDFdir, stat.S_IROTH)
os.chmod(downloadsDir, stat.S_IROTH)
os.chmod(jsonsDir, stat.S_IROTH)
os.chmod(pathToSaveJsonErrors, stat.S_IROTH)
os.chmod(pathToSaveParsingErrors, stat.S_IROTH)
os.chmod(initRdfErrorsFilePath, stat.S_IROTH)
os.chmod(updateErrorsFilePath, stat.S_IROTH)
os.chmod(pathToSaveDownloadErrors, stat.S_IROTH)
os.chmod(pathToSaveProgrammingErrors, stat.S_IROTH)
'''       
        
def getContentType(pageInfo):
    contentType = ""
    #there are literally different keys for content type:
    if("Content-Type" in pageInfo.keys()):
        contentType = pageInfo["Content-Type"]
    elif("Content-type" in pageInfo.keys()):
        contentType = pageInfo["Content-type"]
    elif("content-type" in pageInfo.keys()):
        contentType = pageInfo["content-type"]
    elif("content-Type" in pageInfo.keys()):
        contentType = pageInfo["content-Type"]
    elif("contentType" in pageInfo.keys()):
        contentType = pageInfo["contentType"]
    elif("contenttype" in pageInfo.keys()):
        contentType = pageInfo["contenttype"]
    elif("Contenttype" in pageInfo.keys()):
        contentType = pageInfo["Contenttype"]
    elif("Content type" in pageInfo.keys()):
        contentType = pageInfo["Content type"]
    elif("Content Type" in pageInfo.keys()):
        contentType = pageInfo["Content Type"]
    return contentType


def isDesiredContent(cType, od):
    isDesired = True
    isKnownType = False
    for ct in desiredFileTypes:
        if (ct in cType):
            isKnownType = True
            break
    
    if(not isKnownType):
        for ct in (undesiredFileTypes + undesiredFileExtensions):
            if (ct in cType):
                isDesired = False
                break
    return isDesired



def getUrlSHA(redirectedTo):
    return hashlib.sha224(redirectedTo.encode("utf-8")).hexdigest()


def exceptionRecorder(self, pathToErrorFile, pathToGivenFile, webpage, e, addInfoStr=""):
    errString =time.strftime("%d/%m/%Y_%H:%M:%S") + " " + pathToGivenFile + " " + webpage + " " + addInfoStr.replace(" ", "_") + str(sys.exc_info()[0]) + "\n"
    if isinstance(e, collections.Iterable):
        for elem in e:
            errString += str(elem).replace(" ", "_")  + "_"
    
    jf = open(pathToErrorFile, 'a', encoding='utf-8')
    jf.write(time.strftime(errString + str(sys.exc_info()[0]) + "\n"))
    jf.close()

    
def printException(pathToErrorFile, errString=""):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    err= (errString + ' {}_EXCEPTION_IN_({},_LINE_{}_"{}"):_{}_'.format(exc_type, filename, lineno, line.strip(), exc_obj) + "\n")  
    jf = open(pathToErrorFile, 'a', encoding='utf-8')
    jf.write(err)#
    jf.close()    
    

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
       
def replaceToPunkts(s6ne):
    sentences = set()
    prune1 = s6ne.strip().replace('\n', ' ').replace('\t', ' ').replace('&nbsp;', ' ')
    multiSpaces="\s{2,}"
    prune2 = re.sub(multiSpaces, ' ', prune1)
    prune3 = prune2.replace(';', '.').replace(':', '.').replace('(', '.').replace(')', '.').replace('?', '.').replace('!', '.').replace(',', '.').replace(' | ', '.').replace('|', '.').replace('/', '.').replace('\\', '.').replace('{', '.').replace('}', '.').replace('[', '.').replace(']', '.').replace('¬', '.').replace('_', '.').replace('~', '.').replace('#', '.').replace('%', '.').replace('`', '.').replace('"', '.').replace('<', '.').replace('>', '.').replace('=', '.').replace('+', '.')
    laused = prune3.split(".")
    for s6n in laused:
        s6ne = s6n.encode("ascii","replace")
        if(len(s6ne) > 2) & (not is_number(s6ne)):
            sentences.add(s6ne)
    return list(sentences)    
    
    
    
    
