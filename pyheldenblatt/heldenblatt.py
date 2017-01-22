# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from builtins import object, str

from collections import OrderedDict

from . import config


class ZeilenFeld(object):

    def __init__(self, titel, weite, fontsize, text='', style='', align='', linie=tuple(), font=config.FONT):
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

    def print_line(self, zeilenfelder={}, leerzeile=False, standardzeile=True, **kwd):
        x, y = self.pdf.get_x, self.pdf.get_y
        # distinguish between standard and header lines
        if standardzeile:
            height = self.zeilen_h
            headspace = 0
            template = self.zeilenfelder
            zeilenfelder = OrderedDict((name, zeilenfelder[name])
                                       for name in self.feldreihenfolge if name in zeilenfelder)
        else:
            height = self.zeilentitel_h
            template = self.zeilentitelfelder
            headspace = self.zeilentitel_kopfabstand

        # line below the text of the line
        bottomline = (x() + self.zeilen_seitenabstand, y() + height,
                      x() + self.zeilen_w - self.zeilen_seitenabstand, y() + height)

        # configure fields (build ZeilenFelder objects and detemine width of in-line fields)
        fields = list(configure_fields(zeilenfelder, template, height, self.pdf))
        fields_width = sum(field.weite for field in fields)
        inline_fields_count = sum(1 for field in fields if field.linie)
        fields.insert(
            inline_fields_count + standardzeile,
            ZeilenFeld(weite=self.zeilen_w - fields_width + standardzeile + self.zeilen_seitenabstand,
                       fontsize=self.zeilen_fontsize, titel='filler', text='', linie=vertical_line(x, y, height))
        )
        return print_line(self.pdf, fields, height, bottomline, headspace)

    def drucke_zeile(self, zeilenfelder={}, leerzeile=False, standardzeile=True, **kwd):
        """Konfiguriert und druckt dann eine Talentzeile oder deren Titel"""
        #return self.print_line(zeilenfelder, leerzeile, standardzeile)  # TODO: Continue with this
        # Höhe der Zeile festlegen und Kopfabstand bei Titelzeilen setzen
        if standardzeile:
            hoehe = self.zeilen_h
            # Zeilenfelder sortieren - nur bei Standardzeilen nötig
            zeilenfelder = OrderedDict((name, zeilenfelder[name])
                                       for name in self.feldreihenfolge
                                       if name in zeilenfelder)
        else:
            self.pdf.ln(self.zeilentitel_kopfabstand)
            hoehe = self.zeilentitel_h
        # Untere Linie ziehen
        self.pdf.line(self.pdf.get_x() + self.zeilen_seitenabstand,
                      self.pdf.get_y() + hoehe,
                      self.pdf.get_x() + self.zeilen_w - self.zeilen_seitenabstand,
                      self.pdf.get_y() + hoehe)
        felder = self.konfiguriere_zeile(zeilenfelder, standardzeile)
        # Felder und begrenzungslinien Drucken
        for feld in felder:
            self.pdf.set_font(family=feld.font, style=feld.style, size=feld.fontsize)
            if leerzeile:
                self.pdf.cell(feld.weite, hoehe, '')
            else:
                # NOTE: format is necessary to be p2/py3 compatible with unicodes
                # NOTE: builtins.str does not work for some reason!
                self.pdf.cell(feld.weite, hoehe, "{}".format(feld.text), align=feld.align)
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
        for name, zeilenfeld in zeilenfelder.items():
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
        return felder


def vertical_line(xfunc, yfunc, height):
    return (xfunc(), yfunc(), xfunc(), yfunc() + height)


def make_fixwidth_field(content, template):
    # normal fixed-width field -- including a vertical line
    return ZeilenFeld(**dict(template, text='{}'.format(content), linie=vertical_line(pdf.get_x, pdf.get_y, height)))


def make_inline_field(content, template, name, height, pdf):
    # preprocess field text
    if name in ('probe', 'schwierigkeit'):
        field_text = ' {} '.format(content)
    elif name in ('hinweis', ):
        field_text = ' [{}] '.format(content) if content else ' '
    else:
        field_text = '{}'.format(field)



def configure_fields(fields, templates, height, pdf):
    for name, field in fields.items():
        if field is None:
            continue  # skip completely emtpty fields
        if name not in templates:
            raise KeyError("Zeilenfeld {} hat kein Template".format(name))

        if 'weite' in templates[name]:
            yield make_fixwidth_field(field, templates[name])
        else:
            # inline field with dynamic width
            pdf.set_font(family=templates[name]['font'], style=templates[name]['style'],
                              size=templates[name]['fontsize'])
            if name in ('probe', 'schwierigkeit'):
                field_text = ' {} '.format(field)
            elif name in ('hinweis', ):
                field_text = ' [{}] '.format(field) if field else ' '
            else:
                field_text = '{}'.format(field)
            width = pdf.get_string_width(field_text)
            yield ZeilenFeld(text=field_text, weite=width, linie=[], **templates[name])


def print_line(pdf, fields, height, bottomline, headspace=0):
    """print a generic pre-configured talent line"""
    # add addtional headspace (e.g., for title lines)
    pdf.ln(headspace)
    # draw horizontal line below)
    pdf.line(*bottomline)
    # print fields and vertical lines
    for field in fields:
        pdf.set_font(family=field.font, style=field.style, size=field.fontsize)
        pdf.cell(field.weite, height, field.text, align=field.align)
        if field.linie:
            pdf.line(*field.linie)
    # complete by performing line break
    pdf.ln(height)
