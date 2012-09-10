# -*- coding: utf-8 -*-
'''
Created on 06.09.2012

@author: dbuse
'''

from collections import OrderedDict
from heldenblatt import Heldenblatt

def import_zauber(fname='inhalt/Zauberliste.tsv'):
    labels = ['name', 'probe', 'zd', 'kosten', 'ziel', 'schwierigkeit', 'reichweite', 'wirkungsdauer', 'merkmale', 'seite']
    i = -1
    zauberliste = OrderedDict()
    for line in open(fname).readlines():
        i += 1
        row = line.split('\t')
        if len(row) != len(labels):
            print "Feldanzahlfehler bei nr %d. '%s' len: %d" % (i,row[0],len(row))
            continue
        zauberliste[row[0]] = dict([(labels[x],row[x].replace("\n","")) for x in range(len(labels))])
    return zauberliste

class Zauberblatt(Heldenblatt):
    """Druckklasse für den Zauberbogen"""
    
    orientation = "l"
    """Zauberblatt im Querformat drucken"""