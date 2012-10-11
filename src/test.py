# -*- coding: utf-8 -*-
'''
Created on 11.10.2012

Spielplatz ;-)

@author: dbuse
'''

from talente import ZauberTalent
from config import merkmale

def merkmale_finden():
    roh = ZauberTalent.import_zauber()
    merkmal_liste = []
    for name, obj in roh.iteritems():
    #    print "%s: '%s'" % (name, obj['merkmale'].split(","))
        if obj['merkmale']:
            for merkmal_roh in obj['merkmale'].split(','):
                merkmal = merkmal_roh.replace(' ', '')
                if merkmal not in merkmale: 
                    merkmal_liste.append(merkmal)
    print '\n'.join(merkmale[m] for m in sorted(merkmal_liste))
    

    
if __name__ == '__main__':
    merkmale_finden()