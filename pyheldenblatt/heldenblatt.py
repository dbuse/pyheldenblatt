# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

from builtins import object

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
        bottomline = (x() + self.zeilen_seitenabstand, y() + height + headspace,
                      x() + self.zeilen_w - self.zeilen_seitenabstand, y() + height + headspace)

        # configure fields (build ZeilenFelder objects and detemine width of in-line fields)
        fields = list(configure_fields(zeilenfelder, template, height, self.pdf, x(), y()))
        # insert filller
        fields_width = sum(field.weite for field in fields)
        filler_pos = sum(1 for field in fields if not field.linie) + standardzeile
        fillwidth = self.zeilen_w - fields_width + self.zeilen_seitenabstand
        for i, field in enumerate(fields):
            if i >= filler_pos and field.linie:
                field.linie = (field.linie[0] + fillwidth, field.linie[1], field.linie[2] + fillwidth, field.linie[3])
        print("Insert filler at {} of {}".format(filler_pos, len(fields)))
        filler_xmax = sum(field.weite for field in fields[:filler_pos]) + fillwidth
        filler = ZeilenFeld(weite=fillwidth, fontsize=self.zeilen_fontsize, titel='filler', text='',
                            linie=(x() + filler_xmax, y(), x() + filler_xmax, y() + height))
        fields.insert(filler_pos, filler)
        # actually print line
        return print_line(self.pdf, fields, height, bottomline, headspace)

    def drucke_zeile(self, zeilenfelder={}, leerzeile=False, standardzeile=True, **kwd):
        """Konfiguriert und druckt dann eine Talentzeile oder deren Titel"""
        # return self.print_line(zeilenfelder, leerzeile, standardzeile)  # TODO: Continue with this
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
        # Felder und Begrenzungslinien Drucken
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


def preprocess_field_text(content, name, has_width):
    if not has_width:
        if name in ('probe', 'schwierigkeit'):
            return ' ({}) '.format(content)
        elif name in ('hinweis', ):
            return ' [{}] '.format(content) if content else ' '
    return '{}'.format(content)


def configure_fields(fields, templates, height, pdf, x, y):
    for name, field in fields.items():
        if field is None:
            continue  # skip completely emtpty fields
        if name not in templates:
            raise KeyError("Zeilenfeld {} has no template!".format(name))

        field_dict = templates[name].copy()
        field_dict['text'] = preprocess_field_text(field, name, 'weite' in field_dict)
        if 'weite' not in field_dict:  # inline field with dynamic width
            pdf.set_font(family=field_dict['font'], style=field_dict['style'], size=field_dict['fontsize'])
            field_dict['weite'] = pdf.get_string_width(field_dict['text'])
        else:
            field_dict['linie'] = (x + field_dict['weite'], y, x + field_dict['weite'], y + height)
        yield ZeilenFeld(**field_dict)
        x += field_dict['weite']


def print_line(pdf, fields, height, bottomline, headspace=0):
    """print a generic pre-configured talent line"""
    # add addtional headspace (e.g., for title lines)
    pdf.ln(headspace)
    # draw horizontal line below)
    pdf.line(*bottomline)
    # print fields and vertical lines
    print('Neue Zeile, headspace: {}, height: {}'.format(headspace, height))
    for nr, field in enumerate(fields):
        pdf.set_font(family=field.font, style=field.style, size=field.fontsize)
        pdf.cell(field.weite, height, field.text, align=field.align, border=0)
        if field.linie and nr < len(fields) -1:
            print("Vertical Line for {}: {}".format(field.titel, field.linie))
            pdf.line(*field.linie)
    # complete by performing line break
    pdf.ln(height)
