#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import argparse
import os
import sys
import codecs

sys.path.append(os.path.abspath('../'))

import config
from import_xls import importXLS
from import_xml import import_xml
from heldenblatt import MyFPDF
from talentblatt import Talentblatt
from zauberblatt import Zauberblatt


def lese_parameter():
    # Parser konfigurieren
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datei", help="Datei in dem die Helden-Informationen angegeben sind.")
    parser.add_argument("-f","--format", choices=['ext','xml','xls','py'], default='ext',
                        help="Datei-Format von held-datei.Standard: Auswahl nach Dateiendung ('ext'-Modus)")
    parser.add_argument("-o","--output", help="Ausgabe-Datei")
    parser.description = config.cli_description
    parser.epilog = config.cli_epilog
    args = parser.parse_args()
    
    # Quelldatei bestimmen und prüfen
    if args.datei == os.path.basename(args.datei):
        # Es befindet sich kein Verzeichnis oder ./ am Anfang -> in Inhalt-Verzeichnis verschieben
        quell_datei = os.path.join(config.eingabe_pfad, args.datei)
    else:
        quell_datei = args.datei
    if not os.path.isfile(quell_datei):
        sys.exit("Quell-Datei '%s' nicht gefunden, Abbruch!" % quell_datei)

    # Ausgabe-Datei bestimmen
    if not args.output:
        ausgabe_datei = os.path.splitext(args.datei)[0] + ".pdf"
    else:
        ausgabe_datei = args.output
    if ausgabe_datei == os.path.basename(ausgabe_datei):
        # Es befindet sich kein Verzeichnis oder ./ am Anfang -> in Inhalt-Verzeichnis verschieben
        ausgabe_datei = os.path.join(config.ausgabe_pfad, ausgabe_datei)

    # Import-Modus bestimmen
    if args.format == 'ext':
        import_modus = os.path.splitext(quell_datei)[1][1:]
        if import_modus not in ['ext','xml','xls','py']:
            sys.exit("Kein Import-Modus für Dateityp '%s' erkannt. Versuch es mal mit -f/--format" % import_modus)
    else:
        import_modus = args.format
    return quell_datei, ausgabe_datei, import_modus

def lade_held(quelle, import_modus):
    if import_modus == 'py':
        with codecs.open(quelle, encoding='utf-8') as datei:
            held = eval(datei.read())
    elif import_modus == 'xls':
        held = importXLS(quelle)
    elif import_modus == 'xml':
        held = import_xml(quelle)
    return held

def erzeuge_pdf(held):
    fpdf = MyFPDF(orientation='P', unit='mm', format='A4')
    fpdf.add_font('Mason Regular', '', 'mason.py')
    fpdf.add_font('Mason Bold', 'B', 'masonbold.py')

    talente = Talentblatt(fpdf, zeilen_fontsize=8)
    talente.drucke_blatt(held)
        
    if 'Zauber' in held:
        print "### Achtung: Die Berechnung der Lernspalte ist noch nicht vollständig!"
        print "Mehrfache Zauber (z.B. Adlerschwinge, Arcarnovi) und Hexalogien werden noch NICHT berücksichtigt! ###"
        zauber = Zauberblatt(fpdf)
        zauber.drucke_blatt(held)
    return fpdf
    
def main():
    quelle, ziel, import_modus = lese_parameter()
    print "Lade:", quelle, "Modus", import_modus
    held = lade_held(quelle, import_modus)
    print "Name", held['Name'], ziel
    fpdf = erzeuge_pdf(held)
    fpdf.output(ziel,'F')

if __name__ == "__main__":
    main()