#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 19, 2015

@author: mailis
'''
import os, stat
from rdflib import URIRef, Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, DC, FOAF
from multiprocessing import Manager
import commonVariables as comm

class OntologyData():
    
    '''
        Defines common variables for using them in inherited classes
    '''
    
    locationGraph = Graph() 
    organizatioGraph = Graph() 
    peopleGraph = Graph()
    
    datatypeProperty = OWL["DatatypeProperty"]
    owlClass = OWL["Class"]
    owlOntology = OWL["Ontology"]
    perName = FOAF["name"]
    givenName = FOAF["givenName"]
    familyName = FOAF["familyName"]
    #an existing ontology for extracted named entities
    nerd = Namespace("http://nerd.eurecom.fr/ontology#")
    #description about new (this) ontology:
    ner = Namespace("http://www.estner.ee/estnerd#")
    #construct namespace strings for objects' namespaces
    locStr = "http://nerd.eurecom.fr/ontology#"
    orgStr = "http://nerd.eurecom.fr/ontology#"
    perStr = "http://nerd.eurecom.fr/ontology#"
    #description 'about resource':
    location = nerd.Location
    organization = nerd.Organization
    person = nerd.Person
    
    
    #description of datatype property for lemmas:
    lemma = ner.lemma#==URIRef("http://www.estner.ee/estnerd#lemma")
    #description of datatype property mentionedAtSite:
    mentionedAtSite = ner.mentionedAtSite#==URIRef("http://www.estner.ee/estnerd#mentionedAtSite")
    #description of datatype property orgName:
    orgName = ner.orgName#==URIRef("http://www.estner.ee/estnerd#orgName")
    #description of datatype property locationNames:
    locationName = ner.locationName#==URIRef("http://www.estner.ee/estnerd#locationName")
    
    LOC_TYPE = "LOC"
    ORG_TYPE = "ORG"
    PER_TYPE = "PER"
   
    m = Manager()
    #chunk lists
    sharedList_per = m.list()
    sharedList_org = m.list()
    sharedList_loc = m.list()
    
    def __init__(self, namespaceURI = 'http://nerd.eurecom.fr/ontology'):
        self.locRdf = comm.pathToRDFdir + self.LOC_TYPE + ".rdf"
        self.orgRdf = comm.pathToRDFdir + self.ORG_TYPE + ".rdf"
        self.perRdf = comm.pathToRDFdir + self.PER_TYPE + ".rdf"
        #os.chmod(self.locRdf, stat.S_IROTH)
        #os.chmod(self.orgRdf, stat.S_IROTH)
        #os.chmod(self.perRdf, stat.S_IROTH)
        
    def getLocRdfGraph(self):
        g = Graph()
        return g.parse(self.locRdf)
        
    def getOrgRdfGraph(self):
        g = Graph()
        return g.parse(self.orgRdf)
        
    def getPerRdfGraph(self):
        g = Graph()
        return g.parse(self.perRdf)
    def bindNamespaces(self, g):
        g.bind("nerd", self.nerd)
        g.bind("ner", self.ner)
        g.bind("rdf", RDF)
        g.bind("owl", OWL)
        g.bind("dc", DC)
        g.bind("foaf", FOAF)
        

           
           
class LocationManager (OntologyData): 
    def __init__(self, od):
        OntologyData.__init__(self)
        
    def addTriples(self, chunkedList, addLemmas = True):
        try:
            newDataExists = False
            g = self.getLocRdfGraph()
            g_new = Graph()
            #define specific namespace prefix
            self.bindNamespaces(g)
            
            for andmed in chunkedList:
                for webpage in andmed:
                    for objName in andmed[webpage]:
                        lemmaList = andmed[webpage][objName]
                        #print (lemmaList)
                        try:
                            #make triples
                            newLocation = URIRef(self.locStr + objName.replace (">", "").replace ("<", "").replace ("|", "").replace (" ", "_").lower())
                            newLocationName = Literal(objName)
                            newWebpage = URIRef(webpage);
                            
                            #add triples
                            #check if graph contains bob already
                            if ( newLocation, RDF.type, URIRef(self.location)) not in g:
                                newDataExists = True
                                g_new .add( (newLocation, RDF.type, URIRef(self.location)) )
                                g_new .add( (newLocation, self.locationName, newLocationName) )
                             
                            #g_new .add( (newLocation, od.mentionedAtSite, newWebpage) )   
                            #check if graph contains bob already
                            if ( newLocation, self.mentionedAtSite, newWebpage) not in g:
                                newDataExists = True
                                g_new .add( (newLocation, self.mentionedAtSite, newWebpage) )
                            #add lemmas also
                            if(addLemmas):
                                for newLemma in lemmaList:
                                    #check if graph contains bob already
                                    if ( newLocation, self.lemma, Literal(newLemma)) not in g:
                                        newDataExists = True
                                        g_new .add( (newLocation, self.lemma, Literal(newLemma)) )
                        except:
                            comm.printException(comm.initRdfErrorsFilePath, "build_loc_graph")
                            pass
            #write rdf into file
            if (newDataExists):
                try:
                    gg = g+g_new
                    (gg).serialize(self.locRdf, format='pretty-xml', encoding='utf-8')
                except:
                    comm.printException(comm.initRdfErrorsFilePath, "RDF Location Manager serialization error: ")
                    pass
        except:
            comm.printException(comm.initRdfErrorsFilePath, "RDF Location Manager (addTriples) error: ")
            pass
            
            

class OrganizationManager (OntologyData): 
    def __init__(self, od):
        OntologyData.__init__(self)
        
    def addTriples(self, chunkedList, addLemmas = True):
        try:
            newDataExists = False
            g = self.getOrgRdfGraph()
            g_new = Graph()
            #define specific namespace prefix
            self.bindNamespaces(g)
            
            for andmed in chunkedList:
                for webpage in andmed:
                    #print(webpage)
                    for objName in andmed[webpage]:
                        lemmaList = andmed[webpage][objName]
                        #print (lemmaList)
                        try:
                            #make triples
                            newOrg = URIRef(self.orgStr + objName.replace (">", "").replace ("<", "").replace ("|", "").replace (" ", "_").lower())
                            newOrgName = Literal(objName)
                            newWebpage = URIRef(webpage);
                            #add triples
                            #check if graph contains bob already
                            if ( newOrg, RDF.type, URIRef(self.organization)) not in g:
                                newDataExists = True
                                g_new .add( (newOrg, RDF.type, URIRef(self.organization)) )
                                g_new .add( (newOrg, self.orgName, newOrgName) )
              
                            #check if graph contains bob already
                            if ( newOrg, self.mentionedAtSite, newWebpage) not in g:
                                newDataExists = True
                                g_new .add( (newOrg, self.mentionedAtSite, newWebpage) )
                            #add lemmas also
                            if(addLemmas):
                                for newLemma in lemmaList:
                                    #check if graph contains bob already
                                    if ( newOrg, self.lemma, Literal(newLemma)) not in g:
                                        newDataExists = True
                                        g_new .add( (newOrg, self.lemma, Literal(newLemma)) )
                        except:
                            comm.printException(comm.initRdfErrorsFilePath, "build_org_graph")
                            pass
            #write rdf into file
            if (newDataExists):
                try:
                    gg = g+g_new
                    (gg).serialize(self.orgRdf, format='pretty-xml', encoding='utf-8')
                except:
                    comm.printException(comm.initRdfErrorsFilePath, "RDF Organization Manager serialization error: ")
                    pass
        except:
            comm.printException(comm.initRdfErrorsFilePath, "RDF Organization Manager (addTriples) error: ")
            pass


class PeopleManager (OntologyData): 
    def __init__(self, od):
        OntologyData.__init__(self)
        
    def addTriples(self, chunkedList, addLemmas = True):
        try:
            newDataExists = False
            g = self.getPerRdfGraph()
            g_new = Graph()
            #define specific namespace prefix
            self.bindNamespaces(g)
            for andmed in chunkedList:
                for webpage in andmed:
                    gName = andmed[webpage]["gName"]
                    fName = andmed[webpage]["fName"]
                    name = andmed[webpage]["name"]
                    lemmaList = andmed[webpage]["lemmaSet"]
                    #print (lemmaList)
                    try:
                        #make triples
                        newPerson = URIRef(self.perStr + name.replace (">", "").replace ("<", "").replace ("|", "").replace (" ", "_").lower())
                        newGivenName = Literal(gName)
                        newFamilyName = Literal(fName)
                        newPerName = Literal(name)
                        newWebpage = URIRef(webpage);
                        
                        #add triples
                        #check if graph contains bob already
                        if ( newPerson, RDF.type, URIRef(self.person)) not in g:
                            newDataExists = True
                            g_new.add( (newPerson, RDF.type, URIRef(self.person)) )
                            if(newGivenName != Literal("")):
                                g_new.add( (newPerson, self.givenName, newGivenName) )
                            if(newFamilyName != Literal("")):
                                g_new.add( (newPerson, self.familyName, newFamilyName) )
                            g_new.add( (newPerson, self.perName, newPerName) )
                          
                        #check if graph contains bob already
                        if ( newPerson, self.mentionedAtSite, newWebpage) not in g:
                            newDataExists = True
                            g_new.add( (newPerson, self.mentionedAtSite, newWebpage) )
                        #add lemmas also
                        if(addLemmas):
                            for newLemma in lemmaList:
                                #check if graph contains bob already
                                if ( newPerson, self.lemma, Literal(newLemma)) not in g:
                                    newDataExists = True
                                    g_new.add( (newPerson, self.lemma, Literal(newLemma)) )
                    except:
                        comm.printException(comm.initRdfErrorsFilePath, "build_per_graph")
                        pass
            #print(str(newDataExists)) 
            #write rdf into file
            if (newDataExists):
                try:
                    gg = g+g_new
                    (gg).serialize(self.perRdf, format='pretty-xml', encoding='utf-8')
                except:
                    comm.printException(comm.initRdfErrorsFilePath, "RDF People Manager serialization error: ")
                    pass
        except:
            comm.printException(comm.initRdfErrorsFilePath, "RDF People Manager (addTriples) error: ")
            pass



class RdfFilesCreator(OntologyData):
    '''
         NB! this class is inteded to call only once at a start 
         as it re-writes all rdf-files (creates new blank rdf-s)
       Defines namespace and ontology, 
       and creates rdf-files separately for each type: location, organizations and people.
       Adds these common definitions to all 3 types of rdf-s.
       Inherits from basic class OntologyData, where the calss variables are defined.
       This class is used only at the start, when no rdf files are created yet.
    '''
    
    def __init__(self, od, namespaceURI = 'http://nerd.eurecom.fr/ontology'):
        OntologyData.__init__(self)
        self.initGraphs(od, namespaceURI)
               
        
    def initGraphs(self, od, namespaceURI):
        if not (os.path.isfile(od.locRdf) | os.path.isfile(od.orgRdf) | os.path.isfile(od.perRdf)):
           
            OntologyData.nerd = Namespace(namespaceURI + "#")
            OntologyData.ner = Namespace("http://www.estner.ee/estnerd#")
            
            #construct namespace strings for objects' namespaces
            OntologyData.locStr = OntologyData.nerd
            OntologyData.orgStr = OntologyData.nerd
            OntologyData.perStr = OntologyData.nerd
            
            OntologyData.lemma = OntologyData.ner.lemma#==URIRef("http://www.estner.ee/estnerd#lemma")
            OntologyData.mentionedAtSite = OntologyData.ner.mentionedAtSite#==URIRef("http://www.estner.ee/estnerd#mentionedAtSite")
            OntologyData.orgName = OntologyData.ner.orgName#==URIRef("http://www.estner.ee/estnerd#orgName")
            OntologyData.locationName = OntologyData.ner.locationName#==URIRef("http://www.estner.ee/estnerd#orgName")
    
            g = Graph()
            #define specific namespace prefix
            self.bindNamespaces(g)
            
            #describe ner as ontology
            g.add( (URIRef(OntologyData.ner), RDF.type, OntologyData.owlOntology) )
            g.add( (URIRef(OntologyData.ner), DC["title"], Literal("estNERD Ontology")) )
            g.add( (URIRef(OntologyData.ner), DC["description"], Literal("Locations, organizations and persons extracted from Estonian open data, using 'Estnltk — Open source tools for Estonian natural language processing' [http://tpetmanson.github.io/estnltk/].")) )
            #define owl#DatatypeProperty
            g.add( (OntologyData.lemma, RDF.type, OntologyData.datatypeProperty) )
            g.add( (OntologyData.mentionedAtSite, RDF.type, OntologyData.datatypeProperty) )

            
            self.locationGraph = g
            self.organizatioGraph = g
            self.peopleGraph = g
        #write rdf into file if the file do not exist yet
        if not os.path.isfile(od.locRdf):
            self.locationGraph.serialize(od.locRdf, format='pretty-xml', encoding='utf-8')
        if not os.path.isfile(od.orgRdf):
            self.locationGraph.serialize(od.orgRdf, format='pretty-xml', encoding='utf-8')
        if not os.path.isfile(od.perRdf):
            self.locationGraph.serialize(od.perRdf, format='pretty-xml', encoding='utf-8')
        
      
