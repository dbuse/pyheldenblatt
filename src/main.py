# -*- coding: utf-8 -*-
'''
Created on 16.07.2012

@author: dom
'''

from import_xls import importXLS
from import_xml import import_xml
from talentblatt import Talentblatt
from heldenblatt import MyFPDF
from talente import Talent
from zauberblatt import Zauberblatt

    
# Entweder python oder xls (später vielleicht auch xml)
mode = 'xml'

if __name__ == '__main__':
    print "Start!"
    
    held = None
    if mode == 'python':
        # setzt die variable "held" selbst: 
        execfile('../inhalt/helden/jarlak.py')
    elif mode == 'xls':
        held = importXLS("../inhalt/helden/Fedesco_Salingor.xls")
    elif mode == 'xml':
        held = import_xml("../inhalt/helden/Reo Klammwalder.xml")
    Talent.held_pruefen(held)
        
    fpdf = MyFPDF(orientation='P', unit='mm', format='A4')
    fpdf.add_font('Mason Regular', '', 'mason.py')
    fpdf.add_font('Mason Bold', 'B', 'masonbold.py')

    talente = Talentblatt(fpdf, zeilen_fontsize=8)
    talente.drucke_blatt(held)
    
    if 'Zauber' in held:
        print "### Achtung: Die Berechnung der Lernspalte ist noch nicht vollständig! Mehrfache Zauber (z.B. Adlerschwinge, Arcarnovi) und Hexalogien werden noch NICHT berücksichtigt! ###"
        zauber = Zauberblatt(fpdf)
        zauber.drucke_blatt(held)
        
    fpdf.output('../inhalt/ausgabe/Jarlak.pdf','F')
    print "Fertig!"
