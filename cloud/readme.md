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

<i class="icon-file"></i>upload_logfile/index.php and 

<i class="icon-file"></i>upadets/index.php (currently for demonstrating monthly updaes, user can push there button "Simulate" monhly updates)

The order of called files are as follows:



###MASTER instance

<i class="icon-file"></i> commonVariables.py

		>- stores variables of commonly used in many files: folder names, Google Compute Engine (gce) variable names for authentication and some frequently used methods

<i class="icon-file"></i> upload_logfile/

<i class="icon-file"></i> index.php

		>- user interface for uploading log files (up to 10MB), 

		>- start RDFizing process when user pushes button next to logfile in table (1) by calling 

           <i class="icon-file"></i> sendToAuth.py

		>- delete uploaded files

		>- read statistics of processed logfiles

    

<i class="icon-file"></i> sendToAuth.py

		>- reads POST request from index.php and sends logfile name to auth.py

<i class="icon-file"></i> auth.py 

		>- parses logfile, selects one of two URLs from log file row,

        >- validates URL by calling

		   <i class="icon-file"></i> validationFuncs.py

        >- authenticates against gce  by using google-python-api-client (gpac) by calling 

           <i class="icon-file"></i> authenticate_gce.py

		>- gets list of worker instances,their IP-addresses and machine types by using gpac

        >- sends certain amount of URLs (the amount depends on amount of CPUs in given machine) to each worker by using

           <i class="icon-file"></i> postToWorker.py

		>- saves statistics of the time span of RDFizing in workers, number and type of workers, number of parsed log file rows and processed log file rows

		>- downloads open data documents, based on metadata that is saved in gce bucket, into 

           <i class="icon-file"></i> datadownload/downloaded_files

        >- saves statistics about time spent on downloading documents and number of downloads

		>- imports RDF files from worker instances to master instance by using list of worker IPs and calling

           <i class="icon-file"></i> download_rdf_files.py

        >- saves statistics about time spent on importing RDF files, how many triples are in every RDF-file

		>- imports Excel files from worker instaces by calling

           <i class="icon-file"></i> importRemoteFiles.py

        >- saves statistics about time spent on importing Excel files

		>- downloads json-objects (files where metadata are saved) from gce bucket into master-instance, into datadownload/datadownload_jsons  by using gpac and calling

           <i class="icon-file"></i> downloadJsons.py

		>- downloads error-objects (files where generated errors are saved) from gce bucket into master-instance  by using gpac and  calling

           <i class="icon-file"></i> downloadJsons.py

		>- saves catched errors into gce bucket of generated errors by using gpac

        >- sends deletion task for deleting RDF-files in worker instances by POSTing to each worker instance's

           #delete_rdf_files.php 



------------------------------------------------------------

------------------------------------------------------------



<i class="icon-file"></i> updates/index.php

		>- receives post request and calls

		<i class="icon-file"></i> upload_logfile/sendMonthlyUpdateTasks.py

<i class="icon-file"></i> sendMonthlyUpdateTasks.py

		>- reads json-files that are stored in 

		<i class="icon-file"></i> datadownload/datadownload_jsons

		>- gets file URLs and content hashes in json-files

		>- opens the document at the URL,makes hash of it content

		>- compares two hashes, if these are different, puts the file URL into the list of URL that will be sent to worker

        >- gets/uses list of worker instace using same python files as #auth.py

        >- sends certain size list of URLs to workres  using same python files as #auth.py

        >- sends POST request to workers' index.php

        >- saves number of changes, dataset downloads, saves time spent on processes of RDFizing, downloading datasets, json-objects and error-objects from gce buckets, downloading RDF files and excels from workers



###WORKER instance

<i class="icon-file"></i> commonvariables.py

		>- stores variables of commonly used in many files: folder names, Google Compute Engine (gce) variable names for authentication and some frequently used methods



<i class="icon-file"></i> index.php

		>- receives post request with list of URLs

		>- calls connector.py, passes list there

<i class="icon-file"></i> connector.py

		>- receives list of URLs from index.php

		>- creates pool of processes which size is equal to number of CPUs in its worker instance

		>- sends URLs for generating json-structured meta models of open documents to 

           <i class="icon-file"></i> download_files_from_log.py

<i class="icon-file"></i> download_files_from_log.py

        >- tries to read the open doc at given URL

		>- stores its metadata into dictionary-type object

		>- searches among existing json-files its URL's host name

        >- if it does not find, saves new json-object into gce storage bucket named as '<hostname>.json'

        >- if it finds, searches for the same document URL in found json-file

        >- if the file url is not found, saves new metadata of this new document into this existing json-file

		>- if the URL is found, it compares stored hash of content to the document's content just read in memory

        >- if the content hashes are different, it adds new content under doc's URL in json-object

        >- if the content hashes are the same, it continues to the nxt URL

        >- in every case when new data is captured, the respective part of json-object/file is updated and stored in gce storage bucket

		>- creates the mteta data structure for accessed document

		>- it writes metadata into directory type 

		>-  the document's URL and access-date is used in downloading processes 

		>-  and while monthly updating with documet's content-hash and filename-hash

		>-  doc's metadata is used in sorting/filtering through datasets: 

		>-  datasets can be filtered e.g by 

		>-  (part of) hostname

		>-  content type

		>-  accessed date, etc.

        >- after json-object is created/updated, it sends the content, encoding type and URL of the document to the 

		<i class="icon-file"></i> fileparser.py

