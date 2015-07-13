import sys, json
from rdflib import Graph, Literal, URIRef
from pprint import pprint
 
data = dict()
try:
    data = json.loads(sys.argv[1])
    #sys.exit(1)
except: # catch *all* exceptions
    e = sys.exc_info()[0]
    #print('Error: %s' % e )
    f = open('myUrrore.txt','w')
    f.write(thise) # python will convert \n to os.linesep
    f.close()
    sys.exit(1)


g = Graph()
try:
    g.parse("data2.rdf")
except:
    e = sys.exc_info()[0]
    print('Error: %s' % e )


def getJsonReturnValues(qstring, displayHtml):
    res = dict()
    res["qstring"] = qstring
    res["display"] = displayHtml
    return json.dumps(res)

def selectOrgByName(orgname):
    name = Literal(orgname)
    qstring = """SELECT DISTINCT * 
WHERE
{
{{?obj ner:orgName ?name} UNION {?obj ner:lemma ?name}} .
?obj ner:mentionedAtSite ?webpage
}
ORDER BY ?webpage"""
    sparqlRes = g.query(qstring, initBindings={'name': name})
    displayHtml = getJsonResultOfObject(sparqlRes)
    return getJsonReturnValues(qstring, displayHtml)

def selectLocationByName(locname):
    name = Literal(locname)
    qstring = """SELECT DISTINCT * 
WHERE
{
{{?obj ner:locationName ?name} UNION {?obj ner:lemma ?name}} .
?obj ner:mentionedAtSite ?webpage
}
ORDER BY ?webpage"""
    sparqlRes = g.query(qstring, initBindings={'name': name})
    displayHtml = getJsonResultOfObject(sparqlRes)
    return getJsonReturnValues(qstring, displayHtml)

def selectPersonByFName(famname):
    fname = Literal(famname)
    qstring = """SELECT DISTINCT * 
WHERE
{
{{?obj foaf:givenName ?gname} UNION {?obj ner:lemma ?gname}} .
{{?obj foaf:familyName ?fname} UNION {?obj ner:lemma ?fname}} .
?obj ner:mentionedAtSite ?webpage
}
ORDER BY ?gname ?webpage"""
    sparqlRes = g.query(qstring, initBindings={'fname': fname})
    displayHtml = getJsonResultOfPersonObject(sparqlRes)
    return getJsonReturnValues(qstring, displayHtml)

def selectPersonByGName(givname):
    gname = Literal(givname)
    qstring = """SELECT DISTINCT * 
WHERE
{
{{?obj foaf:givenName ?gname} UNION {?obj ner:lemma ?gname}} .
{{?obj foaf:familyName ?fname} UNION {?obj ner:lemma ?fname}} .
?obj ner:mentionedAtSite ?webpage
}
ORDER BY ?fname ?webpage"""
    sparqlRes = g.query(qstring, initBindings={'gname': gname})
    displayHtml = getJsonResultOfPersonObject(sparqlRes)
    return getJsonReturnValues(qstring, displayHtml)

def selectPersonByName(givname, famname):
    gname = Literal(givname)
    fname = Literal(famname)
    qstring = """SELECT DISTINCT * 
WHERE
{
{{?obj foaf:givenName ?gname} UNION {?obj ner:lemma ?gname}} .
{{?obj foaf:familyName ?fname} UNION {?obj ner:lemma ?fname}} .
?obj ner:mentionedAtSite ?webpage
}
ORDER BY ?webpage"""
    sparqlRes = g.query(qstring, initBindings={'gname': gname, 'fname': fname})
    displayHtml = getJsonResultOfPersonObject(sparqlRes)
    return getJsonReturnValues(qstring, displayHtml)

#----------------------------------------------------------------------------------------

def selectOrg():
    qstring = """SELECT DISTINCT * 
WHERE
{
?obj ner:orgName ?name .
?obj ner:mentionedAtSite ?webpage
}
ORDER BY ?name ?webpage"""
    sparqlRes = g.query(qstring)
    displayHtml = getJsonResultOfObject(sparqlRes)
    return getJsonReturnValues(qstring, displayHtml)

def selectLocation():
    qstring = """SELECT DISTINCT * 
WHERE
{
?obj ner:locationName ?name .
?obj ner:mentionedAtSite ?webpage
}
ORDER BY ?name ?webpage"""
    sparqlRes = g.query(qstring)
    displayHtml = getJsonResultOfObject(sparqlRes)
    return getJsonReturnValues(qstring, displayHtml)

def selectPerson():
    qstring = """SELECT DISTINCT * 
WHERE
{
?obj foaf:familyName ?fname .
?obj foaf:givenName ?gname .
?obj ner:mentionedAtSite ?webpage
}
ORDER BY ?fname ?gname ?webpage"""
    sparqlRes = g.query(qstring)
    displayHtml = getJsonResultOfPersonObject(sparqlRes)
    return getJsonReturnValues(qstring, displayHtml)


