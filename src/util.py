# -*- coding: utf-8 -*-
'''
Created on 09.10.2012

@author: dbuse
'''

def chr_inc(c, inc=1):
    """Gebe den den inc-ten Nachfolger des Buchstabens c zurück"""
    return chr(ord(c) + inc)

def chr_dec(c, dec=1):
    """Gebe den den dec-ten Vorgänger des Buchstabens c zurück"""
    return chr(ord(c) - dec)
