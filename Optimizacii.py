'''
Created on Mar 16, 2016

@author: AS017303
'''
from itertools import permutations

def raztoqnie(dupka1, dupka2):
    x1 = dupka1['x']
    y1 = dupka1['y']
    x2 = dupka2['x']
    y2 = dupka2['y']
    
    return ((x1 - x2)**2 + (y1 - y2)**2) ** 0.5

def total_raztoqnie(dupki):  
    return sum([raztoqnie(dupka, dupki[index + 1]) for index, dupka in enumerate(dupki[:-1])])

def optimizirai_otvori(otvori, start=None):    
    if start is None:
        start = otvori[0]
    return min([perm for perm in permutations(otvori) if perm[0] == start], key=total_raztoqnie)

def is_dupka_duplicate(dupka, dupki):
    for d in dupki:
        if dupka['x'] == d['x'] and dupka['y'] == d['y']:
            return 1
    
    return 0