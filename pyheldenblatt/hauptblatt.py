# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

from pkg_resources import resource_filename

from .heldenblatt import Heldenblatt
from . import config


class Hauptblatt(Heldenblatt):

    hintergrund = (resource_filename(__name__, 'data/img/hauptblatt.jpg'), 0, 0, 210, 297)

    def _set_config(self, **kwd):
        return

    def drucke_blatt(self, held):
        """Druckt die komplette Talentblatt"""
        self.drucke_kopfbereich(held)
        self.drucke_erscheinungsbereich(held)

        # Rand zurücksetzen
        self.pdf.set_left_margin(0)
        return

    def drucke_kopfbereich(self, held):
        """Druckt den obsersten Block auf dem Blatt"""
        self.pdf.set_font(family=config.TITEL_FONT, style='B', size=10)
        self.pdf.set_left_margin(32.5)
        self.pdf.set_y(29)

        felder = ['Name', 'Rasse', 'Kultur', 'Profession']
        for feld in felder:
            self.pdf.cell(70, 7.75, held.get(feld, config.LEERER_TEXT), border=0)
            self.pdf.ln(7.75)
        return

    def drucke_erscheinungsbereich(self, held):
        """Druckt den Bereich mit den äußeren Erscheinungsmerkmalen"""
        self.pdf.set_font(family=config.TITEL_FONT, style='B', size=9)
        self.pdf.set_left_margin(35)
        self.pdf.set_y(66.75)

        felder = ['Geschlecht', 'Alter', 'Größe', 'Gewicht', 'Haarfarbe', 'Augenfarbe', 'Aussehen']
        aussehen = held.get('Aussehen', {})
        # TODO: Aussehen mehrzeilig gestalten
        for feld in felder:
            self.pdf.cell(45, 6.45, aussehen.get(feld, config.LEERER_TEXT), border=0)
            self.pdf.ln(6.45)
        return
