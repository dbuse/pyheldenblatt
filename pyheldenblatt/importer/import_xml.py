# -*- coding: utf-8 -*-
'''
Created on 06.03.2013

@author: dom
'''
from __future__ import unicode_literals

import xml.etree.ElementTree as ET

from pyheldenblatt.talente import Talent, Talentgruppe, KampfTalent

mappings = {}
mappings['eigenschaften'] = {
    'Mut': 'MU',
    'Klugheit': 'KL',
    'Intuition': 'IN',
    'Charisma': 'CH',
    'Fingerfertigkeit': 'FF',
    'Gewandtheit': 'GE',
    'Konstitution': 'KO',
    'Körperkraft': 'KK',
}
mappings['talente'] = {
    'Geografie': 'Geographie',
    'Zweihandhiebwaffen': 'Zweihand-Hiebwaffen',
    'Sich verstecken': 'Sich Verstecken',
    'Sich verkleiden': 'Sich Verkleiden',
    'Fallen stellen': 'Fallenstellen',
    'Götter und Kulte': 'Götter/Kulte',
    'Sagen und Legenden': 'Sagen/Legenden',
    'Boote fahren': 'Boote Fahren',
    'Fahrzeug lenken': 'Fahrzeug Lenken',
    'Heilkunde: Gift': 'Heilkunde Gift',
    'Heilkunde: Krankheiten': 'Heilkunde Krankheiten',
    'Heilkunde: Seele': 'Heilkunde Seele',
    'Heilkunde: Wunden': 'Heilkunde Wunden',
    'Kartografie': 'Kartographie',
    'Schlösser knacken': 'Schlösser Knacken',
    'Schnaps brennen': 'Schnaps Brennen',
    'Stoffe färben': 'Stoffe Färben',
    'Alt-Imperial/Aureliani': 'Aureliani',
    'Mohisch': 'Waldmenschen-Sprache',
    'Urtulamidya': 'Ur-Tulamidya',
    '(Alt-)Imperiale Zeichen': 'Imperiale Zeichen',
    'Gimaril-Glyphen': 'Gimaril',
}


def import_xml(dateiname):
    tree = ET.parse(dateiname)
    root = tree.getroot()
    held = root.getchildren()[0]

    data = {}
    data['Name'] = held.attrib['name']
    data['Rasse'] = held.find('basis/rasse').attrib['string']
    data['Kultur'] = held.find('basis/kultur').attrib['string']
    data['Profession'] = held.find("./basis/ausbildungen/ausbildung/[@art='Hauptprofession']").attrib['string']
    data['Attribute'] = dict([(tgt, int(held.find("./eigenschaften/eigenschaft[@name='%s']" % key).attrib['value']))
                              for key, tgt in mappings['eigenschaften'].iteritems()])
    # TODO: Aussehen importieren (Geschlecht, Alter, etc.)
    # Wird im XML nicht gesetzt!
    data['Attribute']['BE'] = 0

    data['Basiswerte'] = {}
    data['Basiswerte']['MR'] = None  # @todo: Berechnen

    data['Besonderheiten'] = {}
    data['Besonderheiten']['Vollzauberer'] = held.find('vt/vorteil[@name="Vollzauberer"]') is not None

    data['Sonderfertigkeiten'] = {}
    data['Sonderfertigkeiten']['Kulturkunde'] = [kultur.attrib['name']
                                                 for kultur in held.findall('sf/*[@name="Kulturkunde"]/kultur')]
    data['Sonderfertigkeiten']['Geländekunde'] = [sf.attrib['name'].replace('kundig', '')
                                                   for sf in held.findall('sf/')
                                                   if sf.attrib['name'].endswith('kundig')]
    data['Sonderfertigkeiten']['Ortskenntnis'] = [sf.attrib['name']
                                                  for sf in held.findall('sf/*[@name="Ortskenntnis"]/')]
    data['Sonderfertigkeiten']['Spezialisierungen'] = [sf.attrib['name'].replace("Talentspezialisierung ", "")
                                                       for sf in held.findall('sf/*/spezialisierung/..')]

    # Allgemeine Sonderfertigkeiten fehlen noch!

    data["Talente"] = dict((gruppe, {}) for gruppe in Talentgruppe.alle())
    sprachen = Talentgruppe.Sprachen()
    schriften = Talentgruppe.Schriften()

    # Kampf-Basiswerte bestimmen (werden für Berechnung benötigt)
    at_basis = int(held.find('eigenschaften/*[@name="at"]').attrib['value'])
    pa_basis = int(held.find('eigenschaften/*[@name="pa"]').attrib['value'])

    # Talente bereinigen/mappen und verarbeiten
    for item in held.findall('talentliste/'):
        tn = unicode(item.attrib['name'])
        val = int(item.attrib['value'])
        if tn.startswith("Sprachen kennen"):
            tn = tn.replace("Sprachen kennen ", "")
            if tn in mappings['talente']:
                tn = mappings['talente'][tn]
            t = sprachen.talente[tn]
        elif tn.startswith("Lesen/Schreiben "):
            tn = tn.replace("Lesen/Schreiben ", "")
            if tn in mappings['talente']:
                tn = mappings['talente'][tn]
            t = schriften.talente[tn]
        elif "Ritualkenntnis" in tn:
            continue
        else:
            if tn in mappings['talente']:
                tn = mappings['talente'][tn]
            t = Talent.talent_nach_name(tn)

        data["Talente"][t.kategorie.name][t.name] = {'taw': val}
        if t.__class__ == KampfTalent:
            # Bei Kampftalenten noch AT und PA angeben
            raw_name = item.attrib['name']
            k_item = held.find('kampf/kampfwerte[@name="%s"]' % raw_name)
            at_val = int(k_item.find('./attacke').attrib['value']) - at_basis
            pa_val = int(k_item.find('./parade').attrib['value']) - pa_basis
            data["Talente"][t.kategorie.name][t.name]['at'] = at_val
            data["Talente"][t.kategorie.name][t.name]['pa'] = pa_val
    # Zauber fehlen noch!

    # Fertig
    return data
