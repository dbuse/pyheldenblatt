# -*- coding: utf-8 -*-
'''
Created on 15.04.2016

@author: dbuse
'''

from __future__ import unicode_literals, print_function, absolute_import

from .heldenblatt import Heldenblatt
from . import config


class Hauptblatt(Heldenblatt):

    hintergrund = ('data/img/hauptblatt.jpg', 0, 0, 210, 297)

    def _set_config(self, **kwd):
        return

    def drucke_blatt(self, held):
        """Druckt die komplette Talentblatt"""

        self.drucker_kopfbereich(held)

        # Rand zurücksetzen
        self.pdf.set_left_margin(0)
        return

    def drucker_kopfbereich(self, held):
        self.pdf.set_font(family=config.TITEL_FONT, style='B', size=10)
        self.pdf.set_left_margin(32.5)
        self.pdf.set_y(29)

        felder = ['Name', 'Rasse', 'Kultur', 'Profession']
        for feld in felder:
            self.pdf.cell(70, 7.75, held[feld], border=0)
            self.pdf.ln(7.75)
        return
