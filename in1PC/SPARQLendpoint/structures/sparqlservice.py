#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
# enable debugging
import cgitb
cgitb.enable()

import sys, json, codecs
from rdflib import Graph, Literal, URIRef
from pprint import pprint

''''''''''''''''''''''''

if sys.stdout.encoding is None or sys.stdout.encoding == 'ANSI_X3.4-1968':
    utf8_writer = codecs.getwriter('UTF-8')
    if sys.version_info.major < 3:
        sys.stdout = utf8_writer(sys.stdout, errors='replace')
    else:
        sys.stdout = utf8_writer(sys.stdout.buffer, errors='replace')

#print(u'\N{snowman}')
#print(u'\N{sun}')



''''''''''''''''''''''''

def getAnswer(tyyp, sparql):
    sparqlRes = g.query(sparql)
    display = sparqlRes.serialize(format=tyyp).decode('utf-8')
    #display = sparqlRes.serialize(format=tyyp).decode('latin-1')
    #display = sparqlRes.serialize(format=tyyp).decode(sys.stdout.encoding.lower())
    print(display)

''''''''''''''''''''''''

def validateParameters(data):
    typekey = 'format'
    sprqlkey = 'sparql'
    #print((typekey in data) & (sprqlkey in data))
    if((typekey in data) & (sprqlkey in data)):
        tyyp = str(data[typekey])
        sparql = str(data[sprqlkey])
        try:
            getAnswer(tyyp, sparql)
        except:
            e = sys.exc_info()[0]
            print('Get answer error: %s' % e )
            sys.exit(1)



''''''''''''''''''''''''
''''''''''''''''''''''''


try:
    data = json.loads(sys.argv[1])    
    #print(data)   
except: # catch *all* exceptions
    e = sys.exc_info()[0]
    print('Parameter load error: %s' % e )
    sys.exit(1)


g = Graph()
try:
    rdfDir = "../../../rdf_files/"
    filePath_loc = rdfDir + "LOC.rdf"
    filePath_org = rdfDir + "ORG.rdf"
    filePath_per = rdfDir + "PER.rdf"
    g.parse(filePath_loc)
    g.parse(filePath_org)
    g.parse(filePath_per)
except:
    e = sys.exc_info()[0]
    print('Parse error: %s' % e )
    sys.exit(1)


try:
    validateParameters(data)
except:
    e = sys.exc_info()[0]
    print('Data validation error: %s' % e )
    sys.exit(1)



