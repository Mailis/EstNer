INSTALLATION
===================
Installation for master instance is describein master folder. 
Installation for worker instance is describein worker folder.

DOCUMENTATION
===================
This system mainly does not use calsses. An only file where classes are used is init_rdf.py.
The files are called mainly sequentially.
The finer documentation is given in code comments of script-files.

##RDFizing process
The RDFizing process can be started from two startpoints:
__upload_logfile/index.php and__

__upadets/index.php__ (currently for demonstrating monthly updaes, user can push there button "Simulate" monhly updates)

The order of called files are as follows:


###MASTER instance
__commonVariables.py__
	>- stores variables of commonly used in many files: folder names, Google Compute Engine (gce) variable names for authentication and some frequently used methods
	
__upload_logfile/__

__index.php__

	>- user interface for uploading log files (up to 10MB),
	
	>- start RDFizing process when user pushes button next to logfile in table (1) by calling 
	
           __sendToAuth.py__
           
	>- delete uploaded files
	
	>- read statistics of processed logfiles
	
    
__sendToAuth.py__

	>- reads POST request from index.php and sends logfile name to auth.py
	
__auth.py__

	>- parses logfile, selects one of two URLs from log file row,
	
        >- validates URL by calling
        
	   __validationFuncs.py__
	   
        >- authenticates against gce  by using google-python-api-client (gpac) by calling 
        
           __authenticate_gce.py__
           
	>- gets list of worker instances,their IP-addresses and machine types by using gpac
	
        >- sends certain amount of URLs (the amount depends on amount of CPUs in given machine) to each worker by
        using
           __postToWorker.py__
           
	>- saves statistics of the time span of RDFizing in workers, number and type of workers, number of parsed
	log file rows and processed log file rows
	>- downloads open data documents, based on metadata that is saved in gce bucket, into 
	
           __datadownload/downloaded_files__
           
        >- saves statistics about time spent on downloading documents and number of downloads
        
	>- imports RDF files from worker instances to master instance by using list of worker IPs and calling
	
           __download_rdf_files.py__
           
        >- saves statistics about time spent on importing RDF files, how many triples are in every RDF-file
        
	>- imports Excel files from worker instaces by calling
	
           __importRemoteFiles.py__
           
        >- saves statistics about time spent on importing Excel files
        
	>- downloads json-objects (files where metadata are saved) from gce bucket into master-instance, into
	datadownload/datadownload_jsons  by using gpac and calling
           __downloadJsons.py__
           
	>- downloads error-objects (files where generated errors are saved) from gce bucket into master-instance 
	by using gpac and  calling
           __downloadJsons.py__
           
	>- saves catched errors into gce bucket of generated errors by using gpac
	
        >- sends deletion task for deleting RDF-files in worker instances by POSTing to each worker instance's
        
           #delete_rdf_files.php 
           


__------------------------------------------------------------__


__updates/index.php__

	>- receives post request and calls
	
	__upload_logfile/sendMonthlyUpdateTasks.py
	
__sendMonthlyUpdateTasks.py__

	>- reads json-files that are stored in 
	
	__datadownload/datadownload_jsons__
	
	>- gets file URLs and content hashes in json-files
	
	>- opens the document at the URL,makes hash of it content
	
	>- compares two hashes, if these are different, puts the file URL into the list of URL that will be sent
	to worker
        >- gets/uses list of worker instace using same python files as #auth.py
        
        >- sends certain size list of URLs to workres  using same python files as #auth.py
        
        >- sends POST request to workers' index.php
        
        >- saves number of changes, dataset downloads, saves time spent on processes of RDFizing, downloading
        datasets, json-objects and error-objects from gce buckets, downloading RDF files and excels from workers


###WORKER instance

__commonvariables.py__

	>- stores variables of commonly used in many files: folder names, Google Compute Engine (gce) variable
	names for authentication and some frequently used methods


__index.php__

	>- receives post request with list of URLs
	
	>- calls connector.py, passes list there
	
__connector.py__

	>- receives list of URLs from index.php
	
	>- creates pool of processes which size is equal to number of CPUs in its worker instance
	
	>- sends URLs for generating json-structured meta models of open documents to 
	
           __download_files_from_log.py__
           
__download_files_from_log.py__

        >- tries to read the open doc at given URL
        
	>- stores its metadata into dictionary-type object
	
	>- searches among existing json-files its URL's host name
	
        >- if it does not find, saves new json-object into gce storage bucket named as '<hostname>.json'
        
        >- if it finds, searches for the same document URL in found json-file
        
        >- if the file url is not found, saves new metadata of this new document into this existing json-file
        
	>- if the URL is found, it compares stored hash of content to the document's content just read in memory
	
        >- if the content hashes are different, it adds new content under doc's URL in json-object
        
        >- if the content hashes are the same, it continues to the nxt URL
        
        >- in every case when new data is captured, the respective part of json-object/file is updated and stored
        in gce storage bucket
	>- creates the mteta data structure for accessed document
	
	>- it writes metadata into directory type 
	
	>-  the document's URL and access-date is used in downloading processes 
	
	>-  and while monthly updating with documet's content-hash and filename-hash
	
	>-  doc's metadata is used in sorting/filtering through datasets: 
	
	>-  datasets can be filtered e.g by 
	
	>-  (part of) hostname
	
	>-  content type
	
	>-  accessed date, etc.
	
        >- after json-object is created/updated, it sends the content, encoding type and URL of the document to
        the 
	__fileparser.py__
	
