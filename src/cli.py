#!/usr/bin/python2.7
# encoding: utf-8

import argparse
import os
import sys

sys.path.append(os.path.abspath('../'))

from import_xls import importXLS
from import_xml import import_xml

def lese_parameter():
    # Parser konfigurieren
    parser = argparse.ArgumentParser()
    parser.add_argument("datei", help="Datei in dem die Helden-Informationen angegeben sind.")
    parser.add_argument("-f","--format", choices=['ext','xml','xls','py'], default='ext',
                        help="Datei-Format von held-datei.Standard: Auswahl nach Dateiendung ('ext'-Modus)")
    parser.add_argument("-o","--output", help="Ausgabe-Datei")
    args = parser.parse_args()
    
    # Quelldatei prüfen
    quell_datei = os.path.abspath(args.datei)
    if not os.path.isfile(quell_datei):
        sys.exit("Quell-Datei '%s' nicht gefunden, Abbruch!" % quell_datei)
    # Ausgabe-Datei bestimmen
    if not args.output:
        ausgabe_datei = os.path.splitext(quell_datei)[0] + ".pdf"
    # Import-Modus bestimmen
    if args.format == 'ext':
        import_modus = os.path.splitext(quell_datei)[1][1:]
        if import_modus not in ['ext','xml','xls','py']:
            sys.exit("Kein Import-Modus für Dateityp '%s' erkannt. Versuch es mal mit -f/--format" % import_modus)
    else:
        import_modus = args.format
    return quell_datei, ausgabe_datei, import_modus

def lade_held(quelle, import_modus):
    #held = None
    if import_modus == 'py':
        with open(quelle) as datei:
            held = eval(datei.read())
    elif import_modus == 'xls':
        held = importXLS(quelle)
    elif import_modus == 'xml':
        held = import_xml(quelle)
    return held
    
def main():
    quelle, ziel, import_modus = lese_parameter()
    print "Lade:", quelle, "Modus", import_modus
    held = lade_held(quelle, import_modus)
    #print "Name", held['Name']
    

if __name__ == "__main__":
    main()