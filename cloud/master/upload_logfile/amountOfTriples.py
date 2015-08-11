#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

# enable debugging
import cgitb
cgitb.enable()

import os, sys
import json
from rdflib import Graph
import commonVariables as comm

if __name__ == '__main__':
    www_data = json.loads(sys.argv[1])
    mylargefile = www_data["statfile"]
        #save info about amount of triples
    for fname in comm.rdfFnames:
        g_path = comm.pathToRDFdir + fname + ".rdf" 
        if (os.path.exists(g_path)):
            g_old = Graph()
            g_old.parse(g_path)
        if(mylargefile is not ""):
            note=(fname + " nr of triples: " + str(len(g_old)) + "\n")
            comm.saveStatistics(mylargefile, note)