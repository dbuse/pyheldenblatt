# -*- coding: utf-8 -*-
from collections import OrderedDict

from . import config


class ZeilenFeld(object):

    def __init__(self, titel, weite, fontsize, text='', style='', align='', linie=False, font=config.FONT):
        self.titel = titel
        self.weite = weite
        self.text = text
        self.style = style
        self.align = align
        self.linie = linie
        self.font = font
        self.fontsize = fontsize

    def __str__(self):
        lst = []
        for attr in ['titel', 'weite', 'text', 'style', 'align', 'linie', 'font', 'fontsize']:
            lst.append("%s: '%s'" % (attr, getattr(self, attr)))
        return ', '.join(lst)


class Heldenblatt(object):
    """Grundklasse für alle Einzelblätter des Heldendokumentes"""

    orientation = "p"
    """Standardmäßig im Hochformat drucken"""

    def __init__(self, pdf, zeilen_fontsize=8, kopfleisten_fonsize=16, multiplikator_h=0.6, **kwd):
        self.pdf = pdf
        self.pdf.set_auto_page_break(auto=False)
        self.pdf.add_page(orientation=self.orientation)
        self.pdf.image(*self.hintergrund)
        # Spezifische Konfiguration setzen

        # Schriftgrößen als Variablen
        self.zeilen_fontsize = zeilen_fontsize
        self.kopfleiste_fontsize = kopfleisten_fonsize
        self.multiplikator_h = multiplikator_h
        self._set_config(**kwd)
        return

    def drucke_zeile(self, zeilenfelder={}, leerzeile=False, standardzeile=True, **kwd):
        """Konfiguriert und druckt dann eine Talentzeile oder deren Titel"""
        # Höhe der Zeile festlegen und Kopfabstand bei Titelzeilen setzen
        if standardzeile:
            hoehe = self.zeilen_h
        else:
            self.pdf.ln(self.zeilentitel_kopfabstand)
            hoehe = self.zeilentitel_h
        # Untere Linie ziehen
        self.pdf.line(self.pdf.get_x() + self.zeilen_seitenabstand,
                      self.pdf.get_y() + hoehe,
                      self.pdf.get_x() + self.zeilen_w - self.zeilen_seitenabstand,
                      self.pdf.get_y() + hoehe)
        if standardzeile:
            # Zeilenfelder sortieren - nur bei Standardzeilen nötig
            zeilenfelder_sortiert = OrderedDict()
            for name in self.feldreihenfolge:
                if name in zeilenfelder:
                    zeilenfelder_sortiert[name] = zeilenfelder[name]
        else:       # Titelzeile:
            zeilenfelder_sortiert = zeilenfelder
        felder = self.konfiguriere_zeile(zeilenfelder_sortiert, standardzeile)
        # Felder und begrenzungslinien Drucken
        for feld in felder:
            self.pdf.set_font(family=feld.font, style=feld.style, size=feld.fontsize)
            if leerzeile:
                self.pdf.cell(feld.weite, hoehe, '')
            else:
                self.pdf.cell(feld.weite, hoehe, unicode(feld.text), align=feld.align)
            if feld.linie and len(zeilenfelder) > 1:
                self.pdf.line(self.pdf.get_x(), self.pdf.get_y(), self.pdf.get_x(), self.pdf.get_y() + hoehe)
        # Zeilenumbruch und fertig!
        return self.pdf.ln(hoehe)

    def konfiguriere_zeile(self, zeilenfelder, standardzeile=True):
        """Stellt eine Konfiguration für eine Talentzeile abhängig von den aktuellen Feldern zum Drucken zusammen"""
        # Passendes Templates-Dictionary wählen
        if standardzeile:
            templates = self.zeilenfelder
        else:
            templates = self.zeilentitelfelder
        # Bei Standardzeilen das SE-Feld nicht vergessen
        pos = 0 + standardzeile
        # Feldgrößen bestimmen und Texte vorbereiten
        felder = []
        for name, zeilenfeld in zeilenfelder.iteritems():
            if zeilenfeld is None:
                # Komplett leere Felder überspringen
                continue
            if name in templates:
                if 'weite' in templates[name]:
                    # Standard-Feld mit fixer Weite
                    felder.append(ZeilenFeld(text=zeilenfeld, **templates[name]))
                else:
                    # Inline-Felder: Größe dynamisch Ausmessen
                    conf = templates[name]
                    self.pdf.set_font(family=conf['font'], style=conf['style'], size=conf['fontsize'])
                    if name in ('probe', 'schwierigkeit'):
                        zeilenfeld = ' (%s) ' % zeilenfeld
                    if name in ('hinweis', ):
                        zeilenfeld = ' [%s] ' % zeilenfeld if zeilenfeld else ' '
                    weite = self.pdf.get_string_width(zeilenfeld)
                    felder.append(ZeilenFeld(text=zeilenfeld, weite=weite, **templates[name]))
                    pos += 1
            else:
                raise KeyError('Zeilenfeld "%s" hat kein Template!' % name)
        # Talentnamen einfügen - nach den Inline-Feldern (darum pos hochzählen)
        weite = self.zeilen_w - sum((feld.weite for feld in felder)) + standardzeile * self.zeilen_seitenabstand
        felder.insert(pos, ZeilenFeld(titel='füller', weite=weite, fontsize=self.zeilen_fontsize, text='', linie=True))
        # print('\n'.join([unicode(feld) for feld in felder]), '\n')
        return felder
