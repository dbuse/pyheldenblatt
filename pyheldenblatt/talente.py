# -*- coding: utf-8 -*-
'''
Created on 18.07.2012

@author: dom
'''
from __future__ import unicode_literals, print_function, absolute_import

import codecs
from collections import OrderedDict

from . import config


class BE(object):

    def __init__(self, regel):
        self.regel = regel

    def __str__(self):
        return self.regel.replace('*', 'x').replace('0', '-')

    def __call__(self, BE):
        return eval(self.regel, None, {'BE': BE})


class Talentgruppe(object):

    alle_talente = None

    def __init__(self, name, schwierigkeit, be_komp=None, at_pa=None):
        self.name = name
        self.schwierigkeit = schwierigkeit
        self.talente = OrderedDict()
        self.be_komp = be_komp
        self.at_pa = at_pa

    def setze_talente(self, liste):
        for talent in liste:
            self.talente[talent.name] = talent

    def get_titelfelder(self):
        titelfelder = OrderedDict()
        titelfelder['name'] = self.name
        titelfelder['schwierigkeit'] = self.schwierigkeit
        if self.at_pa:
            titelfelder['at/pa'] = "AT/PA"
        if self.be_komp:
            titelfelder['be'] = self.be_komp
        titelfelder['taw'] = "TaW"
        return titelfelder

    @classmethod
    def Kampf(cls):
        kampf = cls('Kampf', None, 'BE', True)
        kampf.setze_talente([
            KampfTalent('Anderthalbhänder', kampf, BE('BE-2'), 'E'),
            ATKampfTalent('Armbrust', kampf, BE('BE-5'), 'C'),
            ATKampfTalent('Belagerungswaffen', kampf, BE('0'), 'D'),
            ATKampfTalent('Blasrohr', kampf, BE('BE-5'), 'D'),
            ATKampfTalent('Bogen', kampf, BE('BE-3'), 'E'),
            ATKampfTalent('Diskus', kampf, BE('BE-2'), 'D'),
            KampfTalent('Dolche', kampf, BE('BE-1'), 'D', ist_basis=True),
            KampfTalent('Fechtwaffen', kampf, BE('BE-1'), 'E'),
            KampfTalent('Hiebwaffen', kampf, BE('BE-4'), 'D', ist_basis=True),
            KampfTalent('Infanteriewaffen', kampf, BE('BE-3'), 'D'),
            KampfTalent('Kettenstäbe', kampf, BE('BE-1'), 'E'),
            KampfTalent('Kettenwaffen', kampf, BE('BE-3'), 'D'),
            ATKampfTalent('Lanzenreiten', kampf, BE('0'), 'E'),
            ATKampfTalent('Peitsche', kampf, BE('BE-1'), 'E'),
            KampfTalent('Raufen', kampf, BE('BE'), 'C', ist_basis=True),
            KampfTalent('Ringen', kampf, BE('BE'), 'D', ist_basis=True),
            KampfTalent('Säbel', kampf, BE('BE-2'), 'D', ist_basis=True),
            ATKampfTalent('Schleuder', kampf, BE('BE-2'), 'E'),
            KampfTalent('Schwerter', kampf, BE('BE-2'), 'E'),
            KampfTalent('Speere', kampf, BE('BE-3'), 'D'),
            KampfTalent('Stäbe', kampf, BE('BE-2'), 'D'),
            ATKampfTalent('Wurfbeile', kampf, BE('BE-2'), 'D'),
            ATKampfTalent('Wurfmesser', kampf, BE('BE-3'), 'C', ist_basis=True),
            ATKampfTalent('Wurfspeere', kampf, BE('BE-2'), 'C'),
            KampfTalent('Zweihandflegel', kampf, BE('BE-3'), 'D'),
            KampfTalent('Zweihand-Hiebwaffen', kampf, BE('BE-3'), 'D'),
            KampfTalent('Zweihandschwerter/-säbel', kampf, BE('BE-2'), 'E'),
        ])
        return kampf

    @classmethod
    def Koerper(cls):
        koerper = cls('Körper', 'D', 'BE')
        koerper.setze_talente([
            BETalent('Akrobatik', 'MU·GE·KO', koerper, BE('BE*2')),
            BETalent('Athletik', 'MU·KO·KK', koerper, BE('BE*2'), ist_basis=True),
            BETalent('Fliegen', 'MI·IN·GE', koerper, BE('BE')),
            BETalent('Gaukeleien', 'MU·CH·FF', koerper, BE('BE*2')),
            BETalent('Klettern', 'MU·GE·KK', koerper, BE('BE*2'), ist_basis=True),
            BETalent('Körperbeherrschung', 'MU·IN·GE', koerper, BE('BE*2'), ist_basis=True),
            BETalent('Reiten', 'CH·GE·KK', koerper, BE('BE-2')),
            BETalent('Schleichen', 'MU·IN·GE', koerper, BE('BE'), ist_basis=True),
            BETalent('Schwimmen', 'GE·KO·KK', koerper, BE('BE*2'), ist_basis=True),
            BETalent('Selbstbeherrschung', 'MU·KO·KK/MU·KL', koerper, BE('0'), ist_basis=True),
            BETalent('Sich Verstecken', 'MU·IN·GE', koerper, BE('BE-2'), ist_basis=True),
            BETalent('Singen', 'IN·CH·CH/KO', koerper, BE('BE-3'), ist_basis=True),
            BETalent('Sinnenschärfe', 'KL·IN·IN/FF', koerper, BE('0'), ist_basis=True),
            BETalent('Skifahren', 'GE·GE·KO', koerper, BE('BE-2')),
            BETalent('Stimmen Immitieren', 'KL·IN·CH', koerper, BE('BE-4')),
            BETalent('Tanzen', 'CH·GE·GE', koerper, BE('BE*2'), ist_basis=True),
            BETalent('Taschendiebstahl', 'MU·IN·FF', koerper, BE('BEx2')),
            BETalent('Zechen', 'IN·KO·KK', koerper, BE('0'), ist_basis=True),
        ])
        return koerper

    @classmethod
    def Gesellschaft(cls):
        gesellschaft = cls('Gesellschaft', 'B')
        gesellschaft.setze_talente([
            StandardTalent('Betören', 'IN·CH·CH', gesellschaft),
            StandardTalent('Etikette', 'KL·IN·CH', gesellschaft),
            StandardTalent('Gassenwissen', 'KL·IN·CH', gesellschaft),
            StandardTalent('Lehren', 'KL·IN·CH', gesellschaft),
            StandardTalent('Menschenkenntnis', 'KL·IN·CH', gesellschaft, ist_basis=True),
            StandardTalent('Schauspielerei', 'MU·KL·CH', gesellschaft),
            StandardTalent('Schriftlicher Ausdruck', 'KL·IN·IN', gesellschaft),
            StandardTalent('Sich Verkleiden', 'MU·CH·GE', gesellschaft),
            StandardTalent('Überreden', 'MU·IN·CH', gesellschaft, ist_basis=True),
            StandardTalent('Überzeugen', 'KL·IN·CH', gesellschaft),
        ])
        return gesellschaft

    @classmethod
    def Natur(cls):
        natur = cls('Natur', 'B')
        natur.setze_talente([
            StandardTalent('Fährtensuchen', 'KL·IN·IN/KO', natur, ist_basis=True),
            StandardTalent('Fallenstellen', 'KL·KL·FF', natur),
            StandardTalent('Fesseln/Entfesseln', 'FF·GE·KK', natur),
            StandardTalent('Fischen/Angeln', 'IN·FF·KK', natur),
            StandardTalent('Orientierung', 'KL·IN·IN', natur, ist_basis=True),
            StandardTalent('Wettervorhersage', 'KL·IN·IN', natur),
            StandardTalent('Wildnisleben', 'IN·GE·KO', natur, ist_basis=True),
        ])
        return natur

    @classmethod
    def Wissen(cls):
        wissen = cls('Wissen', 'B')
        wissen.setze_talente([
            StandardTalent('Anatomie', 'MU·KL·FF', wissen),
            StandardTalent('Baukunst', 'KL·KL·FF', wissen),
            StandardTalent('Brett-/Kartenspiel', 'KL·KL·IN', wissen),
            StandardTalent('Geographie', 'KL·KL·IN', wissen),
            StandardTalent('Geschichtswissen', 'KL·KL·IN', wissen),
            StandardTalent('Gesteinskunde', 'KL·IN·FF', wissen),
            StandardTalent('Götter/Kulte', 'KL·KL·IN', wissen, ist_basis=True),
            StandardTalent('Heraldik', 'KL·KL·IN/FF', wissen),
            StandardTalent('Hüttenkunde', 'KL·IN·KO', wissen),
            StandardTalent('Kriegskunst', 'MU·KL·CH', wissen),
            StandardTalent('Kryptographie', 'KL·KL·IN', wissen),
            StandardTalent('Magiekunde', 'KL·KL·IN', wissen),
            StandardTalent('Mechanik', 'KL·KL·FF', wissen),
            StandardTalent('Pflanzenkunde', 'KL·IN·FF', wissen),
            StandardTalent('Philosophie', 'KL·KL·IN', wissen),
            StandardTalent('Rechnen', 'KL·KL·IN', wissen, ist_basis=True),
            StandardTalent('Rechtskunde', 'KL·KL·IN', wissen),
            StandardTalent('Sagen/Legenden', 'KL·IN·CH', wissen, ist_basis=True),
            StandardTalent('Schätzen', 'KL·IN·IN', wissen),
            StandardTalent('Sprachenkunde', 'KL·KL·IN', wissen),
            StandardTalent('Staatskunst', 'KL·IN·CH', wissen),
            StandardTalent('Sternkunde', 'KL·KL·IN', wissen),
            StandardTalent('Tierkunde', 'MU·KL·IN', wissen),
        ])
        return wissen

    @classmethod
    def Handwerk(cls):
        handwerk = cls('Handwerk', 'B')
        handwerk.setze_talente([
            StandardTalent('Abrichten', 'MU·IN·CH', handwerk),
            StandardTalent('Ackerbau', 'IN·FF·KO', handwerk),
            StandardTalent('Alchimie', 'MU·KL·FF', handwerk),
            StandardTalent('Bergbau', 'IN·KO·KK', handwerk),
            StandardTalent('Bogenbau', 'KL·IN·FF', handwerk),
            StandardTalent('Boote Fahren', 'GE·KO·KK', handwerk),
            StandardTalent('Brauer', 'KL·FF·KK', handwerk),
            StandardTalent('Drucker', 'KL·FF·KK', handwerk),
            StandardTalent('Fahrzeug Lenken', 'IN·CH·FF', handwerk),
            StandardTalent('Falschspiel', 'MU·CH·FF', handwerk),
            StandardTalent('Feinmechanik', 'KL·FF·FF', handwerk),
            StandardTalent('Feuersteinbearbeitung', 'KL·FF·FF', handwerk),
            StandardTalent('Fleischer', 'KL·FF·KK', handwerk),
            StandardTalent('Gerber/Kürschner', 'KL·FF·KO', handwerk),
            StandardTalent('Glaskunst', 'FF·FF·KO', handwerk),
            StandardTalent('Grobschmied', 'FF·KO·KK', handwerk),
            StandardTalent('Handel', 'KL·IN·CH', handwerk),
            StandardTalent('Hauswirtschaft', 'IN·CH·FF', handwerk),
            StandardTalent('Heilkunde Gift', 'MU·KL·IN', handwerk),
            StandardTalent('Heilkunde Krankheiten', 'MU·KL·CH', handwerk),
            StandardTalent('Heilkunde Seele', 'IN·CH·CH', handwerk),
            StandardTalent('Heilkunde Wunden', 'KL·CH·FF', handwerk, ist_basis=True),
            StandardTalent('Holzbearbeitung', 'KL·FF·KK', handwerk, ist_basis=True),
            StandardTalent('Instrumentenbauer', 'KL·IN·FF', handwerk),
            StandardTalent('Kartographie', 'KL·KL·FF', handwerk),
            StandardTalent('Kochen', 'KL·IN·FF', handwerk, ist_basis=True),
            StandardTalent('Kristallzucht', 'KL·IN·FF', handwerk),
            StandardTalent('Lederarbeiten', 'KL·FF·FF', handwerk, ist_basis=True),
            StandardTalent('Malen/Zeichnen', 'KL·IN·FF', handwerk, ist_basis=True),
            StandardTalent('Maurer', 'FF·GE·KK', handwerk),
            StandardTalent('Metallguss', 'KL·FF·KK', handwerk),
            StandardTalent('Musizieren', 'IN·CH·FF', handwerk),
            StandardTalent('Schlösser Knacken', 'IN·FF·FF', handwerk),
            StandardTalent('Schnaps Brennen', 'KL·IN·FF', handwerk),
            StandardTalent('Schneidern', 'KL·FF·FF', handwerk, ist_basis=True),
            StandardTalent('Seefahrt', 'FF·GE·KK', handwerk),
            StandardTalent('Seiler', 'FF·FF·KK', handwerk),
            StandardTalent('Steinmetz', 'FF·FF·KK', handwerk),
            StandardTalent('Steinschneider/Juwelier', 'IN·FF·FF', handwerk),
            StandardTalent('Stellmacher', 'KL·FF·KK', handwerk),
            StandardTalent('Stoffe Färben', 'KL·FF·KK', handwerk),
            StandardTalent('Tätowieren', 'IN·FF·FF', handwerk),
            StandardTalent('Töpfern', 'KL·FF·FF', handwerk),
            StandardTalent('Viehzucht', 'KL·IN·KK', handwerk),
            StandardTalent('Webkunst', 'FF·FF·KK', handwerk),
            StandardTalent('Winzer', 'KL·FF·KK', handwerk),
            StandardTalent('Zimmermann', 'KL·FF·KK', handwerk),
        ])
        return handwerk

    @classmethod
    def Sprachen(cls):
        sprachen = cls('Sprachen', None, 'Kom')
        sprachen.setze_talente([
            # Garethi-Familie
            KomplexTalent('Garethi', sprachen, 18, dialekte=['Horathi', 'Bornländisch', 'Brabaci', 'Maraskani',
                                                             'Alberned', 'Andergastisch', 'Charypto', 'Gatamo']),
            KomplexTalent('Bosparano', sprachen, 21),
            KomplexTalent('Aureliani', sprachen, 21),
            KomplexTalent('Zyklopäisch', sprachen, 18),
            # Tulamidya-Familie
            KomplexTalent('Tulamidya', sprachen, 18, dialekte=['Khom-Novadisch', 'Aranisch', 'Mhanadisch-Balahdisch']),
            KomplexTalent('Ur-Tulamidya', sprachen, 21),
            KomplexTalent('Zelemja', sprachen, 18),
            KomplexTalent('Alaani', sprachen, 21),
            KomplexTalent('Zhulchammaqra', sprachen, 15),
            KomplexTalent('Ferkina', sprachen, 16),
            KomplexTalent('Ruuz', sprachen, 18),
            KomplexTalent('Altes Kemi', sprachen, 18),
            KomplexTalent('Rabensprache', sprachen, 15),
            # Thorwal-Familie
            KomplexTalent('Thorwalsch', sprachen, 18, dialekte=['Gjalskisch', 'Fjarningsch']),
            KomplexTalent('Hjaldingsch', sprachen, 18),
            # Elfische Sprachen
            KomplexTalent('Isdira', sprachen, 21),
            KomplexTalent('Asdharia', sprachen, 24, 'B'),
            # Zwergische Sprachen
            KomplexTalent('Rogolan', sprachen, 21),
            KomplexTalent('Angram', sprachen, 21),
            # Orkische Sprachen
            KomplexTalent('Ologhaijan', sprachen, 15),
            KomplexTalent('Oloarkh', sprachen, 10),
            # Risso-Sprachen
            KomplexTalent('Mahrisch', sprachen, 20),
            KomplexTalent('Rissoal', sprachen, 20),
            # Einzelne Sprachen
            KomplexTalent('Drachisch', sprachen, 21),
            KomplexTalent('Goblinisch', sprachen, 12),
            KomplexTalent('Grolmisch', sprachen, 17),
            KomplexTalent('Koboldisch', sprachen, 15),
            KomplexTalent('Molochisch', sprachen, 17),
            KomplexTalent('Neckergesang', sprachen, 18),
            KomplexTalent('Nujuka', sprachen, 15),
            KomplexTalent('Rssahh', sprachen, 18),
            KomplexTalent('Trollisch', sprachen, 15),
            KomplexTalent('Waldmenschen-Sprache', sprachen, 15, dialekte=['Mohisch', 'Tocamuyac', 'Puka-Puka']),
            KomplexTalent("Z'Lit", sprachen, 17),
            # Geheimsprachen
            KomplexTalent('Zhayad', sprachen, 15),
            KomplexTalent('Atak', sprachen, 12),
            KomplexTalent('Füchsisch', sprachen, 12),
        ])
        return sprachen

    @classmethod
    def Schriften(cls):
        schriften = cls('Schriften', None, 'Kom')
        schriften.setze_talente([
            KomplexTalent('Altes Alaani', schriften, 18),
            KomplexTalent('Altes Kemi', schriften, 21),
            KomplexTalent('Amulashtra', schriften, 11),
            KomplexTalent('Altes Amulashtra', schriften, 17),
            KomplexTalent('Angram', schriften, 21),
            KomplexTalent('Arkanil', schriften, 24, 'C'),
            KomplexTalent('Chrmk', schriften, 18),
            KomplexTalent('Chuchas', schriften, 24, 'B'),
            KomplexTalent('Drakhard-Zinken', schriften, 9),
            KomplexTalent('Drakned-Glyphen', schriften, 15, 'B'),
            KomplexTalent('Geheiligte Glyphen von Unau', schriften, 13),
            KomplexTalent('Gimaril', schriften, 10),
            KomplexTalent('Gjalskisch', schriften, 14),
            KomplexTalent('Hjaldingsche Runen', schriften, 10),
            KomplexTalent('Imperiale Zeichen', schriften, 12),
            KomplexTalent('Isdira/Asdharia', schriften, 18),
            # KomplexTalent('Asdharia',schriften,18)
            KomplexTalent('Kusliker Zeichen', schriften, 10),
            KomplexTalent('Mahrische Glyphen', schriften, 15, 'B'),
            KomplexTalent('Nanduria', schriften, 10),
            KomplexTalent('Rogolan', schriften, 11),
            KomplexTalent('Trollische Raumbilderschrift', schriften, 'C'),
            KomplexTalent('Tulamidya', schriften, 14),
            KomplexTalent('Ur-Tulamidya', schriften, 16),
            KomplexTalent('Zhayad', schriften, 18),
        ])
        return schriften

    @classmethod
    def alle(cls):
        if not cls.alle_talente:
            cls.alle_talente = OrderedDict()
            cls.alle_talente['Kampf'] = cls.Kampf()
            cls.alle_talente['Körper'] = cls.Koerper()
            cls.alle_talente['Gesellschaft'] = cls.Gesellschaft()
            cls.alle_talente['Natur'] = cls.Natur()
            cls.alle_talente['Wissen'] = cls.Wissen()
            cls.alle_talente['Sprachen'] = cls.Sprachen()
            cls.alle_talente['Schriften'] = cls.Schriften()
            cls.alle_talente['Handwerk'] = cls.Handwerk()
        return cls.alle_talente


