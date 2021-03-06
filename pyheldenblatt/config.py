# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import


# Programm-Spezifisch
cli_description = """
Erzeugt ein PDF aus Helden-Informationen.
"""
cli_epilog = """
Ist der Schalter -o nicht gesetzt, wird das pdf neben der Eingabedatei abgelegt
"""

# DSA-Spezifisch
attribute = ['MU', 'KL', 'IN', 'CH', 'FF', 'GE', 'KO', 'KK', 'BE', 'SO']
basiswerte = ['LE', 'AU', 'ASP', 'KAP', 'MR', 'INI', 'AT', 'PA', 'FK']
kopfwerte = ['Name', 'Rasse', 'Kultur', 'Profession']
aussehen = ['Haarfarbe', 'Augenfarbe', 'Größe', 'Gewicht', 'Aussehen']
gruppen = ['Kampf', 'Körper', 'Gesellschaft', 'Natur', 'Wissen', 'Sprachen', 'Schriften', 'Handwerk']

merkmale = {
    'Amaz': 'Amazeroth', 'Anti': 'Antimagie', 'Asfa': 'Asfaloth', 'Besw': 'Beschwörung', 'Blak': 'Blakharaz',
    'Dämo': 'Dämonisch', 'Eign': 'Eigenschaften', 'Einf': 'Einfluss', 'Eis': 'Eis', 'Elem': 'Elementar',
    'Erz': 'Erz', 'Feur': 'Feuer', 'Form': 'Form', 'Geis': 'Geisterwesen', 'Heil': 'Heilung',
    'Hell': 'Hellsicht', 'Herb': 'Herbeirufung', 'Herr': 'Herrschaft', 'Humu': 'Humus', 'Illu': 'Illusion',
    'Krft': 'Kraft', 'Limb': 'Limbus', 'Lolg': 'Lolgramoth', 'Luft': 'Luft', 'Meta': 'Metamagie',
    'Mish': 'Mishkara', 'Objk': 'Objekt', 'Scha': 'Schaden', 'Tele': 'Telekinese', 'Temp': 'Temporal',
    'Thar': 'Thargunitoth', 'Umwe': 'Umwelt', 'Vers': 'Verständigung', 'Wass': 'Wasser',
}
gegenelemente = {
    'Eis': 'Humus',
    'Erz': 'Luft',
    'Feuer': 'Wasser',
    'Humus': 'Eis',
    'Luft': 'Erz',
    'Wasser': 'Feuer',
}

lernspalten = ['A+', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

# Talentblatt-Spezifisch
seiten2gruppen = {
    'links': ['Kampf', 'Körper', 'Gesellschaft'],
    'rechts': ['Natur', 'Wissen', 'Sprachen', 'Schriften', 'Handwerk']
}

# PDF-Spezifisch
FONT = 'Times'
TITEL_FONT = 'Mason Bold'
LEERER_TEXT = 'Unbekannt'
LEERE_ZAHL = 'XX'
