# -*- coding: utf-8 -*-
'''
Created on 09.10.2012

@author: dbuse
'''
from __future__ import unicode_literals


def chr_inc(c, inc=1):
    """Gebe den den inc-ten Nachfolger des Buchstabens c zurück"""
    if ord(c) + inc > 72:
        return 'H'
    else:
        return chr(ord(c) + inc)


def chr_dec(c, dec=1):
    """Gebe den den dec-ten Vorgänger des Buchstabens c zurück"""
    if ord(c) - dec < 65:
        return "A+"
    else:
        return chr(ord(c) - dec)