__fileparser.py__

	>- forks document contents by their types, whish van be either
	
	>--- html
	
	>--- xml
	
	>--- pdf
	
	>--- excel
	
	>--- json
	
	>--- plain text
	


__read_html__

__read_xml__

__read_pdf__

__rea__eksel__

__read_json__

__read_plaintext__

	>- every type uses its own python library for parsing
	
	>- excel files can be parsed only after downloading, other types of docs are downloaded after RDFizing
	process (using json-files)
	>- these readers trys to find accurate encoding for every document
	
	>- replaces multiple spaces, new-lines and characters that cannot exist in names of locatios,
	organizations and people
	>- tries to split content into short sentences in order to fasten Estnltk's work (it extracts entities
	faster when shorter texts are fed)
	>- after parsing content, list of sentences are sent to 
	
	__getEntities.py__
	
__getEntities.py__

	>- uses Estnltk version 1.1 for extracting named entities.
	
	>- tries to improve labelling entities, by defining them if entity contains certain words like "maa"
	(refers to location) or "OÜ"(ref to company)
        >- also saves possible lemmas for including in triples, because a formed entity in estonian may have
        several lemmas hat denote differet things.
	>- collects extracted entities into lists (each for entity type, total of 3 lists). Lists are global
	variables for all processes in a worker. Lists have predefined size, defined in the variable #chunksize. Purpose of the lists are to find balance in memory usage (lists are saved into memory) and the number of how many
	times RDF-graphs are loaded from and written into __rdf_files/__.
The chunksize is hard-written by developer and is between 50-100.

	>- send lists to init_rdf.py
	
__init_rdf.py__

	>- uses python RDFlib which is developed for creaing and querying RDF graps. Among others, it has methods
	for defining URIs, namespaces, Literals, merging graphs, adding triples etc.
        >- includes classe for defining ontology data and adding triples.
        
	>- when __connector.py__is called, it first creates ontology, using class
	Ontologydata from this file.
	>- Manager classes are for adding triples into rdf-files named as ORG.rdf, LOC.rdf and PER.rdf.
	
	>- uses three types of entities-org, loc and per. 
	
	>- uses existing namespaces OWL, FOAF, RDF, DC, NERD and defines new namespace NER
	
	>- makes triple sfor classes nerd:Organization, nerd:Location, nerd:Person
	
	>- defines ontology datatype properties for ner namespace
	
        >- makes triples regarding in which web URL some entity was mentioned (ner:mentionedAtSite)
        
	>- makes triples for storing names (ner:orgNAme, ner:locationName, foaf:gname, foaf:fname, foaf:name)
	
	>- makes triples for storing alternatives (ner:lemma)
	
        >- stores rdf graph files into folder 
        
	__rdf_files/__
	

__storage/__
	>- in this folder are the python2 scripts, that enable to comminucate to gce data storage

__delete_rdf_files.php__
	>- after RDFizing process is finished, master instance sends post to ths file in every worker. Before that posting master instance had downloaded all RDF-files and downloaded excel-files from all worker instances.
	>- it empties the rdf_files folder as these files are no longer needed


##Graphical User Interfaces

###MASTER instance

User can use web app for starting RDFizing process, browsing in datasets, making SARQL queries, download
RDF-files, read catched errors.
User can also delete all generated file for starting to test this system from scratch.


__datasets/index.php__

__jq/datasets.jq__

	>- for smooth browsing/searcing in datasets
	
	>- uses json-files for filtering options
	
__rdf_files/__

	>- raw output of the three types of generated RDF files
	


__SPARQLendpoint/css/*__

__SPARQLendpoint/js/*__

__SPARQLendpoint/index.php__

__SPARQLendpoint/owlyQuery2.py__

	>- 4 different options for quering rdf-files.
	
	>- user can specify entity with/without web page for quering
	
	>- user can specify URL with/without entity  for quering
	
	>- user can write own query sentence
	
	>- user can test and see result of webservices
	

__SPARQLendpoint/structures/json__

__SPARQLendpoint/structures/xml__

	>- web services for machines that take in POST-request and answer either in a format of json or RDF/XML
	

__errors/index.php__

__css/__

__js/__

	>- meant for develoers, who want to see catched errors
	


__updates/index.php__

	>- user can push button and simulate monthly update
	






