<i class="icon-file"></i> fileparser.py

		>- forks document contents by their types, whish van be either

		>--- html

		>--- xml

		>--- pdf

		>--- excel

		>--- json

		>--- plain text



<i class="icon-file"></i> read__html

<i class="icon-file"></i> read__xml

<i class="icon-file"></i> read__pdf

<i class="icon-file"></i> read__eksel

<i class="icon-file"></i> read__json

<i class="icon-file"></i> read__plaintext

		>- every type uses its own python library for parsing

		>- excel files can be parsed only after downloading, other types of docs are downloaded after RDFizing process (using json-files)

		>- these readers trys to find accurate encoding for every document

		>- replaces multiple spaces, new-lines and characters that cannot exist in names of locatios, organizations and people

		>- tries to split content into short sentences in order to fasten Estnltk's work (it extracts entities faster when shorter texts are fed)

		>- after parsing content, list of sentences are sent to 

		<i class="icon-file"></i> getEntities.py

<i class="icon-file"></i> getEntities.py

		>- uses Estnltk version 1.1 for extracting named entities.

		>- tries to improve labelling entities, by defining them if entity contains certain words like "maa" (refers to location) or "OÜ"(ref to company)

        >- also saves possible lemmas for including in triples, because a formed entity in estonian may have several lemmas hat denote differet things.

		>- collects extracted entities into lists (each for entity type, total of 3 lists). Lists are global variables for all processes in a worker. Lists have predefined size, defined in the variable #chunksize. Purpose of the lists are to find balance in memory usage (lists are saved into memory) and the number of how many times RDF-graphs are loaded from and written into <i class="icon-file"></i> .rdf-files.

The chunksize is hard-written by developer and is between 50-100.

		>- send lists to init_rdf.py

<i class="icon-file"></i> init_rdf.py

		>- uses python RDFlib which is developed for creaing and querying RDF graps. Among others, it has methods for defining URIs, namespaces, Literals, merging graphs, adding triples etc.

        >- includes classe for defining ontology data and adding triples.

		>- when <i class="icon-file"></i> connector.py is called, it first creates ontology, using class Ontologydata from this file.

		>- Manager classes are for adding triples into rdf-files named as ORG.rdf, LOC.rdf and PER.rdf.

		>- uses three types of entities-org, loc and per. 

		>- uses existing namespaces OWL, FOAF, RDF, DC, NERD and defines new namespace NER

		>- makes triple sfor classes nerd:Organization, nerd:Location, nerd:Person

		>- defines ontology datatype properties for ner namespace

        >- makes triples regarding in which web URL some entity was mentioned (ner:mentionedAtSite)

		>- makes triples for storing names (ner:orgNAme, ner:locationName, foaf:gname, foaf:fname, foaf:name)

		>- makes triples for storing alternatives (ner:lemma)

        >- stores rdf graph files into folder 

		<i class="icon-file"></i> rdf_files/



<i class="icon-file"></i> storage/

		>- in this folder are the python2 scripts, that enable to comminucate to gce data storage



<i class="icon-file"></i> delete_rdf_files.php

		>- after RDFizing process is finished, master instance sends post to ths file in every worker. Before that posting master instance had downloaded all RDF-files and downloaded excel-files from all worker instances.

		>- it empties the rdf_files folder as these files are no longer needed





##Graphical User Interfaces



###MASTER instance

User can use web app for starting RDFizing process, browsing in datasets, making SARQL queries, download RDF-files, read catched errors.

User can also delete all generated file for starting to test this system from scratch.



<i class="icon-file"></i> datasets/index.php

<i class="icon-file"></i> jq/datasets.jq

		>- for smooth browsing/searcing in datasets

		>- uses json-files for filtering options

<i class="icon-file"></i> rdf_files

		>- raw output of the three types of generated RDF files



<i class="icon-file"></i> SPARQLendpoint/css/*

<i class="icon-file"></i> SPARQLendpoint/js/*

<i class="icon-file"></i> SPARQLendpoint/index.php

<i class="icon-file"></i> SPARQLendpoint/owlyQuery2.py

		>- 4 different options for quering rdf-files.

		>- user can specify entity with/without web page for quering

		>- user can specify URL with/without entity  for quering

		>- user can write own query sentence

		>- user can test and see result of webservices



<i class="icon-file"></i> SPARQLendpoint/structures/json

<i class="icon-file"></i> SPARQLendpoint/structures/xml

		>- web services for machines that take in POST-request and answer either in a format of json or RDF/XML



<i class="icon-file"></i> errors/index.php

<i class="icon-file"></i> css/

<i class="icon-file"></i> js/

		>- meant for develoers, who want to see catched errors





<i class="icon-file"></i> updates/index.php

		>- user can push button and simulate monthly update










































