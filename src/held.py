# -*- coding: utf-8 -*-
'''
Created on 05.08.2012

@author: joti
'''
from __future__ import unicode_literals

from talente import Talent
import config


class Held(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

        self.kopfwerte = {}
        self.aussehen = {}
        self.attribute = {}
        self.vorteile = {}
        self.nachteile = {}
        self.sonderfertigkeiten = {}
        self.magischeSonderfertigkeiten = {"Merkmale": [], 'Repräsentationen': [], 'Repräsentationen': []}
        self.basiswerte = {}

        self.kampf = {}
        self.koerper = {}
        self.gesellschaft = {}
        self.natur = {}
        self.wissen = {}
        self.sprachen = {}
        self.schriften = {}
        self.sprachen = {}
        self.handwerk = {}
        self.gaben = {}
        self.completArray = {}

        self.talente = {'Kampf': self.kampf,
                        'Körper': self.koerper,
                        'Gesellschaft': self.gesellschaft,
                        'Natur': self.natur,
                        'Wissen': self.wissen,
                        'Sprachen': self.sprachen,
                        'Schriften': self.schriften,
                        'Handwerk': self.handwerk}

        for attr in config.attribute:
            self.attribute[attr] = 0

        for item in config.aussehen:
            self.aussehen[item] = ''

        for item in config.kopfwerte:
            self.kopfwerte[item] = ""

        for item in config.basiswerte:
            self.basiswerte[item] = 0

    def toArray(self):
        self.completArray['Attribute'] = self.attribute
        self.completArray['Talente'] = self.talente
        self.completArray['Sonderfertigkeiten'] = self.sonderfertigkeiten
        self.completArray['Besonderheiten'] = {}
        self.completArray['Basiswerte'] = self.basiswerte
        self.completArray['Kopfwerte'] = self.kopfwerte
        self.completArray['Aussehen'] = self.aussehen
        self.completArray['Magische Sonderfertigkeiten'] = self.magischeSonderfertigkeiten
        return self.completArray

    def addTalent(self, name, wert):
        name = name.strip()
        if(Talent.ist_talent(name)):
            talent = Talent.talent_nach_name(name)
            if talent is None:
                talent = Talent.sprache_zu_dialekt(name)
            self.talente[talent.kategorie.name][talent.name] = {'taw': wert}
