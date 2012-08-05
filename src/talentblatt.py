# -*- coding: utf-8 -*-
'''
Created on 04.08.2012

@author: dom
'''
import math
from libs.pyfpdf import FPDF
from talente import Talentkategorie

FONT = 'Times'
OBENLINKS = {'links':(12,35),'rechts':(106.5,35)}

# Nutzbare Fläche ist 250mm * 92,5mm (Je Spalte)
# Linke obere Ecke der linken Spalte: 12mm/36,5mm
# Linke obere Ecke der rechten Spalte: 106,5mm/36,5mm


class Talentblatt(FPDF):
    
    def __init__(self, *arg, **kwd):
        FPDF.__init__(self, *arg, **kwd)
        
        # Konstante Abstände und Längen
        self.rand_links = 12
        self.zeilen_w = 92
        self.zeilen_seitenabstand = 0.5
        
        # Schriftgrößen als Variablen
        self.zeilen_fontsize = 8
        self.attribute_fontsize = 16
        self.multiplikator_h = 0.6

        # Kopfzeile mit Attributen (müssen nicht variabel sein)
        self.attribute_h = 10
        self.attribute_w = 20.5
        self.attribute_be_w = 25
        self.attribute_dummy_w = 3
        
        # Eigenschaften der Talentzeilen
        self.zeilen_se_w = self.zeilen_fontsize * 0.5
        self.zeilen_h = self.zeilen_fontsize * self.multiplikator_h
        self.zeilen_taw_w = self.zeilen_fontsize * 0.75
        self.zeilen_atpa_w = self.zeilen_fontsize * 0.75
        self.zeilen_be_kom_w = self.zeilen_fontsize 
        
        # Überschriften für Talentblöcke
        self.zeilentitel_offset_oben = 1
        self.zeilentitel_fontsize_haupt = self.zeilen_fontsize * 1.5
        self.zeilentitel_fontsize_neben = self.zeilen_fontsize * 1.25
        self.zeilentitel_h = self.zeilentitel_fontsize_haupt * self.multiplikator_h
        self.zeilentitel_kopfabstand = 2*self.zeilen_h - self.zeilentitel_h 
        return
    
    def cell(self, w, h, txt='',*args, **kwd):
        """Nur überschrieben um allen Unicode handlich umwandeln zu können"""
        FPDF.cell(self, w, h, txt.encode('latin-1'), *args, **kwd)
        
    def get_string_width(self, s):
        return FPDF.get_string_width(self, s.encode('latin-1'))

    def attribute_leiste(self, attribute):
        self.set_font(family=FONT, style='B', size=self.attribute_fontsize)
        self.set_left_margin(self.rand_links)
        for attr in ['MU','KL','IN','CH','FF','GE','KO','KK']:
            self.cell(self.attribute_w, self.attribute_h, "%s: %d" % (attr, attribute[attr]), align='C')
        self.cell(self.attribute_dummy_w, self.attribute_h, '')
        self.cell(self.attribute_be_w, self.attribute_h, "BE: %d" % attribute['BE'])
        return
    
    def _sonderfertigkeiten_gruppen(self, besonderheiten):
        gruppen = ['Kulturkunde', 'Geländekunde', 'Ortskenntnis']
        if 'Vollzauberer' in besonderheiten and besonderheiten['Vollzauberer']:
            gruppen.append('Große Meditation')
        if 'Geweihter' in besonderheiten and besonderheiten['Geweihter']:
            gruppen.append('Karmalqueste')
        gruppen.append('')
        return gruppen
    
    def sonderfertigkeiten_zeilen(self,sonderfertigkeiten, besonderheiten):
        self.set_font(family=FONT, style='', size=self.zeilen_fontsize)
        verfuegbare_weite =self.zeilen_w - 2* self.zeilen_seitenabstand 
        gruppen = self._sonderfertigkeiten_gruppen(besonderheiten)
        anzahl = 0
        for gruppe in gruppen:
            titel = "%s: " % gruppe
            zeile = []
            for sf in sonderfertigkeiten:
                if self.get_string_width(titel + ', '.join(zeile + [str(sf)])) > verfuegbare_weite:
                    anzahl += 1
                    titel = ''
                    zeile = [str(sf)]
            anzahl += 1
        return anzahl + 1 # Leerzeile drunter
        
    
    def sonderfertigkeitenblock(self, sonderfertigkeiten, besonderheiten={}):
        self.set_font(family=FONT, style='B', size=self.zeilentitel_fontsize_haupt)
        links = self.get_x() + self.zeilen_seitenabstand
        rechts = self.get_x() + self.zeilen_w - self.zeilen_seitenabstand
        # Überschrift
        self.ln(self.zeilentitel_kopfabstand)
        self.cell(self.zeilen_w, self.zeilentitel_h, 'Sonderfertigkeiten (Allgemein)')
        self.line(links, self.get_y() + self.zeilentitel_h, rechts, self.get_y() + self.zeilentitel_h)
        self.ln(self.zeilentitel_h)
        
        # Zeilen abarbeiten
        gruppen = self._sonderfertigkeiten_gruppen(besonderheiten)
        self.set_font(family=FONT, style='', size=self.zeilen_fontsize)
        for gruppe in gruppen:
            sonderfertigkeiten.setdefault(gruppe,{}) # Leere Gruppen voraussetzen
            zeile = []
            titel = gruppe and gruppe + ': ' or '' 
            for sf in sonderfertigkeiten[gruppe]:
                sf = str(sf)
                if self.get_string_width(titel + ', '.join(zeile + [sf])) <= self.zeilen_w:
                    zeile.append(sf)
                else:
                    # Zeile schon zu voll -> Rausschreiben und neue Zeile beginnen. 
                    self.cell(self.zeilen_w, self.zeilen_h, titel + ', '.join(zeile))
                    self.line(links, self.get_y() + self.zeilen_h, rechts, self.get_y() + self.zeilen_h)
                    self.ln(self.zeilen_h)
                    zeile = [sf]
                    titel = ''
            # Zeile Rausschreiben
            self.cell(self.zeilen_w, self.zeilen_h, titel + ', '.join(zeile))
            self.line(links, self.get_y() + self.zeilen_h, rechts, self.get_y() + self.zeilen_h)
            self.ln(self.zeilen_h)
        # Leerzeile
        self.ln(self.zeilen_h)
        self.image('../inhalt/bilder/line-01.png', self.get_x(), self.get_y(), self.zeilen_w + 0.5, 1)
        
    def _konfiguriere_zeile(self, talent, taw, linienfelder, textfelder):
        # Feldgrößen bestimmen und Texte vorbereiten
        felder = []
        felder.append(('se',self.zeilen_se_w, '', '','', True))
        felder.append(('talent',self.get_string_width(talent),talent, 'B','L', False))
        # Schwierigkeit und Probe
        self.set_font(family=FONT, style='I', size=self.zeilen_fontsize)
        if 'probe' in textfelder and textfelder['probe'] is not None:
            feldtxt = ' (%s)' % textfelder['probe']
            felder.append(('probe',self.get_string_width(feldtxt), feldtxt, 'I','L', False))
        elif 'schwierigkeit' in textfelder:
            feldtxt = ' (%s)' % textfelder['schwierigkeit']
            felder.append(('schwierigkeit',self.get_string_width(feldtxt), feldtxt, 'I','L', False))
        self.set_font(family=FONT, style='B', size=self.zeilen_fontsize)
        grenze = len(felder)
        # At/PA, BE, Komplexität und TaW
        if 'AT' in linienfelder: # wo AT ist, ist auch PA
            felder.append(('at', self.zeilen_atpa_w, linienfelder['AT'], 'B','C', True))
            felder.append(('pa', self.zeilen_atpa_w, linienfelder['PA'], 'B','C', True))
        if 'BE' in linienfelder:
            felder.append(('be', self.zeilen_be_kom_w, linienfelder['BE'], 'B','C', True))
        if 'Kom' in linienfelder:
            felder.append(('kom', self.zeilen_be_kom_w, linienfelder['Kom'], 'B','C', True))
        felder.append(('taw', self.zeilen_taw_w, taw, 'B','C', True))
        felder.append(('taw_leer', self.zeilen_taw_w, '', 'B','', False))
        # Dummy zwischen Text- und Linienfeldern nachtragen
        verbrauchte_weite = sum((feld[1] for feld in felder)) + self.zeilen_seitenabstand
        verbleibende_weite = self.zeilen_w - verbrauchte_weite
        felder.insert(grenze, ('dummy',verbleibende_weite, '', 'B','', True))
        return felder
        
    def zeile(self, talent, taw, linienfelder={}, textfelder={}, leerzeile=False, **kwd):
        self.set_font(family=FONT, style='B', size=self.zeilen_fontsize)
        # untere Linie Ziehen
        self.line(self.get_x() + self.zeilen_seitenabstand,
                  self.get_y() + self.zeilen_h,
                  self.get_x() + self.zeilen_w - self.zeilen_seitenabstand,
                  self.get_y() + self.zeilen_h)
        felder = self._konfiguriere_zeile(talent, taw, linienfelder, textfelder)
        # Felder und begrenzungslinien Drucken
        for feld in felder:
            self.set_font(family=FONT, style=feld[3], size=self.zeilen_fontsize)
            if leerzeile:
                self.cell(feld[1],self.zeilen_h, '')
            else:
                self.cell(feld[1],self.zeilen_h, str(feld[2]), align=feld[4])
            if feld[5]:
                self.line(self.get_x(), self.get_y(), self.get_x(), self.get_y() + self.zeilen_h)
        # Zeilenumbruch und fertig!
        return self.ln(self.zeilen_h)
    
        
    def zeilentitel(self, text, schwierigkeit='B', be_komp=None, at_pa=None):
        self.ln(self.zeilentitel_kopfabstand)
        links = self.get_x() + self.zeilen_seitenabstand
        rechts = self.get_x() + self.zeilen_w - self.zeilen_seitenabstand
        oben = self.get_y() + self.zeilentitel_offset_oben
        unten = self.get_y() + self.zeilentitel_h
        
        minus = links + 2*self.zeilen_taw_w - 0.5
        linien = [self.zeilen_taw_w * 2]
        if be_komp: 
            minus += self.zeilen_be_kom_w
            linien.append(self.zeilen_be_kom_w)
        if at_pa:
            minus += 2*self.zeilen_atpa_w
            linien.append(self.zeilen_atpa_w * 2)
        
        vonrechts = rechts
        for linie in linien:
            vonrechts -= linie
            self.line(vonrechts, oben, vonrechts, unten)
        self.line(links, unten, rechts, unten)
        
        self.set_font(family=FONT, style='B', size=self.zeilentitel_fontsize_haupt)
        self.cell(self.get_string_width(text), self.zeilentitel_h, text)
        minus += self.get_string_width(text)
        self.set_font(family=FONT, style='B', size=self.zeilentitel_fontsize_neben)
        if schwierigkeit:
            schwierigkeit_txt = " (%s)" % schwierigkeit
            schwierigkeit_w = self.get_string_width(schwierigkeit_txt)
            minus += schwierigkeit_w 
            self.cell(schwierigkeit_w, self.zeilentitel_h, schwierigkeit_txt)
        # Dummy-Zelle zum Auffüllen
        self.cell(rechts - minus, self.zeilentitel_h)
        if at_pa:
            self.cell(self.zeilen_atpa_w*2, self.zeilentitel_h, 'AT/PA', align='C')
        if be_komp:
            self.cell(self.zeilen_be_kom_w, self.zeilentitel_h, be_komp, align='C')
        self.cell(self.zeilen_taw_w*2, self.zeilentitel_h, 'TaW', align='C')
        return self.ln(self.zeilentitel_h)
    
    def talentblock(self, titel, zeilen, leerzeilen=0):
        alle = Talentkategorie.alle()
        self.zeilentitel(titel, alle[titel].schwierigkeit, alle[titel].be_komp, alle[titel].at_pa)
        for talent, talentobj in alle[titel].talente.iteritems():
            if talent not in zeilen:
                if talentobj.ist_basis:
                    zeilen[talent] = {'taw':0}
                else:
                    continue 
            d = alle[titel].talente[talent].get_print_dict(**zeilen[talent])
            self.zeile(**d)
        for _ in xrange(leerzeilen):
            self.zeile(leerzeile=True, **d)
            
    def anzahl_zeilen(self, held, gruppe):
        anzahl = len(held['Talente'][gruppe])
        for talent, talentobj in Talentkategorie.alle()[gruppe].talente.iteritems():
            if talent not in held['Talente'][gruppe] and talentobj.ist_basis:
                anzahl += 1
        return anzahl
            
    def platz_pro_seite(self, held, verteilung, leerzeilen={}, sonderfertigkeiten_sind='links'):
        platz = {'links':-99,'rechts':-99}
        for seite, gruppen in verteilung.iteritems():
            summe = sum(self.anzahl_zeilen(held, gruppe) + leerzeilen[gruppe] for gruppe in gruppen)
            summe += len(gruppen) * 2
            if sonderfertigkeiten_sind == seite:
                summe += self.sonderfertigkeiten_zeilen(held['Sonderfertigkeiten'], held['Besonderheiten']) + 2
            platz[seite] = math.floor(250.0 / self.zeilen_h) - summe
        return platz
            
            
    def helden_drucken(self, held):
        seiten = {'links':['Kampf','Körper','Gesellschaft'],
                  'rechts':['Natur','Wissen','Sprachen','Schriften','Handwerk']}
        gruppen = ['Kampf','Körper','Gesellschaft','Natur','Wissen','Sprachen','Schriften','Handwerk']
        leerzeilen = {}
        for gruppe in gruppen:
            leerzeilen[gruppe] = 0 
        zeiger = 0
        seite = None
        # Platz mit Leerzeilen auffüllen
        while True:
            platz = self.platz_pro_seite(held, seiten, leerzeilen)
            if platz['links'] <= 0 and platz['rechts'] <= 0:
                break
            
            # Gruppe zum Leerzeilen erhöhen suchen
            while True:
                zeiger = zeiger % len(gruppen)
                if gruppen[zeiger] in seiten['links']: seite = 'links'
                else: seite = 'rechts'
                if platz[seite] > 0:
                    leerzeilen[gruppen[zeiger]] += 1
                    zeiger += 1
                    break 
                else:
                    zeiger += 1
            
        self.attribute_leiste(held['Attribute'])
        self.set_y(35)
        self.sonderfertigkeitenblock(held['Sonderfertigkeiten'],held['Besonderheiten'])
        for gruppen in seiten.itervalues():
            for gruppe in gruppen:
                self.talentblock(gruppe, held['Talente'][gruppe], leerzeilen[gruppe])
            self.set_y(35)
            self.set_left_margin(106.5)