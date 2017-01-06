# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

# Nutzbarer Bereich:
# Kopf: 265 * 22,5

import math
from collections import OrderedDict
from pkg_resources import resource_filename

from .heldenblatt import Heldenblatt
from .talente import ZauberTalent
from . import config


class Zauberblatt(Heldenblatt):
    """Druckklasse für den Zauberbogen"""

    orientation = "l"
    """Zauberblatt im Querformat drucken"""

    hintergrund = (resource_filename(__name__, 'data/img/zauberblatt.jpg'), 0, 0, 297, 210)

    def _set_config(self, **kwd):

        # Konstante Abstände
        self.rand_links = 12
        self.zeilen_w = 273
        # Für andere Werte als 0 Verschiebt sich hier noch die Titelzeile!
        self.zeilen_seitenabstand = 0

        # Eigenschaften der Talentzeilen
        self.zeilen_se_w = self.zeilen_fontsize * 0.5
        self.zeilen_probe_w = self.zeilen_fontsize * 2
        self.zeilen_taw_w = self.zeilen_fontsize * 0.75
        self.zeilen_h = self.zeilen_fontsize * self.multiplikator_h
        #  self.zauber_pro_seite = int(144 / self.zeilen_h)
        self.zauber_pro_seite = int(130 / self.zeilen_h)

        # Überschriftenzeile
        self.zeilentitel_kopfabstand = 0
        self.zeilentitel_h = self.zeilen_h * 1.4
        self.zeilentitel_fontsize = self.zeilen_fontsize * 1.25

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
            'Repräsentationen': dict(weite=50, heldenfeld="Repräsentationen", abteil="Magische Sonderfertigkeiten"),
            'Begabungen': dict(weite=95, heldenfeld='Begabungen', abteil='Magische Sonderfertigkeiten'),
            'Merkmale': dict(weite=80, heldenfeld='Merkmale', abteil='Magische Sonderfertigkeiten'),
            'Unfähigkeiten': dict(weite=60, heldenfeld='Unfähigkeiten', abteil='Magische Sonderfertigkeiten'),
        }

        self.zeilentitelfelder = {
            'name': dict(titel='name', style='B', align='L'),
            'probe': dict(titel='probe', weite=self.zeilen_probe_w, style='B', align='C', linie=True),
            'taw': dict(titel='taw', weite=2 * self.zeilen_taw_w, style='B', align='C', linie=True),
            'zd': dict(titel='zd', weite=self.zeilen_fontsize * 2.5, style='B', align='C', linie=True),
            'kosten': dict(titel='kosten', weite=self.zeilen_fontsize * 3, style='B', align='C', linie=True),
            'reichweite': dict(titel='reichweite', weite=self.zeilen_fontsize * 3, style='B', align='C', linie=True),
            'ziel': dict(titel='ziel', weite=self.zeilen_fontsize * 2, style='B', align='C', linie=True),
            'wd': dict(titel='wd', weite=self.zeilen_fontsize * 3, style='B', align='C', linie=True),
            'schwierigkeit': dict(titel='schwierigkeit', weite=self.zeilen_taw_w, style='B', align='C', linie=True),
            'merkmale': dict(titel='merkmale', weite=self.zeilen_fontsize * 4 - self.zeilen_taw_w, style='B',
                             align='C', linie=True),
            'lernmods': dict(titel='lernmods', weite=self.zeilen_taw_w * 2, style='B', align='C', linie=True),
            'lernen': dict(titel='lernen', weite=self.zeilen_taw_w, style='B', align='C', linie=True),
            'seite': dict(titel='seite', weite=self.zeilen_fontsize * 1.5, style='B', align='C'),

        }
        for ztf in self.zeilentitelfelder:
            self.zeilentitelfelder[ztf]['fontsize'] = self.zeilentitel_fontsize
            self.zeilentitelfelder[ztf]['font'] = config.TITEL_FONT

        self.zeilenfelder = {
            'se': dict(titel='se', weite=self.zeilen_se_w, linie=True),
            'talent': dict(titel='talent', style='B', align='L', font=config.FONT),
            'hinweis': dict(titel='hinweis', style='I', align='L', font=config.FONT),
            'probe': dict(titel='probe', weite=self.zeilen_probe_w, style='I', linie=True),
            'taw': dict(titel='taw', weite=self.zeilen_taw_w, style='B', align='C', linie=True),
            'taw_leer': dict(titel='taw_leer', weite=self.zeilen_taw_w, style='B', linie=True),
            'zd': dict(titel='zd', weite=self.zeilen_fontsize * 2.5, style='', linie=True),
            'kosten': dict(titel='kosten', weite=self.zeilen_fontsize * 3, style='', linie=True),
            'reichweite': dict(titel='reichweite', weite=self.zeilen_fontsize * 3, style='', linie=True),
            'ziel': dict(titel='ziel', weite=self.zeilen_fontsize * 2, style='', linie=True),
            'wd': dict(titel='wd', weite=self.zeilen_fontsize * 3, style='', linie=True),
            'schwierigkeit': dict(titel='schwierigkeit', weite=self.zeilen_taw_w, style='B', align='C', linie=True),
            'merkmale': dict(titel='merkmale', weite=self.zeilen_fontsize * 4 - self.zeilen_taw_w, style='I',
                             linie=True),
            'lernmods': dict(titel='lernmods', weite=self.zeilen_taw_w * 2, style='B', align='C', linie=True),
            'lernen': dict(titel='lernen', weite=self.zeilen_taw_w, style='B', align='C', linie=True),
            'seite': dict(titel='seite', weite=self.zeilen_fontsize * 1.5, style='I', align='C'),
        }
        for zf in self.zeilenfelder:
            self.zeilenfelder[zf]['fontsize'] = self.zeilen_fontsize

        self.feldreihenfolge = [
            'se', 'talent', 'hinweis', 'probe', 'taw', 'taw_leer', 'zd', 'kosten', 'reichweite', 'ziel', 'wd',
            'schwierigkeit', 'merkmale', 'lernmods', 'lernen', 'seite']
        return

    def drucke_blatt(self, held):
        anzahl_seiten = int(math.ceil(len(held['Zauber']) / float(self.zauber_pro_seite)))
        zauber_sortiert = sorted(held['Zauber'].keys(), reverse=True)
        for i in xrange(anzahl_seiten):
            if i > 0:
                # FÜr folgende Seiten neue Page mit Hintergrund anlegen
                self.pdf.add_page(orientation=self.orientation)
                self.pdf.image(*self.hintergrund)
            self.drucke_kopfleiste(held)

            # Zauber des Helden sortiert in kleinere Listen zerteilen
            zauberliste = {}
            for _ in xrange(self.zauber_pro_seite):
                try:
                    name = zauber_sortiert.pop()
                except IndexError:
                    break
                zauberliste[name] = held['Zauber'][name]
            self.drucke_zauberliste(zauberliste, held)
        return

    def drucke_kopfleiste(self, held):
        self.pdf.set_font(family=config.FONT, style='B', size=self.kopfleiste_fontsize)
        self.pdf.set_left_margin(self.rand_links)

        zeilen = (
            ['Name', 'Rasse', 'Profession'],
            config.attribute[0:8] + ['MR'],
            ['Repräsentationen', 'Begabungen', 'Merkmale', 'Unfähigkeiten'],
        )

        for felder in zeilen:
            self.pdf.ln(self.kopfleiste_h)
            for feld in felder:
                template = self.kopfleistenfelder[feld]
                if template['abteil']:
                    text = held[template['abteil']].get(template['heldenfeld'], '')
                else:
                    text = held[template['heldenfeld']]
                if isinstance(text, (list, tuple)):
                    text = ', '.join(text)
                if text:
                    self.pdf.cell(template['weite'], self.kopfleiste_h, "%s: %s" % (feld, text))
        self.pdf.ln(15)
        return

    def drucke_zeilentitel(self):
        """Drucke eine Titelzeile in etwas größerer Schrift. Soll auf jeder Seite erneut aufgerufen werden"""
        titel = OrderedDict()
        titel['name'] = 'Zaubername'
        titel['probe'] = 'Probe'
        titel['taw'] = 'ZfW'
        titel['zd'] = 'Zauberd.'
        titel['kosten'] = 'Kosten'
        titel['reichweite'] = 'Reichweite'
        titel['ziel'] = 'Ziel'
        titel['wd'] = 'Wirkungsd.'
        titel['schwierigkeit'] = 'K'
        titel['merkmale'] = 'Merkmale'
        titel['lernmods'] = 'LM'
        titel['lernen'] = 'L'
        titel['seite'] = 'Seite'
        return self.drucke_zeile(titel, standardzeile=False)

    def drucke_zauberliste(self, zauberliste, held):
        """Drucke eine Liste an Zaubern in Tabellenform. Berechnung der Zauber pro Blatt findet *nicht* hier statt!"""
        # Erst noch Kopfzeile Drucken
        self.drucke_zeilentitel()
        # Einzelne Zauber drucken
        alle = ZauberTalent.alle()
        for zauber, zauberobj in alle.iteritems():
            if zauber in zauberliste:
                d = zauberobj.get_print_dict(merkmale=held['Magische Sonderfertigkeiten'].get('Merkmale', []),
                                             begabungen=held['Magische Sonderfertigkeiten'].get('Begabungen', []),
                                             unfaehigkeiten=held['Magische Sonderfertigkeiten'].get('Unfähigkeiten',
                                                                                                    []),
                                             **zauberliste[zauber])
                self.drucke_zeile(d)
        for zauber in zauberliste:
            if zauber not in alle:
                print("Warnung: Unbekannter Zauber:", zauber)
        for _ in xrange(self.zauber_pro_seite - len(zauberliste)):
            self.drucke_zeile(zeilenfelder=d, leerzeile=True)
        return
