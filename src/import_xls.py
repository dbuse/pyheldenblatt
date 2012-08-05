# -*- coding: utf-8 -*-

'''
Created on 03.08.2012

@author: joti
'''

import xlrd
from talente import Talent

    
def importXls(path):
    zeile1=""
    zeile2=""
    zeile3=""
    zeile1_dict = {}
    zeile2_dict = {}
    zeile3_dict = {}
    
    held={'Attribute': {
        'MU':12,'KL':14,'IN':15,'CH':12,'FF':13,'GE':12,'KO':13,'KK':11,'BE':0
    },
    'Besonderheiten':{
        'Vollzauberer':True,
    },
    'Sonderfertigkeiten':{
        'Kulturkunde':['Horasreich'],
        'Geländekunde':[],
        'Ortskenntnis':[],
        'Große Meditation': [],
        '':['Nandusgefälliges Wissen']
    }}
    held["Talente"]={}
    
    
    book = xlrd.open_workbook(path, encoding_override="utf-8")
    sh = book.sheet_by_name("Talente")
    for rx in range(sh.nrows):
        group1=sh.cell(rx,1)
        group2=sh.cell(rx,5)
        group3=sh.cell(rx,9)
        
        

        
        if group1.ctype!=0 :
            if zeile1!="" :
                held["Talente"][zeile1]=zeile1_dict
            zeile1_dict = {}
            if isinstance(group1.value, unicode) :
                zeile1=group1.value.encode('utf8')

                
            
        else :
            if sh.cell(rx, 2).ctype!=0 :
                if Talent.ist_talent(sh.cell(rx,2).value.encode('utf8')):
                    if sh.cell(rx,3).ctype!= 0 :
                        zeile1_dict[sh.cell(rx,2).value.encode('utf8')] = sh.cell(rx,3).value
                else :
                    pass
                    #TODO: Fehler werfen

                    
                                       
        if group2.ctype!=0 :
            if zeile2!="" :
                held["Talente"][zeile2]=zeile2_dict
            zeile2_dict={}
            zeile2=group2.value.encode('utf8')
            
        else :
            if sh.cell(rx, 6).ctype!=0 :
                if Talent.ist_talent(sh.cell(rx,6).value.encode('utf8')):
                    if sh.cell(rx,7).ctype!= 0 :
                        zeile2_dict[sh.cell(rx,6).value.encode('utf8')] = sh.cell(rx,7).value
                else :
                    pass
                    #TODO: Fehler werfen
                
                
        if group3.ctype!=0 :
            if zeile3!="" :
                held["Talente"][zeile3]=zeile3_dict
            zeile3_dict={}
            zeile3=group3.value.encode('utf8')
            
       
        if sh.cell(rx, 10).ctype!=0 :
            if Talent.ist_talent(sh.cell(rx,10).value.encode('utf8')):
                if sh.cell(rx,11).ctype!= 0 :
                    zeile3_dict[sh.cell(rx,10).value.encode('utf8')] = sh.cell(rx,11).value
            else :
                pass
                #TODO: Fehler werfen
    
    held["Talente"][zeile1]=zeile1_dict
    held["Talente"][zeile2]=zeile2_dict
    held["Talente"][zeile3]=zeile3_dict

    print held
    return held
        