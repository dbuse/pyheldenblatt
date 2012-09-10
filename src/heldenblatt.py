# -*- coding: utf-8 -*-
'''
Created on 06.09.2012

@author: dbuse
'''

from libs.pyfpdf import FPDF
import config

class MyFPDF(FPDF):
    """Überschriebene Zwischenklasse zur Anpassung des Encoding"""
    def cell(self, w, h, txt='',*args, **kwd):
        """Nur überschrieben um allen Unicode handlich umwandeln zu können"""
        FPDF.cell(self, w, h, txt.encode('latin-1'), *args, **kwd)
        
    def get_string_width(self, s):
        """Nur überschrieben um allen Unicode handlich umwandeln zu können"""
        return FPDF.get_string_width(self, s.encode('latin-1'))
    
class ZeilenFeld(object):
    
    def __init__(self,titel, weite, fontsize, text='', style='',align='',linie=False, font=config.FONT):
        self.titel = titel
        self.weite = weite
        self.text = text
        self.style = style
        self.align = align
        self.linie = linie
        self.font = font
        self.fontsize = fontsize
    
class Heldenblatt(object):
    """Grundklasse für alle Einzelblätter des Heldendokumentes"""
    
    orientation = "p"
    """Standardmäßig im Hochformat drucken"""
    
    def __init__(self, pdf):
        self.pdf = pdf
        self.pdf.set_auto_page_break(auto=False)
        self.pdf.add_page(orientation=self.orientation)
        self.pdf.image(*self.hintergrund)
        # Spezifische Konfiguration setzen
        self._set_config()