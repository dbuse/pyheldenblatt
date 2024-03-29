# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from builtins import str
import xml.etree.ElementTree as ET

from pyheldenblatt.talente import Talent, Talentgruppe, KampfTalent, ZauberTalent

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
mappings['zauber'] = {
    'Accuratum Zaubernadel': 'Accuratum',
    'Applicatus Zauberspeicher': 'Applicatus',
    'Aureolus Güldenglanz': 'Aureolus',
    'Auris Nasus Oculus': 'Auris Nasus',
    'Blitz dich find': 'Blitz',
    'Claudibus Clavistibor': 'Claudibus',
    'Delicioso Gaumenschmaus': 'Delicioso',
    'Duplicatus Doppelbild': 'Duplicatus',
    'Favilludo Funkentanz': 'Favilludo',
    'Flim Flam Funkel': 'Flim Flam',
    'Foramen Foraminor': 'Foramen',
    'Ignorantia Ungesehn': 'Ignorantia',
    'Impersona Maskenbild': 'Impersona',
    'Manifesto Element': 'Manifesto',
    'Menetekel Flammenschrift': 'Menetekel',
    'Pectetondo Zauberhaar': 'Pectetondo',
    'Plumbumbarum schwerer Arm': 'Plumbumbarum',
    'Reflectimago Spiegelschein': 'Reflectimago',
    'Sapefacta Zauberschwamm': 'Sapefacta',
    'Somnigravis tiefer Schlaf': 'Somnigravis',
    'Vocolimbo hohler Klang': 'Vocolimbo',
    'Vogelzwitschern Glockenspiel': 'Vogelzwitschern',
    'Weihrauchwolke Wohlgeruch': 'Weihrauchwolke',
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
                              for key, tgt in mappings['eigenschaften'].items()])
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
        tn = str(item.attrib['name'])
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

    zauberliste = len(held.findall("zauberliste/")) > 0
    if zauberliste:
        data["Zauber"] = dict()
        data["Magische Sonderfertigkeiten"] = {
            "Repräsentationen": [],
            "Merkmale": [],
            "Begabungen": [],
            "Unfähigkeiten": [],
        }
        zauberliste = ZauberTalent.alle()
        for item in held.findall("zauberliste/"):
            zn = str(item.attrib['name'])
            val = str(item.attrib['value'])
            zn = mappings['zauber'].get(zn, zn)

            z = zauberliste[zn]
            data["Zauber"][z.name] = {'taw': val}

            if item.get("hauszauber", False):
                data["Zauber"][z.name]["hauszauber"] = True

        for item in held.findall('vt/vorteil[@name="Begabung für [Merkmal]"]'):
            val = str(item.get("value"))
            data["Magische Sonderfertigkeiten"]["Begabungen"].append(val)

        for item in held.findall('sf/'):
            val = str(item.get("name"))
            if "Merkmalskenntnis" in val:
                data["Magische Sonderfertigkeiten"]["Merkmale"].append(
                    val.replace("Merkmalskenntnis: ", "")
                )
            if "Repräsentation" in val:
                data["Magische Sonderfertigkeiten"]["Repräsentationen"].append(
                    val.replace("Repräsentation: ", "")
                )

    # Fertig
    return data