class Talent(object):
    '''
    Repräsentiert ein allgemeines Talent mit all seinen Eigenheiten
    '''

    def __init__(self, name, probe, kategorie, schwierigkeit=None, ist_basis=False):
        self.name = name
        self.probe = probe
        self.kategorie = kategorie
        if schwierigkeit:
            self.schwierigkeit = schwierigkeit
        else:
            self.schwierigkeit = kategorie.schwierigkeit
        self.ist_basis = ist_basis

    def get_print_dict(self, taw, *arg, **kwd):
        return {
            'se': '',
            'talent': self.name,
            'probe': self.probe,
            'hinweis': '; '.join(
                hinweis
                for hinweis in [
                    'Begabt' if kwd.get('begabt', False) else None,
                    'Unfähig' if kwd.get('unfaehig', False) else None,
                    'Spez: %s' % ','.join(kwd['spezialisierungen']) if kwd.get('spezialisierungen', False) else None,
                ]
                if hinweis is not None
            ),
            'taw': taw,
            'taw_leer': ''
        }

    @staticmethod
    def ist_talent(gesucht):
        for gruppe in Talentgruppe.alle().itervalues():
            if gesucht in gruppe.talente:
                return True
        return Talent.ist_dialekt(gesucht)

    @staticmethod
    def ist_dialekt(gesucht):
        for sprache in Talentgruppe.alle()['Sprachen'].talente.itervalues():
            if gesucht in sprache.dialekte:
                return True
        return False

    @staticmethod
    def sprache_zu_dialekt(dialekt):
        for sprache in Talentgruppe.alle()['Sprachen'].talente.itervalues():
            if dialekt in sprache.dialekte:
                return sprache
        return None

    @staticmethod
    def talent_nach_name(talent):
        for gruppe in Talentgruppe.alle().itervalues():
            if talent in gruppe.talente:
                return gruppe.talente[talent]
        return None

    @staticmethod
    def held_pruefen(held):
        alle = Talentgruppe.alle()
        # Talente
        for gruppenname, gruppe in held['Talente'].iteritems():
            if gruppenname not in alle:
                raise KeyError('Talentgruppe "%s" von Held "%s" ist ungültig!' % (gruppenname, held['Name']))
            for talent in gruppe:
                if not Talent.ist_talent(talent):
                    raise KeyError('Talent "%s" von Held "%s" ist ungültig' % (talent, held['Name']))
        # Zaubertalente, so vorhanden
        if 'Zauber' in held and held['Zauber']:
            allezauber = ZauberTalent.alle()
            for zauber in held['Zauber']:
                if zauber not in allezauber:
                    raise KeyError('Zauber "%s" von Held "%s" ist ungültig' % (zauber, held['Name']))
        return True


