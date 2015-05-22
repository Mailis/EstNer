#!/usr/bin/python3.4
# -*- coding: UTF-8 -*-
'''
Created on Feb 21, 2015
alias python=python3
sudo pip install xlrd
http://www.youlikeprogramming.com/2012/03/examples-reading-excel-xls-documents-using-pythons-xlrd/
https://github.com/python-excel/xlrd
'''
# enable debugging
import cgitb
cgitb.enable()

import xlrd
import getEntities
import commonVariables as comm
from urllib.request import urlretrieve as urr
        
def readExcel(filePath, url, ontologyData):
    try:
        urr(url, filePath)
        try:
            workbook = xlrd.open_workbook(filePath)
            worksheets = workbook.sheet_names()
            for worksheet_name in worksheets:
                worksheet = workbook.sheet_by_name(worksheet_name)
                num_rows = worksheet.nrows - 1
                num_cells = worksheet.ncols - 1
                curr_row = -1
                while curr_row < num_rows:
                    curr_row += 1
                    #row = worksheet.row(curr_row)
                    #print ('Row:', curr_row)
                    curr_cell = -1
                    while curr_cell < num_cells:
                        curr_cell += 1
                        # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                        cell_type = worksheet.cell_type(curr_row, curr_cell)
                        cell_value = worksheet.cell_value(curr_row, curr_cell)
                        if (cell_type == 1):
                            sentences = comm.replaceToPunkts(cell_value)
                            for sentence in sentences:
                                if(len(sentence) > 2) & (not comm.is_number(sentence)):
                                    getEntities.getEntities(url, sentence, ontologyData)
        
        except:
            comm.printException(comm.pathToSaveParsingErrors, "read_excel.py " + url)
            pass
    except:
        comm.printException(comm.pathToSaveParsingErrors, "read_excel.py " + url)
        pass
'''
import initRdf, sys, traceback
from urllib import request as ur                   
od = initRdf.OntologyData('/var/www/html/mag/rdf_files/')
initRdf.RdfFilesCreator(od)
url = 'http://duokirjastus.eu/cloud/rdf/dlTest-.xls'
#url = 'dlTest-.xls'
saveExcelTo = 'tmpExcels/ekselfile'
#excelFile = ur.urlretrieve(url, saveExcelTo)
excelFile = ur.urlopen(url)
#print(excelFile.info()["Content-Type"])
reed = excelFile.read()
#print(reed)

import csv
with open(saveExcelTo, newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
'''
'''
try:
    readExcel(reed, url, od)
except TypeError as e:
    print (traceback.format_exc())
    print (sys.exc_info()[0])
except:
    e = sys.exc_info()[0]
    print( "<p>Error: %s</p>" % e )
'''   
    
    
    
    
    
    
    
    
