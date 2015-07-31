#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 18, 2015
http://tpetmanson.github.io/estnltk/tutorials/ner.html
'''
from estnltk import tokenize, morf, ner
import itertools
import init_rdf
from storage import commonvariables as comm
import time

tokenizer = tokenize.Tokenizer()
analyzer = morf.PyVabamorfAnalyzer()
tagger = ner.NerTagger()

def printIncomingText(text):
    timeDir = time.strftime("%d_%m_%Y")
    jf = open(timeDir+"_incoming.txt", 'a')
    jf.write(str(text) + "\n")
    jf.close() 


def getEntities(url, text, ontologyData, orgWords=['kogu', 'selts', 'ansambel', 'keskus', 'ühendus', 'ühing', 'mtü', 'oü', 'as', 'klubi', 'asutus', 'keskus', 'fond', 'cup'], locWords=['vabarii', 'maakond']):
    #print("GETENTITIES ", url)
    #printIncomingText(text)
    ntwl = list()
    ner_tagged = None
    try:
        ner_tagged = tagger(analyzer(tokenizer(text)))
    except:
        comm.printException(comm.initRdfErrorsFilePath, "getEntities.py-def_getEntities_:_ner_tagged " + str(text))
        pass
    if (ner_tagged is not None):
        try:
            ntwl = ner_tagged.named_entities
        except:
            comm.printException(comm.initRdfErrorsFilePath, "getEntities.py-def_getEntities_:_ntwl" + str(len(ntwl)) + " " + str(text))
            pass
    try:
        if(len(ntwl) > 0):
            
            andmed = dict()
            #andmed[url]=dict()
            #print(text)
            #print(ner_tagged)
            #print(ntwl)
            for i in ntwl:
                label = i.label
                freqLemma = i.lemma.replace(';', '').replace(':', '').replace(',', '').replace('.', '').replace('?', '').replace('!', '').replace('"', '').replace("'", '').replace(' | ', '').replace('|', '').lower()
                
                #correct some ner labels
                for ow in orgWords:
                    if(ow.lower() in freqLemma.lower()):
                        label = "ORG"
                for lw in locWords:
                    if(lw.lower() in freqLemma.lower()):
                        label = "LOC"
                        
                #process values by labels
                if label == "PER":
                    entitySet = set()
                    if(freqLemma != ""):
                        name = freqLemma.title()
                        names = name.split(' ')
                        gName = ""
                        fName = ""
                        try:
                            if len(names) > 1:
                                if len(names) > 2:
                                    gName = names[0] + " " + names[1]
                                    fName = names[2]
                                elif len(names) == 2:
                                    gName = names[0]
                                    fName = names[1]
                        except:
                            comm.printException(comm.initRdfErrorsFilePath, "getEntities.py-def_getEntities_gname-fname")
                            pass
                        entitySet.add(freqLemma)
                        #to later remove, currently for avoid double values
                        entitySet.add(name)
                        entitySet.add(gName)
                        entitySet.add(fName)
                        wConcat = (' '.join(w.text for w in i.words)).replace(';', '').replace(':', '').replace(',', '').replace('.', '').replace('?', '').replace('!', '')
                        entitySet.add(wConcat)
                        lemmalist = list()
                        for w in i.words:
                            lemmalist.append(w.lemmas)
                        produkt = itertools.product(*lemmalist)
                        for j in produkt:
                            entitySet.add( " ".join(str(u) for u in(list(j)) if ((u.lower() != name.lower()) & (u != "") & (u.title() in names))  ) )
                        #now remove double values
                        if name in entitySet:
                            entitySet.remove(name)
                        if gName in entitySet:
                            entitySet.remove(gName)
                        if fName in entitySet:
                            entitySet.remove(fName)
                        if "" in entitySet:
                            entitySet.remove("")
                            
                        andmed={url: {"gName": gName, "fName": fName, "name": name, "lemmaSet": entitySet}};
                        if not(ontologyData.sharedList_per._callmethod('__contains__', (andmed,))):
                            ontologyData.sharedList_per._callmethod('append', (andmed,))    
                        
                        if ((ontologyData.sharedList_per)._callmethod('__len__') > comm.chunksize):
                            try:
                                chunkedList = ontologyData.sharedList_per[:]#makes copy,not refrence
                                del ontologyData.sharedList_per[:]
                                perManager = init_rdf.PeopleManager(ontologyData)
                                perManager.addTriples(chunkedList)
                            except:
                                comm.printException(comm.initRdfErrorsFilePath, "get_PER_entities") 
                                pass
                else:
                    objName = freqLemma.title()
                    entitySet = set();
                    entitySet.add(freqLemma);
                    wConcat = (' '.join(w.text for w in i.words)).replace(';', '').replace(':', '').replace(',', '').replace('.', '').replace('?', '').replace('!', '')
                    entitySet.add(wConcat)
                    lemmalist = list()
                    for w in i.words:
                        lemmalist.append(w.lemmas)
                    produkt = itertools.product(*lemmalist)
                    for j in produkt:
                        entitySet.add( " ".join(str(u) for u in(list(j)) if ((u.lower() != objName.lower()) & (u != ""))  ) )
                    if "" in entitySet:
                        entitySet.remove("")
                    
                    andmed={url: {objName: entitySet}};
                        
                    if(label == "ORG"):
                        if not(ontologyData.sharedList_org._callmethod('__contains__', (andmed,))):
                            ontologyData.sharedList_org._callmethod('append', (andmed,))
                    elif(label == "LOC"):
                        if not(ontologyData.sharedList_loc._callmethod('__contains__', (andmed,))):
                            ontologyData.sharedList_loc._callmethod('append', (andmed,))
                    
                    if ((ontologyData.sharedList_org)._callmethod('__len__') > comm.chunksize):
                        try:
                            chunkedList = (ontologyData.sharedList_org[:])#makes copy,not refrence
                            del ontologyData.sharedList_org[:]
                            #tests
                            #jf = open("tEst.txt", 'a', encoding='utf-8')
                            #jf.write(str(len(chunkedList)) + "\n")
                            #jf.close() 
                            orgManager = init_rdf.OrganizationManager(ontologyData)
                            orgManager.addTriples(chunkedList)
                        except:
                            comm.printException(comm.initRdfErrorsFilePath, "get_ORG_entities")
                            pass
                    if ((ontologyData.sharedList_loc)._callmethod('__len__') > comm.chunksize):
                        try:
                            chunkedList = ontologyData.sharedList_loc[:]#makes copy,not refrence
                            del ontologyData.sharedList_loc[:]
                            locManager = init_rdf.LocationManager(ontologyData)
                            locManager.addTriples(chunkedList)
                        except:
                            comm.printException(comm.initRdfErrorsFilePath, "get_LOC_entities")
                            pass
    except:
        comm.printException(comm.initRdfErrorsFilePath, "getEntities.py")
        pass