class StandardTalent(Talent):
    pass


class BETalent(Talent):

    def __init__(self, name, probe, kategorie, be, schwierigkeit=None, ist_basis=False):
        Talent.__init__(self, name, probe, kategorie, schwierigkeit, ist_basis)
        self.be = be

    def get_print_dict(self, taw, *arg, **kwd):
        d = Talent.get_print_dict(self, taw)
        d['be'] = self.be
        return d


class KomplexTalent(Talent):

    def __init__(self, name, kategorie, komplexitaet, schwierigkeit='A', dialekte=None):
        Talent.__init__(self, name, None, kategorie, schwierigkeit, ist_basis=None)
        self.komplexitaet = komplexitaet
        if not dialekte:
            self.dialekte = []
        else:
            self.dialekte = dialekte
        self.dialekte.append(name)

    def get_print_dict(self, taw, Typ=None, Dialekt=None, *arg, **kwd):
        d = Talent.get_print_dict(self, taw)
        d['kom'] = self.komplexitaet
        if Dialekt:
            d['talent'] = Dialekt
        if Typ is None:
            Typ = 'Sprache kennen' if self.kategorie.name == 'Sprachen' else 'Lesen/Schreiben'
        d['talent'] = ' '.join((Typ, d['talent']))
        d['schwierigkeit'] = self.schwierigkeit
        return d


