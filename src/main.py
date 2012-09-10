# -*- coding: utf-8 -*-
'''
Created on 16.07.2012

@author: dom
'''

from import_xls import importXLS
from talentblatt import Talentblatt
from heldenblatt import MyFPDF
from talente import Talent
    
    
# Entweder python oder xls (später vielleicht auch xml)
mode = 'python'

if __name__ == '__main__':
    print "Start!"
    fpdf = MyFPDF(orientation='P', unit='mm', format='A4')
    pdf = Talentblatt(fpdf)
    held = None
    if mode == 'python':
        # setzt die variable "held" selbst: 
        execfile('../inhalt/helden/carisolan.py')
    elif mode == 'xls':
        held = importXLS("../inhalt/helden/Fedesco_Salingor.xls")
    Talent.held_pruefen(held)
    pdf.drucke_blatt(held)
    fpdf.output('../inhalt/ausgabe/test.pdf','F')
    print "Fertig!"
