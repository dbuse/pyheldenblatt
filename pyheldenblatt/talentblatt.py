# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

import math
from pkg_resources import resource_filename

from .talente import Talentgruppe
from .heldenblatt import Heldenblatt, ZeilenFeld
from . import config


# Nutzbare Fläche ist 250mm * 92,5mm (Je Spalte)
# Linke obere Ecke der linken Spalte: 12mm/36,5mm
# Linke obere Ecke der rechten Spalte: 106,5mm/36,5mm

def sonderfertigkeiten_gruppen(besonderheiten):
    """Baut die Grundstruktur der Sonderfertigkeiten abhängig von den Besonderheiten des Helden auf"""
    gruppen = ['Kulturkunde', 'Geländekunde', 'Ortskenntnis', 'Spezialisierungen']
    if 'Vollzauberer' in besonderheiten and besonderheiten['Vollzauberer']:
        gruppen.append('Große Meditation')
    if 'Geweihter' in besonderheiten and besonderheiten['Geweihter']:
        gruppen.append('Karmalqueste')
    gruppen.append('')
    return gruppen


class Talentblatt(Heldenblatt):
    """Druckklasse für den Talentbogen"""

    hintergrund = (resource_filename(__name__, 'data/img/talentblatt.jpg'), 0, 0, 210, 297)

    def _set_config(self, **kwd):
        # Konstante Abstände und Längen
        self.rand_links = 12
        self.zeilen_w = 92
        self.zeilen_seitenabstand = 0.5
        self.oben_links = {'links': (12, 35), 'rechts': (106.5, 35)}

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
        self.zeilentitel_kopfabstand = 2 * self.zeilen_h - self.zeilentitel_h

        # Konfiguration für die Zeilenfelder
        self.zeilentitelfelder = {
            'at/pa': dict(titel='at/pa', weite=2 * self.zeilen_atpa_w, fontsize=self.zeilentitel_fontsize_neben,
                          style='B', align='C', linie=True),
            'be': dict(titel='be', weite=self.zeilen_be_kom_w, fontsize=self.zeilentitel_fontsize_neben,
                       style='B', align='C', linie=True),
            'kom': dict(titel='kom', weite=self.zeilen_be_kom_w, fontsize=self.zeilentitel_fontsize_neben,
                        style='B', align='C', linie=True),
            'taw': dict(titel='taw', weite=2 * self.zeilen_taw_w - 0.5, fontsize=self.zeilentitel_fontsize_neben,
                        style='B', align='C'),
            # Mit dynamischer Breite (Inline-Felder)
            'name': dict(titel='name', fontsize=self.zeilentitel_fontsize_haupt, style='B', align='L',
                         font=config.TITEL_FONT),
            'schwierigkeit': dict(titel='schwierigkeit', fontsize=self.zeilentitel_fontsize_neben, style='I',
                                  align='L', font=config.FONT),
        }
        self.zeilenfelder = {
            'se': dict(titel='se', weite=self.zeilen_se_w, fontsize=self.zeilen_fontsize, linie=True),
            'at': dict(titel='at', weite=self.zeilen_atpa_w, fontsize=self.zeilen_fontsize, style='B', align='C',
                       linie=True),
            'pa': dict(titel='pa', weite=self.zeilen_atpa_w, fontsize=self.zeilen_fontsize, style='B', align='C',
                       linie=True),
            'be': dict(titel='be', weite=self.zeilen_be_kom_w, fontsize=self.zeilen_fontsize, style='B', align='C',
                       linie=True),
            'kom': dict(titel='kom', weite=self.zeilen_be_kom_w, fontsize=self.zeilen_fontsize, style='B', align='C',
                        linie=True),
            'taw': dict(titel='taw', weite=self.zeilen_taw_w, fontsize=self.zeilen_fontsize, style='B', align='C',
                        linie=True),
            'taw_leer': dict(titel='taw_leer', weite=self.zeilen_taw_w, fontsize=self.zeilen_fontsize, style='B'),
            # Mit dynamischer Breite (Inline-Felder)
            'talent': dict(titel='talent', fontsize=self.zeilen_fontsize, style='B', align='L', font=config.FONT),
            'probe': dict(titel='probe', fontsize=self.zeilen_fontsize, style='I', align='L', font=config.FONT),
            'schwierigkeit': dict(titel='schwierigkeit', fontsize=self.zeilen_fontsize, style='I', align='L',
                                  font=config.FONT),
            'hinweis': dict(titel='hinweis', fontsize=self.zeilen_fontsize, style='I', align='L', font=config.FONT),
        }
        self.feldreihenfolge = [
            'se', 'talent', 'probe', 'schwierigkeit', 'hinweis', 'at', 'pa', 'be', 'kom', 'taw', 'taw_leer'
        ]
        return