#----------------------------------------------------------------------------------------
def selectObjectsOnWebPage(weburi, locObject = True, orgObj = True, peopleObj = True):
    qstrings = dict()
    wpage = URIRef(weburi)
    objekt = dict()
    if(orgObj):
        qstring = """SELECT ?name 
WHERE
{
?obj ner:mentionedAtSite ?webpage .
?obj ner:orgName ?name .
}"""
        sparqlRes = g.query(qstring, initBindings={'webpage': wpage})
        qstrings["org"] = qstring;
        objekt["org"] = getListResultOfObjectOnSite(sparqlRes)
    
    if(locObject):
        qstring = """SELECT ?name 
WHERE
{
?obj ner:mentionedAtSite ?webpage .
?obj ner:locationName ?name .
}"""
        sparqlRes = g.query(qstring, initBindings={'webpage': wpage})
        qstrings["loc"] = qstring;
        objekt["loc"] = getListResultOfObjectOnSite(sparqlRes)
    
    if(peopleObj):
        qstring = """SELECT ?gname ?fname 
WHERE
{
?obj foaf:givenName ?gname .
?obj foaf:familyName ?fname .
?obj ner:mentionedAtSite ?webpage
}"""
        sparqlRes = g.query(qstring, initBindings={'webpage': wpage})
        qstrings["people"] = qstring;
        objekt["people"] = getListResultOfPersonObjectOnSite(sparqlRes)
    displayHtml = dict()
    displayHtml[weburi] = objekt
    return getJsonReturnValues(qstrings, displayHtml)


#----------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------
def getJsonResultOfObject(sparqlRes):
    stack = dict()
    for row in sparqlRes:
        key = ""
        for a in row:
            if(type(a) is Literal):
                if(key is not ""):
                    key = key + " " + a
                else:
                    key = a
        #key = row.name
        if key not in stack:
            stack[key] = [row.webpage]
        else:
            stack[key].append(row.webpage)
    return (stack)

#----------------------------------------------------------------------------------------
def getJsonResultOfPersonObject(sparqlRes):
    stack = dict()
    for row in sparqlRes:
        key = row.gname + " " + row.fname
        #key = row.name
        if key not in stack:
            stack[key] = [row.webpage]
        else:
            stack[key].append(row.webpage)
    return (stack) 

def getListResultOfObjectOnSite(sparqlRes):
    stack = list()
    for row in sparqlRes:
            stack.append(row.name)
    return (stack) 

def getListResultOfPersonObjectOnSite(sparqlRes):
    stack = list()
    for row in sparqlRes:
            stack.append(row.gname + " " + row.fname)
    return (stack) 

#------------------------------------------------------------------
#END OF FUNCTIONS
#------------------------------------------------------------------

#qresjson = selectObjectsOnWebPage("http://www.epl.ee", True, False, True)
#qresjson = selectOrgByName("MTÜ DUO kirjastus")
qresjson = {}

''''''''''''''''''''''''
#1st col key:
fstkey = "fst"
#2nd col key:
scndkey = "scnd"

if(fstkey in data):
    #print(data["fst"][0][0])
    parameter = data["fst"][0]
    #print(parameter)
    tyyp = str(data["fst"][1])
    #print(parameter["gname"])
    #print(tyyp == "per")
    #print("gname" in parameter)
    #print(tyyp)
    if(parameter[0] == "null"):
        #print(parameter)
        if(tyyp == "loc"):
            qresjson = selectLocation()
        elif(tyyp == "org"):
            qresjson = selectOrg()
        elif(tyyp == "per"):
            qresjson = selectPerson()
    else:
        if(tyyp == "loc"):
            qresjson = selectLocationByName(parameter[0])
        elif(tyyp == "org"):
            qresjson = selectOrgByName(parameter[0])
        else:
            gKey = "gname"
            fKey = "fname"
            if((gKey in parameter[0]) & (fKey in parameter[0])):
                qresjson = selectPersonByName(parameter[0][gKey], parameter[0][fKey])
            elif(gKey in parameter[0]):
                qresjson = selectPersonByGName(parameter[0][gKey])
            elif(fKey in parameter[0]):
                qresjson = selectPersonByFName(parameter[0][fKey])

if(scndkey in data):
    #print(data)
    #print(fstkey in data)
    #print(scndkey in data)
    wurl = data[scndkey]["uri"]
    loc = data[scndkey]["loc"]
    org = data[scndkey]["org"]
    per = data[scndkey]["per"]
    qresjson = selectObjectsOnWebPage(wurl, loc, org, per)


print (qresjson)












