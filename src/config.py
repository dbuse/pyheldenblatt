# -*- coding: utf-8 -*-
'''
Created on 06.08.2012

@author: joti
'''
from __future__ import unicode_literals
import os.path

# Programm-Spezifisch
inhalt_pfad = '../inhalt'
ausgabe_pfad = os.path.join(inhalt_pfad, 'ausgabe')
eingabe_pfad = os.path.join(inhalt_pfad, 'helden')
cli_description = """
Erzeugt ein PDF aus Helden-Informationen.
Hinweis zur Angabe von Pfaden:
Wird nur der reine Dateiname angegeben (z.B. "held.py"), 
so wird im vorkonfigurierten Ein- bzw. Ausgabeverzeichnis nach der Datei gesucht.
Wenn tatsächlich der aktuelle Pfad durchsucht werden soll, 
muss ein ./ vorangestellt werden (z.B. "./held.py").
"""

# DSA-Spezifisch
attribute=['MU','KL','IN','CH','FF','GE','KO','KK','BE','SO']
basiswerte=['LE','AU','ASP','KAP','MR','INI','AT','PA','FK']
kopfwerte=['Name','Rasse','Kultur','Profession']
aussehen=['Haarfarbe','Augenfarbe','Größe','Gewicht','Aussehen']
gruppen = ['Kampf','Körper','Gesellschaft','Natur','Wissen','Sprachen','Schriften','Handwerk']

merkmale = {
    'Amaz':'Amazeroth', 'Anti':'Antimagie', 'Asfa':'Asfaloth', 'Besw':'Beschwörung', 'Blak':'Blakharaz',
    'Dämo':'Dämonisch', 'Eign':'Eigenschaften', 'Einf':'Einfluss', 'Eis' :'Eis', 'Elem':'Elementar',
    'Erz' :'Erz', 'Feur':'Feuer', 'Form':'Form', 'Geis':'Geisterwesen', 'Heil':'Heilung',
    'Hell':'Hellsicht', 'Herb':'Herbeirufung', 'Herr':'Herrschaft', 'Humu':'Humus', 'Illu':'Illusion',
    'Krft':'Kraft', 'Limb':'Limbus', 'Lolg':'Lolgramoth', 'Luft':'Luft', 'Meta':'Metamagie',
    'Mish':'Mishkara', 'Objk':'Objekt', 'Scha':'Schaden', 'Tele':'Telekinese', 'Temp':'Temporal',
    'Thar':'Thargunitoth', 'Umwe':'Umwelt', 'Vers':'Verständigung', 'Wass':'Wasser',
}
gegenelemente = {
    'Eis'   :'Humus',
    'Erz'   :'Luft',
    'Feuer' :'Wasser',
    'Humus' :'Eis',
    'Luft'  :'Erz',
    'Wasser':'Feuer',    
}

# PDF-Spezifisch
FONT = 'Times'
TITEL_FONT = 'Mason Bold'