###
# Zählmethoden
###

    def zaehle_platz_pro_seite(self, held, verteilung, leerzeilen={}, sonderfertigkeiten_sind='links'):
        """Berechnet die Anzahl verbleibender Zeilen je Seite zurück"""
        platz = {'links': -99, 'rechts': -99}
        for seite, gruppen in verteilung.iteritems():
            anzahlen = dict([(gruppe, self.zaehle_talentblock_zeilen(held, gruppe) + leerzeilen[gruppe])
                             for gruppe in gruppen])
            anzahlen['Gruppen'] = len(gruppen) * 2
            if sonderfertigkeiten_sind == seite:
                anzahlen['Sonderfertigkeiten'] = self.zaehle_sonderfertigkeiten_zeilen(held['Sonderfertigkeiten'],
                                                                                       held['Besonderheiten']) + 2
#            print("Seite %s: Summe: %d, Anteile %s" % (seite, sum(anzahlen.values()), anzahlen))
            platz[seite] = math.floor(250.0 / self.zeilen_h) - sum(anzahlen.values())
        return platz

    def zaehle_talentblock_zeilen(self, held, gruppe):
        """Zählt die benötigten Zeilen eines Talentgruppenblocks"""
        anzahl = len(held['Talente'][gruppe])
        for talent, talentobj in Talentgruppe.alle()[gruppe].talente.iteritems():
            if talent not in held['Talente'][gruppe] and talentobj.ist_basis:
                anzahl += 1
        return anzahl

    def zaehle_sonderfertigkeiten_zeilen(self, sonderfertigkeiten, besonderheiten):
        """Zählt die benötigte Anzahl Zeilen des Sonderfertigkeitenblocks"""
        self.pdf.set_font(family=config.FONT, style='', size=self.zeilen_fontsize)
        verfuegbare_weite = self.zeilen_w - 2 * self.zeilen_seitenabstand
        gruppen = sonderfertigkeiten_gruppen(besonderheiten)
        anzahl = 0
        for gruppe in gruppen:
            titel = "%s: " % gruppe
            zeile = []
            for sf in sonderfertigkeiten:
                if self.pdf.get_string_width(titel + ', '.join(zeile + [unicode(sf)])) > verfuegbare_weite:
                    anzahl += 1
                    titel = ''
                    zeile = [unicode(sf)]
            anzahl += 1
        return anzahl + 1  # Leerzeile drunter