class KampfTalent(BETalent):

    def __init__(self, name, kategorie, be, schwierigkeit=None, ist_basis=False):
        BETalent.__init__(self, name, None, kategorie, be, schwierigkeit, ist_basis)

    def get_print_dict(self, taw, at=' ', pa=' ', *arg, **kwd):
        d = BETalent.get_print_dict(self, taw)
        d['at'] = at
        d['pa'] = pa
        d['schwierigkeit'] = self.schwierigkeit
        return d


class ATKampfTalent(KampfTalent):

    def get_print_dict(self, taw, *arg, **kwd):
        return KampfTalent.get_print_dict(self, taw, taw, '-', *arg, **kwd)


class ZauberTalent(Talent):

    """Ablage für die Liste aller Zauber"""
    zauberliste = None

    def __init__(self, name, probe, schwierigkeit, zd, kosten, ziel, reichweite, wd, merkmale,
                 seite, lernmods=None, lernen=None, sonderform=None):
        Talent.__init__(self, name, probe, schwierigkeit=schwierigkeit, kategorie="Zauber", ist_basis=False)
        self.zd = zd
        self.kosten = kosten
        self.ziel = ziel
        self.reichweite = reichweite
        self.wd = wd
        self.merkmale = merkmale
        self.merkmal_liste = [config.merkmale[kurz.replace(' ', '')] for kurz in merkmale.split(',')]
        self.seite = seite
        self.lernmods = lernmods
        self.lernen = lernen
        self.sonderform = sonderform

    @staticmethod
    def import_zauber(fname='data/Zauberliste.tsv'):
        labels = ['name', 'probe', 'zd', 'kosten', 'ziel', 'schwierigkeit', 'reichweite', 'wd', 'merkmale', 'seite']
        i = -1
        zauberliste = OrderedDict()
        for line in codecs.open(fname, encoding='utf-8').readlines():
            i += 1
            row = line.split('\t')
            if len(row) != len(labels):
                print("Feldanzahlfehler bei nr %d. '%s' len: %d" % (i, row[0], len(row)))
                continue
            zauberliste[row[0]] = dict([(labels[x], row[x].replace("\n", "")) for x in range(len(labels))])
        return zauberliste

    @classmethod
    def alle(cls, fname='data/Zauberliste.tsv'):
        if not cls.zauberliste:
            roh_liste = cls.import_zauber(fname)
            liste = OrderedDict()
            for zauber, daten in roh_liste.iteritems():
                liste[zauber] = cls(**daten)
            cls.zauberliste = liste
        return cls.zauberliste

    def berechner_lernparameter(self, merkmale=None, begabungen=None, unfaehigkeiten=None, **kwd):
        merkmale = merkmale if merkmale is not None else []
        begabungen = begabungen if begabungen is not None else []
        unfaehigkeiten = unfaehigkeiten if unfaehigkeiten is not None else []

        spalten_wert = config.lernspalten.index(self.schwierigkeit)
        lernmods = []

        if 'hauszauber' in kwd and kwd['hauszauber']:
            lernmods.append('H')
            spalten_wert -= 1
        # Einzelne Begabungen/Unfähigkeiten
        if 'begabt' in kwd and kwd['begabt']:
            lernmods.append('B')
            spalten_wert -= 1
        elif 'unfähig' in kwd and kwd['unfähig']:
            lernmods.append('U')
            spalten_wert += 1
        for merkmal in self.merkmal_liste:
            # Merkmalskenntnisse
            if merkmal in merkmale:
                lernmods.append('m')
                spalten_wert -= 1
            if merkmal in config.gegenelemente and 'Elementar' in merkmale:
                lernmods.append('m')
                spalten_wert -= 1
            # Merkmalskenntnis im Gegenelement => Schlechter lernbar
            # TODO: Elementarharmonisierte Aura nicht implementiert
            if merkmal in config.gegenelemente and config.gegenelemente[merkmal] in merkmale:
                lernmods.append('g')
                spalten_wert += 1
            # Merkmalsbegabungen
            if merkmal in begabungen:
                lernmods.append('b')
                spalten_wert -= 1
            if merkmal in config.gegenelemente and 'Elementar' in begabungen:
                lernmods.append('b')
                spalten_wert -= 1
            # Merkmalsunfähigkeiten
            if merkmal in unfaehigkeiten:
                lernmods.append('u')
                spalten_wert += 1
        # wert der Lernspalte auf exitente Spalten (A+ (=0) bis 'H' (=8)) begrenzen
        begrenzter_spalten_wert = min(len(config.lernspalten) - 1, max(0, spalten_wert))
        spalte = config.lernspalten[begrenzter_spalten_wert]
        return spalte, ''.join(sorted(lernmods))

    def get_print_dict(self, taw, merkmale=None, begabungen=None, *arg, **kwd):
        d = Talent.get_print_dict(self, taw)
        d['zd'] = self.zd
        d['kosten'] = self.kosten
        d['ziel'] = self.ziel
        d['reichweite'] = self.reichweite
        d['wd'] = self.wd
        d['schwierigkeit'] = self.schwierigkeit
        d['merkmale'] = self.merkmale
        d['seite'] = self.seite
        # TODO: Berechnung noch nicht vollständig! Hexalogien und mehrfache Zauber fehlen noch!
        d['lernen'], d['lernmods'] = self.berechner_lernparameter(merkmale, begabungen, **kwd)
        return d
