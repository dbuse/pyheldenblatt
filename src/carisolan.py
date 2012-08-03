# -*- coding: utf-8 -*-
'''
Created on 19.07.2012

@author: dom
'''
held = {
  'Attribute': {
    'MU':12,'KL':14,'IN':15,'CH':12,'FF':13,'GE':12,'KO':13,'KK':11,'BE':0
  },
  'Besonderheiten':{
    'Vollzauberer':True,
  },
  'Sonderfertigkeiten':{
    'Kulturkunde':['Horasreich'],
    'Geländekunde':[],
    'Ortskenntnis':[],
    'Große Meditation': [],
    '':['Nandusgefälliges Wissen']
  },
  'Talente':{
    'Kampf':{
      'Armbrust':{'taw':1},
      'Dolche':{'taw':1,'at':1,'pa':0},
      'Fechtwaffen':{'taw':1,'at':1,'pa':0},
      'Hiebwaffen':{'taw':0,'at':0,'pa':0},
      'Infanteriewaffen':{'taw':3,'at':3,'pa':0},
      'Raufen':{'taw':6,'at':4,'pa':2},
      'Ringen':{'taw':5,'at':1,'pa':4},
      'Säbel':{'taw':2,'at':2,'pa':0},
      'Stäbe':{'taw':6,'at':2,'pa':4},
      'Wurfmesser':{'taw':0},
    },
    'Körper':{
      'Athletik':{'taw':2},
      'Klettern':{'taw':2},
      'Körperbeherrschung':{'taw':3},
      'Schleichen':{'taw':2},
      'Schwimmen':{'taw':1},
      'Selbstbeherrschung':{'taw':3},
      'Sich Verstecken':{'taw':0},
      'Singen':{'taw':3},
      'Sinnenschärfe':{'taw':5},
      'Tanzen':{'taw':4},
      'Zechen':{'taw':2},
    },
    'Gesellschaft':{
      'Betören':{'taw':1},
      'Etikette':{'taw':5},
      'Gassenwissen':{'taw':3},
      'Lehren':{'taw':3},
      'Menschenkenntnis':{'taw':4},
      'Überreden':{'taw':4},
    },
    'Natur':{
      'Fährtensuchen':{'taw':0},
      'Orientierung':{'taw':2},
      'Wildnisleben':{'taw':0},
    },
    'Wissen':{
      'Brettspiel':{'taw':3},
      'Geographie':{'taw':8},
      'Geschichtswissen':{'taw':6},
      'Götter/Kulte':{'taw':6},
      'Magiekunde':{'taw':8},
      'Mechanik':{'taw':10, 'Spezialisierungen':['Magomechanik']},
      'Pflanzenkunde':{'taw':1},
      'Philosophie':{'taw':2},
      'Rechnen':{'taw':7},
      'Rechtskunde':{'taw':3},
      'Sternkunde':{'taw':3},
      'Sagen/Legenden':{'taw':7},
      'Tierkunde':{'taw':2},
    },
    'Sprachen':{
      'Bosparano':{'taw':12},
      'Garethi':{'taw':16, 'Typ':'Muttersprache', 'Dialekt':'Horati'},
      'Isdira':{'taw':8},
      'Tulamidya':{'taw':15, 'Typ':'Lehrsprache'},
      'Ur-Tulamidya':{'taw':6},
    },
    'Schriften':{
      'Isdira/Asdharia':{'taw':6},
      'Kusliker Zeichen':{'taw':10},
      'Tulamidya':{'taw':7},
    },
    'Handwerk':{
      'Ackerbau':{'taw':1},
      'Alchimie':{'taw':2},
      'Heilkunde Wunden':{'taw':0},
      'Holzbearbeitung':{'taw':0},
      'Kochen':{'taw':0},
      'Lederarbeiten':{'taw':1},
      'Malen/Zeichnen':{'taw':4},
      'Schneidern':{'taw':0},
    }
  }
}