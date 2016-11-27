#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
TODOs:
- Schriftgröße via Parameter angeben
- Mehrere Talentblatt-Seiten bei zu vielen Talenten
- Berechnung der Leerzeilen berichtigen
    -> manchmal fehlt am Ende eine
    -> Bei sehr kleinen Schriftarten kommt es zu Aufhängern
"""


from __future__ import unicode_literals, print_function, absolute_import

import argparse
import os
import sys
import codecs

from pyheldenblatt import config
from pyheldenblatt.importer.import_xls import importXLS
from pyheldenblatt.importer.import_xml import import_xml
from fpdf import FPDF
from pyheldenblatt.hauptblatt import Hauptblatt
from pyheldenblatt.talentblatt import Talentblatt
from pyheldenblatt.zauberblatt import Zauberblatt


def lese_parameter():
    # Parser konfigurieren
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("datei", help="Datei in dem die Helden-Informationen angegeben sind.")
    parser.add_argument("-f", "--format", choices=['ext', 'xml', 'xls', 'py'], default='ext',
                        help="Datei-Format von held-datei.Standard: Auswahl nach Dateiendung ('ext'-Modus)")
    parser.add_argument("-o", "--output", help="Ausgabe-Datei")
    parser.description = config.cli_description
    parser.epilog = config.cli_epilog
    args = parser.parse_args()

    # Quelldatei bestimmen und prüfen
    quell_datei = args.datei
    if not os.path.isfile(quell_datei):
        sys.exit("Quell-Datei '%s' nicht gefunden, Abbruch!" % quell_datei)

    # Ausgabe-Datei bestimmen
    if not args.output:
        ausgabe_datei = os.path.splitext(quell_datei)[0] + ".pdf"
    else:
        ausgabe_datei = args.output

    # Import-Modus bestimmen
    if args.format == 'ext':
        import_modus = os.path.splitext(quell_datei)[1][1:]
        if import_modus not in ['ext', 'xml', 'xls', 'py']:
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
    fpdf = FPDF(orientation='P', unit='mm', format='A4')
    fpdf.add_font('Mason Regular', '', './data/font/mason.ttf', uni=True)
    fpdf.add_font('Mason Bold', 'B', './data/font/masonbold.ttf', uni=True)

    uebersicht = Hauptblatt(fpdf)
    uebersicht.drucke_blatt(held)

    talente = Talentblatt(fpdf, zeilen_fontsize=8, kopfleisten_fonsize=14)
    talente.drucke_blatt(held)

    if 'Zauber' in held:
        print("### Achtung: Die Berechnung der Lernspalte ist noch nicht vollständig!")
        print("Mehrfache Zauber Merkmals-Unfähigkeiten und Hexalogien werden noch NICHT berücksichtigt! ###")
        zauber = Zauberblatt(fpdf, zeilen_fontsize=6.5, kopfleisten_fonsize=12)
        zauber.drucke_blatt(held)
    return fpdf


def main():
    quelle, ziel, import_modus = lese_parameter()
    print("Lade:", quelle, "Modus", import_modus)
    held = lade_held(quelle, import_modus)
    print("Name", held['Name'], ziel)
    fpdf = erzeuge_pdf(held)
    fpdf.output(ziel, 'F')

if __name__ == "__main__":
    main()
