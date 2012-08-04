# -*- coding: utf-8 -*-
'''
Created on 16.07.2012

@author: dom
'''

from import_xls import importXls
from talentblatt import Talentblatt
    
    
# Entweder python oder xls (später vielleicht auch xml)
mode = 'python'

if __name__ == '__main__':
    pdf = Talentblatt(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=False)
    pdf.add_page()
    pdf.image('../inhalt/bilder/bg-03.png',0,0,210,297)
    held = None
    if mode == 'python':
        # setzt die variable "held" selbst: 
        execfile('../inhalt/helden/carisolan.py')
    elif mode == 'xls':
        held = importXls("/home/joti/Dokumente/python/Talentblatt/xls/Fedesco_Salingor.xls")
    pdf.helden_drucken(held)
    pdf.output('../inhalt/ausgabe/test.pdf','F')
