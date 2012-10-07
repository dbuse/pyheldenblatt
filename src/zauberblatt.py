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
from talente import ZauberTalent



class Zauberblatt(Heldenblatt):
    """Druckklasse für den Zauberbogen"""
    
    orientation = "l"
    """Zauberblatt im Querformat drucken"""
    
    hintergrund = ('../inhalt/bilder/zauberblatt.png',0,0,297,210)
    
    def _set_config(self):
        # Konstante Abstände
        self.rand_links = 12
        self.zeilen_w = 273
        self.zeilen_seitenabstand = 0.5
        
        # Schriftgrößen als Variablen
        self.zeilen_fontsize = 8
        self.kopfleiste_fontsize = 14
        self.multiplikator_h = 0.6
        
        # Eigenschaften der Talentzeilen
        self.zeilen_se_w = self.zeilen_fontsize * 0.5
        self.zeilen_probe_w = self.zeilen_fontsize * 2
        self.zeilen_taw_w = self.zeilen_fontsize * 0.75
        self.zeilen_h = self.zeilen_fontsize * self.multiplikator_h
        
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
            'Merkmale': dict(weite=120, heldenfeld='Merkmale', abteil='Magische Sonderfertigkeiten'),
            'Repräsentationen': dict(weite=120, heldenfeld="Repräsentationen", abteil="Magische Sonderfertigkeiten"),
        }
        self.zeilenfelder = {
            'se': dict(titel='se', weite=self.zeilen_se_w, fontsize=self.zeilen_fontsize, linie=True),
            'talent': dict(titel='talent', fontsize=self.zeilen_fontsize, style='B', align='L', font=config.FONT),
            'probe': dict(titel='probe', weite=self.zeilen_probe_w, fontsize=self.zeilen_fontsize, style='I', linie=True),
            'taw': dict(titel='taw', weite=self.zeilen_taw_w, fontsize=self.zeilen_fontsize, style='B',align='C', linie=True),
            'taw_leer': dict(titel='taw_leer', weite=self.zeilen_taw_w, fontsize=self.zeilen_fontsize, style='B', linie=True),
            'zd': dict(titel='zd', weite=self.zeilen_fontsize * 2, fontsize=self.zeilen_fontsize, style='', linie=True),
            'kosten': dict(titel='kosten', weite=self.zeilen_fontsize * 3, fontsize=self.zeilen_fontsize, style='', linie=True),
            'reichweite': dict(titel='reichweite', weite=self.zeilen_fontsize * 3, fontsize=self.zeilen_fontsize, style='', linie=True),
            'ziel': dict(titel='ziel', weite=self.zeilen_fontsize * 2, fontsize=self.zeilen_fontsize, style='', linie=True),
            'wd': dict(titel='wd', weite=self.zeilen_fontsize * 3, fontsize=self.zeilen_fontsize, style='', linie=True),
            'schwierigkeit': dict(titel='schwierigkeit', weite=self.zeilen_taw_w, fontsize=self.zeilen_fontsize, style='B', align='C', linie=True),
            'merkmale': dict(titel='merkmale', weite=self.zeilen_fontsize * 4, fontsize=self.zeilen_fontsize, style='I', linie=True),
            'lernmods': dict(titel='lernmods', weite=self.zeilen_taw_w, fontsize=self.zeilen_fontsize, style='B', align='C', linie=True),
            'lernen': dict(titel='lernen', weite=self.zeilen_taw_w, fontsize=self.zeilen_fontsize, style='B', align='C', linie=True),
            'seite': dict(titel='seite', weite=self.zeilen_fontsize * 1.5, fontsize=self.zeilen_fontsize, style='I', align='C'),
        }
        self.feldreihenfolge = ['se', 'talent', 'probe', 'taw', 'taw_leer', 'zd', 'kosten', 'reichweite', 'ziel', 'wd', 
                                'schwierigkeit', 'merkmale', 'lernmods', 'lernen', 'seite']
        return
    
    def drucke_blatt(self, held):
        self.drucke_kopfleiste(held)
        self.drucke_zauberliste(held)
        return
        
    def drucke_kopfleiste(self, held):
        print held
        self.pdf.set_font(family=config.FONT, style='B', size=self.kopfleiste_fontsize)
        self.pdf.set_left_margin(self.rand_links)
        
        zeilen = (
            ['Name', 'Rasse', 'Profession'],
            config.attribute[0:8] + ['MR'],
            ['Merkmale', 'Repräsentationen'],
        )
        
        for felder in zeilen:
            self.pdf.ln(self.kopfleiste_h)
            for feld in felder:
                #print feld
                template = self.kopfleistenfelder[feld]
                if template['abteil']:
                    text = held[template['abteil']][template['heldenfeld']]
                else: 
                    text = held[template['heldenfeld']]
                if isinstance(text, (list, tuple)):
                    text = ', '.join(text)
                self.pdf.cell(template['weite'], self.kopfleiste_h, "%s: %s" % (feld, text))
        self.pdf.ln(15)
        return
    
    def drucke_zauberliste(self, held):
        # Erst noch Kopfzeile Drucken
        
        # Einzelne Zauber drucken
        alle = ZauberTalent.alle()
        for zauber, zauberobj in alle.iteritems():
            if zauber in held['Zauber']:
                d = zauberobj.get_print_dict(**held['Zauber'][zauber])
                self.drucke_zeile(d)
        return