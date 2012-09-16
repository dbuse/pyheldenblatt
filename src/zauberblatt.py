# -*- coding: utf-8 -*-
'''
Created on 06.09.2012

@author: dbuse
'''

# Nutzbarer Bereich:
# Kopf: 265 * 22,5

from collections import OrderedDict
from heldenblatt import Heldenblatt
import config

def import_zauber(fname='inhalt/Zauberliste.tsv'):
    labels = ['name', 'probe', 'zd', 'kosten', 'ziel', 'schwierigkeit', 'reichweite', 'wirkungsdauer', 'merkmale', 'seite']
    i = -1
    zauberliste = OrderedDict()
    for line in open(fname).readlines():
        i += 1
        row = line.split('\t')
        if len(row) != len(labels):
            print "Feldanzahlfehler bei nr %d. '%s' len: %d" % (i,row[0],len(row))
            continue
        zauberliste[row[0]] = dict([(labels[x],row[x].replace("\n","")) for x in range(len(labels))])
    return zauberliste

class Zauberblatt(Heldenblatt):
    """Druckklasse für den Zauberbogen"""
    
    orientation = "l"
    """Zauberblatt im Querformat drucken"""
    
    hintergrund = ('../inhalt/bilder/zauberblatt.png',0,0,297,210)
    
    def _set_config(self):
        # Konstante Abstände
        self.rand_links = 12
        
        # Schriftgrößen als Variablen
        self.zeilen_fontsize = 8
        self.kopfleiste_fontsize = 14
        
        # Konstante Größen der Kopfleiste
        self.kopfleiste_attribut_w = 32
        self.kopfleiste_h = 7.5
        
        
        # Felder der Kopfleiste
        self.kopfleistenfelder = {
            # Erste Zeile
            'Name': dict(weite=110, heldenfeld='Name', abteil=None),
            'Rasse': dict(weite=45, heldenfeld='Rasse', abteil=None),
            'Profession': dict(weite=110, heldenfeld='Profession', abteil=None),
            # Zweite Zeile
            'MU': dict(weite=self.kopfleiste_attribut_w, heldenfeld='MU', abteil='Attribute'),
            'KL': dict(weite=self.kopfleiste_attribut_w, heldenfeld='KL', abteil='Attribute'),
            'IN': dict(weite=self.kopfleiste_attribut_w, heldenfeld='IN', abteil='Attribute'),
            'CH': dict(weite=self.kopfleiste_attribut_w, heldenfeld='CH', abteil='Attribute'),
            'FF': dict(weite=self.kopfleiste_attribut_w, heldenfeld='FF', abteil='Attribute'),
            'GE': dict(weite=self.kopfleiste_attribut_w, heldenfeld='GE', abteil='Attribute'),
            'KO': dict(weite=self.kopfleiste_attribut_w, heldenfeld='KO', abteil='Attribute'),
            'KK': dict(weite=self.kopfleiste_attribut_w, heldenfeld='KK', abteil='Attribute'),
            'MR': dict(weite=self.kopfleiste_attribut_w, heldenfeld='MR', abteil='Basiswerte'),
            # Dritte Zeile
            'Merkmale': dict(weite=80, heldenfeld='Merkmale', abteil='Magische Sonderfertigkeiten'),
        }
    
    def drucke_blatt(self, held):
        self.drucke_kopfleiste(held)
        return
        
    def drucke_kopfleiste(self, held):
        self.pdf.set_font(family=config.FONT, style='B', size=self.kopfleiste_fontsize)
        self.pdf.set_left_margin(self.rand_links)
        
        zeilen = (
            ['Name', 'Rasse', 'Profession'],
            config.attribute[0:8] + ['MR'],
            ['Merkmale'],
        )
        
        for felder in zeilen:
            self.pdf.ln(self.kopfleiste_h)
            for feld in felder:
                template = self.kopfleistenfelder[feld]
                if template['abteil']:
                    text = held[template['abteil']][template['heldenfeld']]
                else: 
                    text = held[template['heldenfeld']]
                if isinstance(text, (list, tuple)):
                    text = ', '.join(text)
                self.pdf.cell(template['weite'], self.kopfleiste_h, "%s: %s" % (feld, text))

        
             
        return