###
# Druckmethoden
###

    def drucke_attributleiste(self, attribute):
        """Druckt die Attribute in die Kopfleiste"""
        self.pdf.set_font(family=config.TITEL_FONT, style='B', size=self.kopfleiste_fontsize)
        self.pdf.set_left_margin(self.rand_links)
        for attr in config.attribute[0:8]:
            self.pdf.cell(self.attribute_w, self.attribute_h, "%s: %d" % (attr, attribute[attr]), align='C')
        self.pdf.cell(self.attribute_dummy_w, self.attribute_h, '')
        self.pdf.cell(self.attribute_be_w, self.attribute_h, "BE: %d" % attribute['BE'])
        return

    def drucke_blatt(self, held):
        """Druckt die komplette Talentblatt"""
        seiten = dict(config.seiten2gruppen)
        leerzeilen = self.erweitere_leerzeilen(held, seiten)
        self.drucke_attributleiste(held['Attribute'])
        self.pdf.set_y(35)
        self.drucke_sonderfertigkeiten(held['Sonderfertigkeiten'], held['Besonderheiten'])
        for gruppen in seiten.itervalues():
            for gruppe in gruppen:
                self.drucke_talentblock(gruppe, held['Talente'][gruppe], leerzeilen[gruppe])
            self.pdf.set_y(35)
            self.pdf.set_left_margin(106)

    def drucke_sonderfertigkeiten(self, sonderfertigkeiten, besonderheiten={}):
        """Druckt den Block von Sonderfertigkeiten"""
        self.pdf.set_font(family=config.FONT, style='B', size=self.zeilentitel_fontsize_haupt)
        links = self.pdf.get_x() + self.zeilen_seitenabstand
        rechts = self.pdf.get_x() + self.zeilen_w - self.zeilen_seitenabstand
        # Überschrift
        self.drucke_zeile({'name': 'Sonderfertigkeiten (Allgemein)'}, standardzeile=False)

        # Zeilen abarbeiten
        gruppen = sonderfertigkeiten_gruppen(besonderheiten)
        self.pdf.set_font(family=config.FONT, style='', size=self.zeilen_fontsize)
        for gruppe in gruppen:
            sonderfertigkeiten.setdefault(gruppe, {})  # Leere Gruppen voraussetzen
            zeile = []
            titel = gruppe and gruppe + ': ' or ''
            for sf in sonderfertigkeiten[gruppe]:
                sf = unicode(sf)
                if self.pdf.get_string_width(titel + ', '.join(zeile + [sf])) <= self.zeilen_w:
                    zeile.append(sf)
                else:
                    # Zeile schon zu voll -> Rausschreiben und neue Zeile beginnen.
                    self.pdf.cell(self.zeilen_w, self.zeilen_h, titel + ', '.join(zeile))
                    self.pdf.line(links, self.pdf.get_y() + self.zeilen_h, rechts, self.pdf.get_y() + self.zeilen_h)
                    self.pdf.ln(self.zeilen_h)
                    zeile = [sf]
                    titel = ''
            # Zeile Rausschreiben
            self.pdf.cell(self.zeilen_w, self.zeilen_h, titel + ', '.join(zeile))
            self.pdf.line(links, self.pdf.get_y() + self.zeilen_h, rechts, self.pdf.get_y() + self.zeilen_h)
            self.pdf.ln(self.zeilen_h)
        # Leerzeile
        self.pdf.ln(self.zeilen_h)
        self.pdf.image(resource_filename(__name__, 'data/img/line-01.png'), self.pdf.get_x(), self.pdf.get_y(),
                       self.zeilen_w + 0.5, 1)
        return

    def drucke_talentblock(self, titel, zeilen, leerzeilen=0):
        """Druckt den Block einer kompletten Talentgruppe"""
        alle = Talentgruppe.alle()
        self.drucke_zeile(alle[titel].get_titelfelder(), standardzeile=False)
        for talent, talentobj in alle[titel].talente.iteritems():
            if talent not in zeilen:
                if talentobj.ist_basis:
                    zeilen[talent] = {'taw': 0}
                else:
                    continue
            d = alle[titel].talente[talent].get_print_dict(**zeilen[talent])
            self.drucke_zeile(d)
        for _ in xrange(leerzeilen):
            self.drucke_zeile(d, leerzeile=True)


###
# Weitere hilfsmethoden
###

    def erweitere_leerzeilen(self, held, seiten):
        """Erweitert die Talentgruppenblöcke schrittweise um Leerzeilen um die Seite auszufüllen"""
        gruppen = config.gruppen
        alle = Talentgruppe.alle()
        leerzeilen = {}
        for gruppe in gruppen:
            leerzeilen[gruppe] = 0
        zeiger = 0
        seite = None
        # Platz mit Leerzeilen auffüllen
        while True:
            platz = self.zaehle_platz_pro_seite(held, seiten, leerzeilen)
            if platz['links'] <= 0 and platz['rechts'] <= 0:
                break
            # Gruppe zum Leerzeilen erhöhen suchen
            while True:
                zeiger = zeiger % len(gruppen)
                gruppe = gruppen[zeiger]
                # bereits "volle" Gruppen abfangen - nicht mehr Leerzeilen vorsehen als die Gruppe bietet!
                if len(held['Talente'][gruppe]) + leerzeilen[gruppe] >= len(alle[gruppe].talente):
                    zeiger += 1
                    continue
                if gruppe in seiten['links']:
                    seite = 'links'
                else:
                    seite = 'rechts'
                if platz[seite] > 0:
                    leerzeilen[gruppe] += 1
                    zeiger += 1
                    break
                else:
                    zeiger += 1
        return leerzeilen
