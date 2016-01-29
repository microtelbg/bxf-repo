#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
## dd/mm/yyyy format

from Tkinter import *
from tkFileDialog import askopenfilename

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

''' ***************************************************************************
*** Labels
*************************************************************************** '''
rotateButtonText = 'Завърти'
openBXFFileButtonText = 'Отвори BXF файл'
placeOnMachineButtonText = 'Постави на машината'
instrument1LabelText = 'Инструмент 1'
instrument2LabelText = 'Инструмент 2'
instrument3LabelText = 'Инструмент 3'
instrument4LabelText = 'Инструмент 4'
instrument5LabelText = 'Инструмент 5'
diameturLabelText = 'Диаметър (мм)'
skorostText = 'Скорост (мм/мин)'
generateGCodeButtonText = 'Генериране на G код'

''' ***************************************************************************
*** Global Variables
*************************************************************************** '''
ns = {'blum' : 'http://www.blum.com/bxf'}
mashtab = 0.5
filename = 'tester.bxf'

PLOT_NA_MACHINA_X = 1500
PLOT_NA_MACHINA_Y = 600

#Vsichi elementi of BXF faila za dupchene
elementi_za_dupchene = {}

# 0 - Po horizontalata, 1 - po verticalata
# 0: ako e strana (X,Z of BXF), X->Y(masata) Z->X(masata)
#    ako e duno   (X,Y ot BXF), X->Y(masata) Y->X(masata)
#    ako e grub   (Y,Z ot BXF), Y->X(masata) Z->Y(masata)
# 1: ako e strana (X,Z of BXF), X->X(masata) Z->Y(masata)
#    ako e duno   (X,Y ot BXF), X->X(masata) Y->Y(masata)
#    ako e grub   (Y,Z ot BXF), Y->Y(masata) Z->X(masata)
# Currently selected elements (izbranite v momenta elementi)
izbrani_elementi = {}

#Dupki za g-code
dupki_za_gcode = []

class ElementZaDupchene(object):
    def __init__(self, ime, razmeri, dupki):
        self.ime = ime
        self.razmeri = razmeri
        self.dupki = dupki

    def opisanie(self):
        print "-----------------------------------------------------------------------------------"
        print "Ime:", self.ime
        print "Razmeri: ", self.razmeri
        print len(self.dupki)
        print "Dupki: ", self.dupki
        print "-----------------------------------------------------------------------------------"


def cheti_bxf_file(filename1):
    tree = ET.parse(filename1)
    myroot = tree.getroot()
    
    #Reset
    elementi_za_dupchene.clear()

    suzdai_element_strana(myroot, elementi_za_dupchene, 'LinkeSeitenwand')
    suzdai_element_strana(myroot, elementi_za_dupchene, 'RechteSeitenwand')
    suzdai_element_vrata(myroot, elementi_za_dupchene, 'Tuer')
    suzdai_element_shkafche(myroot, elementi_za_dupchene, 'Aussenschubkasten')

    #suzdai_element_duno_gornica(root, element_dictionary, 'Oberboden')
    #suzdai_element_duno_gornica(root, element_dictionary, 'Unterboden')
    #print '-------------------------------------------'
    #suzdai_element_grub_prednica(root, element_dictionary, 'KorpusRueckwand')

def suzdai_element(root, elements, name):
    parenttag = 'blum:'+name
    print parenttag
    parent = root.find(parenttag, ns) #TODO: has to be findall
    if parent is not None:
        strana = parent.findall('.//blum:Quader', ns)
        print len(strana)
        if strana is not None:
            visochina = strana[0].find('blum:Hoehe', ns)
            if visochina is not None:
                s_y = visochina.text
            else:
                s_y = 0
                print 'Hoehe tag ne e namer za Quader za ', parenttag
            shirina = strana[0].find('blum:Position', ns)

            if shirina is not None:
                s_pos_x = shirina.attrib['X']
            else:
                s_pos_x = 0
                print 'Position tag ne e namer za Quader/LinkeSeitenwand'
            s_pointc = strana[0].find('blum:PunktC', ns)

            if s_pointc is not None:
                s_pointc_x = s_pointc.attrib['X']
            else:
                s_pointc_x = 0
                print 'PunktC tag ne e namer za Quader/LinkeSeitenwand'
            s_x = float(s_pointc_x) - float(s_pos_x)
        else:
            print 'Quader tag ne e namer za LinkeSeitenwand'

        print 'x:', s_x
        print 'y:', s_y


    else:
        print 'LinkeSeitenwand ne e nameren takuv tag'

''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     LinkeSeitenwand (lqva strana)
     RechteSeitenwand (dqsna strana)
     X and Z
*******************************************************************************'''
def suzdai_element_strana(root, elements, name):
    parenttag = 'blum:'+name
    print parenttag
    parent = root.find(parenttag, ns) #Namira samo 1 element s tozi tag. Predpolagam che samo 1 ima v bxf
    if parent is not None:
        # Orientacia e XZ, Y e debelina
        quader = parent.findall('.//blum:Quader', ns)
        if quader is not None:
            hoehe = quader[0].find('blum:Hoehe', ns)
            if hoehe is not None:
                razmer_z = hoehe.text
            else:
                razmer_z = 0
                print 'Greshka - Hoehe tag ne e nameren za ', name

            # <Position X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
            position = quader[0].find('blum:Position', ns)
            if position is not None:
                pos_x = position.attrib['X']
                pos_y = position.attrib['Y']
            else:
                pos_x = 0
                pos_y = 0
                print 'Greshka - Position tag ne e namer za ', name

            #<PunktC X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
            pointc = quader[0].find('blum:PunktC', ns)
            if pointc is not None:
                pointc_x = pointc.attrib['X']
                pointc_y = pointc.attrib['Y']
            else:
                pointc_x = 0
                pointc_y = 0
                print 'Greshka - PunktC tag ne e namer za ', name
            razmer_x = float(pointc_x) - float(pos_x)
            razmer_debelina = float(pointc_y) - float(pos_y)

            #Dupki
            dupki_map = suzdai_dupki(quader)
        else:
            print 'Greshka -Quader tag ne e namer za ', name

        #Create object
        razmeri_map = {"orientation" : "xz", "x" : razmer_x, "y": razmer_debelina, "z":razmer_z}

        stana = ElementZaDupchene(name, razmeri_map, dupki_map)
        if name == 'LinkeSeitenwand':
            elements['Lqva Strana'] = stana
        elif  name == 'RechteSeitenwand':
            elements['Dqsna Strana'] = stana
        else:
            elements[name] = stana

        print 'x:', razmer_x
        print 'z:', razmer_z
    else:
        print 'Greshka -', name, " ne e nameren takuv tag"

''' ***************************************************************************
**** Tazi funkcia chete parametrite za dupkite
*******************************************************************************'''
def suzdai_dupki(curparent):
    dupki_list = []
    #<Zylinder von_Bohrbild="*bb_sk_korpusschiene_422">
    bohrugen = curparent[0].find('blum:Bohrungen', ns)
    if bohrugen is not None:
        zylinders = bohrugen.findall('.//blum:Zylinder', ns)
        for zyl in zylinders:
            zyl_position = zyl.find('blum:Position', ns)
            zyl_pos_x = zyl_position.attrib['X']
            zyl_pos_y = zyl_position.attrib['Y']
            zyl_pos_z = zyl_position.attrib['Z']
            zyl_hoehe = zyl.find('blum:Hoehe', ns)
            zyl_h = zyl_hoehe.text
            zyl_radius = zyl.find('blum:Radius', ns)
            zyl_r = zyl_radius.text

            dupki = {"x" : zyl_pos_x, "y": zyl_pos_y, "z":zyl_pos_z, "h" : zyl_h, "r" : zyl_r}
            dupki_list.append(dupki)
    return dupki_list

''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     KorpusRueckwand (grub)
*******************************************************************************'''
def suzdai_element_grub_prednica(root, elements, name):
    parenttag = 'blum:'+name
    print parenttag
    parent = root.find(parenttag, ns) #Namira samo 1 element s tozi tag. Predpolagam che samo 1 ima v bxf
    if parent is not None:
        quader = parent.findall('.//blum:Quader', ns)

        if quader is not None:
            # <Hoehe>0.0</Hoehe> visochina
            hoehe = quader[0].find('blum:Hoehe', ns)
            if hoehe is not None:
                razmer_visochina = hoehe.text
            else:
                razmer_visochina = 0
                print 'Greshka - Hoehe tag ne e nameren za ', name

            # <Position X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
            position = quader[0].find('blum:Position', ns)
            if position is not None:
                pos_y = position.attrib['Y']
            else:
                pos_y = 0
                print 'Greshka - Position tag ne e namer za ', name

            # <PunktC X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
            point_c = quader[0].find('blum:PunktC', ns)
            if point_c is not None:
                pointc_y = point_c.attrib['Y']
            else:
                pointc_y = 0
                print 'Greshka - PunktC tag ne e namer za ', name

            #Izchisli razmerite na tazi starna
            razmer_x = float(razmer_visochina)
            razmer_y = float(pointc_y) - float(pos_y)
        else:
            print 'Greshka -Quader tag ne e namer za ', name

        print 'x:', razmer_x
        print 'y:', razmer_y
    else:
        print 'Greshka -', name, " ne e nameren takuv tag"

''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     Oberboden(gornica)
     Unterboden(duno)
*******************************************************************************'''
def suzdai_element_duno_gornica(root, elements, name):
    parenttag = 'blum:'+name
    print parenttag
    parent = root.find(parenttag, ns) #Namira samo 1 element s tozi tag. Predpolagam che samo 1 ima v bxf
    if parent is not None:
        quader = parent.findall('.//blum:Quader', ns)

        if quader is not None:
            # <Position X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
            position = quader[0].find('blum:Position', ns)
            if position is not None:
                pos_x = position.attrib['X']
                pos_y = position.attrib['Y']
            else:
                pos_x = 0
                pos_y = 0
                print 'Greshka - Position tag ne e namer za ', name

            # <PunktC X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
            point_c = quader[0].find('blum:PunktC', ns)
            if point_c is not None:
                pointc_x = point_c.attrib['X']
                pointc_y = point_c.attrib['Y']
            else:
                pointc_x = 0
                pointc_y = 0
                print 'Greshka - PunktC tag ne e namer za ', name

            #Izchisli razmerite na tazi starna
            razmer_x = float(pointc_x) - float(pos_x)
            razmer_y = float(pointc_y) - float(pos_y)
        else:
            print 'Greshka -Quader tag ne e namer za ', name

        print 'x:', razmer_x
        print 'y:', razmer_y
    else:
        print 'Greshka -', name, " ne e nameren takuv tag"

''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     Aussenschubkasten(vunshno shkafche)
     Innenschubkasten (vutreshno shkafche)
*******************************************************************************'''
def suzdai_element_shkafche(root, elements, name):
    #Prednata chast na shkafcheto e sushtata kato vratichka
    suzdai_element_vrata(root, elements, name)

    #Dunoto chast na shkafcheto
    parenttag = './/blum:'+name
    parents = root.findall(parenttag, ns) #Namira vsichki tags
    for parent in parents:
        parentName = parent.attrib['Name']
        duna = parent.findall('.//blum:Holzschubkasten', ns)
        for duno in duna:
            dunoID = duno.attrib['ID']
            quader = duno.findall('.//blum:Quader', ns)

            if quader is not None:
                # <Hoehe>0.0</Hoehe> visochina
                hoehe = quader[0].find('blum:Hoehe', ns)
                if hoehe is not None:
                    razmer_debelina = hoehe.text
                else:
                    razmer_debelina = 0
                    print 'Greshka - Hoehe tag ne e nameren za ', name

                # <Position X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
                position = quader[0].find('blum:Position', ns)
                if position is not None:
                    pos_x = position.attrib['X']
                    pos_y = position.attrib['Y']
                else:
                    pos_x = 0
                    pos_y = 0
                    print 'Greshka - Position tag ne e namer za ', name

                # <PunktC X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
                point_c = quader[0].find('blum:PunktC', ns)
                if point_c is not None:
                    pointc_x = point_c.attrib['X']
                    pointc_y = point_c.attrib['Y']
                else:
                    pointc_x = 0
                    pointc_y = 0
                    print 'Greshka - PunktC tag ne e namer za ', name

                #Izchisli razmerite na tazi vrata
                razmer_x = float(pointc_x) - float(pos_x)
                razmer_y = float(pointc_y) - float(pos_y)

                #Dupki
                dupki_map = suzdai_dupki(quader)

                #Create object
                razmeri_map = {"orientation" : "xy", "x" : razmer_x, "y": razmer_y, "z":razmer_debelina}

                dunoShkafche = ElementZaDupchene(name, razmeri_map, dupki_map)

                if name == 'Aussenschubkasten':
                    elements['Shafche-'+parentName+'Duno-'+dunoID] = dunoShkafche
                else:
                    elements[name] = dunoShkafche

            else:
                print 'Greshka -Quader tag ne e namer za ', name


''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     Tuer(edinichka vratichka)
     Doppeltuer (dvoina vratichka)
     Aussenschubkasten (samo chast - prednata chast na shkafcheto)
*******************************************************************************'''
def suzdai_element_vrata(root, elements, name):
    parenttag = './/blum:'+name
    parents = root.findall(parenttag, ns) #Namira vsichki tags
    for parent in parents:
        parentName = parent.attrib['Name']
        fronts = parent.findall('.//blum:Front', ns)
        for front in fronts:
            frontID = front.attrib['ID']
            quader = front.findall('.//blum:Quader', ns)

            if quader is not None:
                # <Hoehe>0.0</Hoehe> visochina
                hoehe = quader[0].find('blum:Hoehe', ns)
                if hoehe is not None:
                    razmer_z = hoehe.text
                else:
                    razmer_z = 0
                    print 'Greshka - Hoehe tag ne e nameren za ', name

                # <Position X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
                position = quader[0].find('blum:Position', ns)
                if position is not None:
                    pos_x = position.attrib['X']
                    pos_y = position.attrib['Y']
                else:
                    pos_x = 0
                    pos_y = 0
                    print 'Greshka - Position tag ne e namer za ', name

                # <PunktC X="0.0" Y="0.0" Z="0.0" Bezug="A"/>
                point_c = quader[0].find('blum:PunktC', ns)
                if point_c is not None:
                    pointc_x = point_c.attrib['X']
                    pointc_y = point_c.attrib['Y']
                else:
                    pointc_x = 0
                    pointc_y = 0
                    print 'Greshka - PunktC tag ne e namer za ', name

                #Izchisli razmerite na tazi vrata
                razmer_debelina = float(pointc_x) - float(pos_x)
                razmer_y = float(pointc_y) - float(pos_y)

                #Dupki
                dupki_map = suzdai_dupki(quader)

                #Create object
                razmeri_map = {"orientation" : "yz", "x" : razmer_debelina, "y": razmer_y, "z":razmer_z}

                vrata = ElementZaDupchene(name, razmeri_map, dupki_map)

                if name == 'Tuer':
                    elements['Vrata-'+parentName+'Front-'+frontID] = vrata
                elif name == 'Aussenschubkasten':
                    elements['Shafche-'+parentName+'Front-'+frontID] = vrata
                else:
                    elements[name] = vrata

            else:
                print 'Greshka -Quader tag ne e namer za ', name


def zaredi_file_info():
    myfilename = askopenfilename(filetypes=(("BXF files", "*.bxf"), ("All files", "*.*")))

    # 1. Procheti BXF file
    cheti_bxf_file(myfilename)

    # 2. Pokaji izbrania file
    fileNameLabel['text'] = myfilename

    # 3. Populti lista s elementi
    listbox.delete(0, END)
    for ek in elementi_za_dupchene.keys():
        listbox.insert(END, ek)

    #Reset
    canvas.delete(ALL)
    canvas.create_rectangle(20, 20, 770, 320, fill="bisque")
    
def izberi_element_za_dupchene():
      
    #Nameri izbrania element
    itemIndex = int(listbox.curselection()[0])
    itemValue = listbox.get(itemIndex)
    
    print elementi_za_dupchene

    izbranElement = elementi_za_dupchene[itemValue]

    #Sloji elementa v lista i purvonachalnata orientacia
    izbrani_elementi['L'] = izbranElement
    izbrani_elementi['LO'] = 0

    print izbranElement.opisanie()

    #narisuvai_po_horizontalata(izbranElement, 0)
    narisuvai_element_na_plota(izbranElement, 0)

def narisuvai_strana_na_plota(shirina, duljina):
    canvas.create_rectangle(30, 30, shirina*mashtab+30, duljina*mashtab+30, fill="lightblue")

def narisuvai_dupka_na_plota(xcoordinata, ycoordinata, radius, eIzvunPlota):
    nachalo_x = 30 + (xcoordinata - radius)*mashtab
    nachalo_y = 30 + (ycoordinata - radius)*mashtab
    krai_x = 30 + (xcoordinata + radius)*mashtab
    krai_y = 30 + (ycoordinata + radius)*mashtab

    if eIzvunPlota == 1:
        canvas.create_oval(nachalo_x, nachalo_y, krai_x, krai_y, fill="maroon")
    else:
        canvas.create_oval(nachalo_x, nachalo_y, krai_x, krai_y, fill="blue")

def rotate_element():
    #Nameri izbrania element
    izbranElement = izbrani_elementi['L']
    currentOrienatation = int(izbrani_elementi['LO'])
    
    if currentOrienatation == 3:
        newOrientation = 0
    else:
        newOrientation = currentOrienatation + 1
        
    izbrani_elementi['LO'] = newOrientation

    narisuvai_element_na_plota(izbranElement, newOrientation)

#     if newOrientation == 0:
#         #narisuvai_po_horizontalata(izbranElement, newOrientation)
#         narisuvai_element_na_plota(izbranElement, newOrientation)
#     elif newOrientation == 1:
#         narisuvai_po_verticalata(izbranElement, newOrientation)
#     elif newOrientation == 2:
#         narisuvai_po_horizontalata(izbranElement, newOrientation)
#     elif newOrientation == 3:
#         narisuvai_po_verticalata(izbranElement, newOrientation)
        
def ima_li_dupki_izvun_plota(orientacia_na_elementa, dupki_za_proverka, rotation, element_x, element_y):
    poneEdnaDupkaIzlizaPoX = 0
    poneEdnaDupkaIzlizaPoY = 0
    
    for dupka in dupki_za_proverka:
        if rotation == 0 or rotation == 2:
            if orientacia_na_elementa == 'xz':
                d_x = float(dupka['z'])
                d_y = float(dupka['x'])
                d_r = float(dupka['r'])
            elif orientacia_na_elementa == 'yz':
                d_x = float(dupka['y'])
                d_y = float(dupka['z'])
                d_r = float(dupka['r'])
            elif orientacia_na_elementa == 'xy':
                d_x = float(dupka['y'])
                d_y = float(dupka['x'])
                d_r = float(dupka['r'])
        else:
            if orientacia_na_elementa == 'xz':
                d_x = float(dupka['x'])
                d_y = float(dupka['z'])
                d_r = float(dupka['r'])
            elif orientacia_na_elementa == 'yz':
                d_x = float(dupka['z'])
                d_y = float(dupka['y'])
                d_r = float(dupka['r'])
            elif orientacia_na_elementa == 'xy':
                d_x = float(dupka['x'])
                d_y = float(dupka['y'])
                d_r = float(dupka['r'])
        
        d_r = float(dupka['r'])
        
        if rotation == 1:
            d_x = element_x - d_x
        elif rotation == 2:
            d_x = element_x - d_x
            d_y = element_y - d_y
        elif rotation == 3:
            d_y = element_y - d_y
        
        # Dobavi radiusa za da imame nai krainata tochka
        d_x = d_x + d_r
        d_y = d_y + d_r
        
        print 'd_x:', d_x
        print 'd_y:', d_y
               
        if poneEdnaDupkaIzlizaPoX == 0:
            if d_x > PLOT_NA_MACHINA_X:
                poneEdnaDupkaIzlizaPoX = 1
            
        if poneEdnaDupkaIzlizaPoY == 0:
            if d_y > PLOT_NA_MACHINA_Y:
                poneEdnaDupkaIzlizaPoY = 1    
        
    dupkiIzvunPlota = {}
    dupkiIzvunPlota["IzvunX"] = poneEdnaDupkaIzlizaPoX
    dupkiIzvunPlota["IzvunY"] = poneEdnaDupkaIzlizaPoY
    
    return dupkiIzvunPlota
        
        
def narisuvai_element_na_plota(izbranElement, rotation):
    #Reset
    canvas.delete(ALL)
    canvas.create_rectangle(20, 20, 770, 320, fill="bisque")
    del dupki_za_gcode[:]
    
    #Vzemi razmerite na stranata
    razmeri_na_elementa = izbranElement.razmeri
    orientacia_na_elementa = razmeri_na_elementa['orientation']
    if rotation == 0 or rotation == 2:
        if orientacia_na_elementa == 'xz':
            element_x = float(razmeri_na_elementa['z'])
            element_y = float(razmeri_na_elementa['x'])
        elif orientacia_na_elementa == 'yz':
            element_x = float(razmeri_na_elementa['y'])
            element_y = float(razmeri_na_elementa['z'])
        elif orientacia_na_elementa == 'xy':
            element_x = float(razmeri_na_elementa['y'])
            element_y = float(razmeri_na_elementa['x'])
    else:
        if orientacia_na_elementa == 'xz':
            element_x = float(razmeri_na_elementa['x'])
            element_y = float(razmeri_na_elementa['z'])
        elif orientacia_na_elementa == 'yz':
            element_x = float(razmeri_na_elementa['z'])
            element_y = float(razmeri_na_elementa['y'])
        elif orientacia_na_elementa == 'xy':
            element_x = float(razmeri_na_elementa['x'])
            element_y = float(razmeri_na_elementa['y'])
        
    #Nachertai elementa vurhu plota na machinata
    narisuvai_strana_na_plota(element_x, element_y)

    # Izliza li elementa ot plota na machinata?
    izlizaPoX = 0
    izlizaPoY = 0
    if element_x > PLOT_NA_MACHINA_X:
        izlizaPoX = 1
    if element_y > PLOT_NA_MACHINA_Y:
        izlizaPoY = 1
        
    dupki_na_elementa = izbranElement.dupki
    
    dupkaIzvunX = 0
    dupkaIzvunY = 0
    if izlizaPoX == 1 or izlizaPoY == 1:
        dupkiIzvunPlot = ima_li_dupki_izvun_plota(orientacia_na_elementa, dupki_na_elementa, rotation, element_x, element_y)
        dupkaIzvunX = dupkiIzvunPlot['IzvunX']
        dupkaIzvunY = dupkiIzvunPlot['IzvunY']
            
    for dupka in dupki_na_elementa:
        if rotation == 0 or rotation == 2:
            if orientacia_na_elementa == 'xz':
                d_x = float(dupka['z'])
                d_y = float(dupka['x'])
                d_r = float(dupka['r'])
            elif orientacia_na_elementa == 'yz':
                d_x = float(dupka['y'])
                d_y = float(dupka['z'])
                d_r = float(dupka['r'])
            elif orientacia_na_elementa == 'xy':
                d_x = float(dupka['y'])
                d_y = float(dupka['x'])
                d_r = float(dupka['r'])
        else:
            if orientacia_na_elementa == 'xz':
                d_x = float(dupka['x'])
                d_y = float(dupka['z'])
                d_r = float(dupka['r'])
            elif orientacia_na_elementa == 'yz':
                d_x = float(dupka['z'])
                d_y = float(dupka['y'])
                d_r = float(dupka['r'])
            elif orientacia_na_elementa == 'xy':
                d_x = float(dupka['x'])
                d_y = float(dupka['y'])
                d_r = float(dupka['r'])
                
        dulbochina = float(dupka['h'])
        
        if rotation == 1:
            d_x = element_x - d_x
        elif rotation == 2:
            d_x = element_x - d_x
            d_y = element_y - d_y
        elif rotation == 3:
            d_y = element_y - d_y
        
        # Proveri kude e tazi dupka spriamo sredata na elementa
        izlizaPoX = 0
        izlizaPoY = 0
        if dupkaIzvunX == 1:
            if d_x > element_x/2:
                izlizaPoX = 1
        
        if dupkaIzvunY == 1:
            if d_y > element_y/2:
                izlizaPoY = 1
        
        
        if izlizaPoX == 0 and izlizaPoY == 0:     
            # Zapazi tochnite koordinati na dupkite za g-code
            dupka_za_gcode = {"x" : d_x, "y": d_y, "h" : dulbochina, "r" : d_r}
            dupki_za_gcode.append(dupka_za_gcode)
            
            narisuvai_dupka_na_plota(d_x, d_y, d_r, 0)
        else:
            narisuvai_dupka_na_plota(d_x, d_y, d_r, 1)        

def instrument_za_dupka(diametur):
    if diametur == 35:
        return 'T1'
    elif diametur == 15:
        return 'T2'
    elif diametur == 8:
        return 'T3'
    elif diametur == 5:
        return 'T4'
    elif diametur == 2.5:
        return 'T5'
    else:
        return 'invalid'

def skorost_za_dupka(instrument):
    if instrument == 'T1':
        return float(instrument1EntrySkorostValue.get())
    elif instrument == 'T2':
        return float(instrument2EntrySkorostValue.get())
    elif instrument == 'T3':
        return float(instrument3EntrySkorostValue.get())
    elif instrument == 'T4':
        return float(instrument4EntrySkorostValue.get())
    elif instrument == 'T5':
        return float(instrument5EntrySkorostValue.get())
    else:
        return -1
    
def suzdai_gcode_file():  
    # Line iterator
    n10 = 30
    bezopasno_z = "{0:.3f}".format(50.000) # Tova she bude izchesleno kato debelinata na materiala ot bxf + 20
    debelinaMaterial = 18.0
    razmerNachalnaDupka = 0
    
    # Stoinosti na instrumentite
    dateTimeLine = '('+time.strftime("%d/%m/%Y")+')\n'
    instr1Value = '(Instrument 1: Diametur:'+ instrument1EntryDiaValue.get()+', Skorost:'+ instrument1EntrySkorostValue.get()+ ')\n'
    instr2Value = '(Instrument 2: Diametur:'+ instrument2EntryDiaValue.get()+', Skorost:'+ instrument2EntrySkorostValue.get()+ ')\n'
    instr3Value = '(Instrument 3: Diametur:'+ instrument3EntryDiaValue.get()+', Skorost:'+ instrument3EntrySkorostValue.get()+ ')\n'
    instr4Value = '(Instrument 4: Diametur:'+ instrument4EntryDiaValue.get()+', Skorost:'+ instrument4EntrySkorostValue.get()+ ')\n'
    instr5Value = '(Instrument 5: Diametur:'+ instrument5EntryDiaValue.get()+', Skorost:'+ instrument5EntrySkorostValue.get()+ ')\n'
         
    fw = open("sample123.txt", "w")
    fw.write("(Imeto na file)\n")
    fw.write(dateTimeLine)
    fw.write(instr1Value)
    fw.write(instr2Value)
    fw.write(instr3Value)
    fw.write(instr4Value)
    fw.write(instr5Value)   
    # Tova e samo za komentar v g-code za da vidq koq sled koq dupka se dupchi
    for dupka in dupki_za_gcode:
        dupkaLine = '(Dupka: X:'+ str("{0:.3f}".format(dupka['x'])) + ', Y:' + str(dupka['y']) +', R:'+ str(dupka['r']) + ')\n'
        fw.write(dupkaLine)
        if razmerNachalnaDupka == 0:
            razmerNachalnaDupka = dupka['r']*2
    
    
    # Logika za liniite na g-coda
    TT = instrument_za_dupka(razmerNachalnaDupka)
    HT = 'H'+TT[1]
    SD = "{0:.1f}".format(skorost_za_dupka(TT))
    vzemiInstrument = 'N'+str(n10)+TT+'M06\n'
    n10 = n10 + 10
    predpazvaneNaZ = 'N'+str(n10)+'G00G43Z'+str(bezopasno_z)+HT+'\n'
    n10 = n10 + 10
    zavurtiNaMaxOboroti = 'N'+str(n10)+'S6000M03\n'
    n10 = n10 + 10
    prediNachalnoPozicionirane = 'N'+str(n10)+'G94\n'
    n10 = n10 + 10
    
    # Nachalo na g-code
    fw.write('N10G00G21G17G90G40G49G80\n')    
    fw.write('N20G71G91.1\n')  
    fw.write(vzemiInstrument)
    fw.write(predpazvaneNaZ)
    fw.write(zavurtiNaMaxOboroti)
    fw.write(prediNachalnoPozicionirane)
    
    #Dupki
    purvonachaloZ = "{0:.3f}".format(debelinaMaterial + 5)
    for dupka in dupki_za_gcode:
        # Vij kakuv instrument triabva da polzvash
        instrZaDupka = instrument_za_dupka(dupka['r']*2)
        
        if instrZaDupka != TT:  
            # Smeni instrumenta
            TT = instrZaDupka
            HT = 'H'+TT[1]
            SD = "{0:.1f}".format(skorost_za_dupka(TT))
            vzemiInstrument = 'N'+str(n10)+TT+'M06\n'
            n10 = n10 + 10
            fw.write(vzemiInstrument)
            d4Line = 'N'+str(n10)+'G43'+HT+'\n'
            fw.write(d4Line)
            n10 = n10 + 10
            zavurtiNaMaxOboroti = 'N'+str(n10)+'S6000M03\n'
            n10 = n10 + 10
            fw.write(zavurtiNaMaxOboroti)
            
        d1Line = 'N'+str(n10)+'G00X'+str("{0:.3f}".format(dupka['x']))+'Y'+str("{0:.3f}".format(dupka['y']))+"Z"+str(purvonachaloZ)+'\n'
        n10 = n10 + 10
        fw.write(d1Line)
        krainoZ = "{0:.3f}".format(debelinaMaterial - dupka['h'])
        d2Line = 'N'+str(n10)+'G1X'+str("{0:.3f}".format(dupka['x']))+'Y'+str("{0:.3f}".format(dupka['y']))+"Z"+str(krainoZ)+'F'+SD+'\n'
        n10 = n10 + 10
        fw.write(d2Line)   
        d3Line = 'N'+str(n10)+'G00X'+str("{0:.3f}".format(dupka['x']))+'Y'+str("{0:.3f}".format(dupka['y']))+"Z"+str(purvonachaloZ)+'\n'
        n10 = n10 + 10
        fw.write(d3Line)
    
    krai1 = 'N'+str(n10)+'G00Z'+str(bezopasno_z)+'\n'
    n10 = n10 + 10
    krai2 = 'N'+str(n10)+'G00X0.000Y0.000\n'
    n10 = n10 + 10
    krai3 = 'N'+str(n10)+'M09\n'
    n10 = n10 + 10
    krai4 ='N'+str(n10)+'M30\n'
    n10 = n10 + 10
    
    fw.write(krai1)
    fw.write(krai2)
    fw.write(krai3)
    fw.write(krai4)
    
    fw.close()

print ('*** BEGIN PROGRAM *************************')
mainframe = Tk()
#mainframe.geometry('450x450+500+300') - Use that for window size

''' ***************************************************************************
*** Variables za stoinosti na instrumentite
*************************************************************************** '''
instrument1EntryDiaValue = StringVar()
instrument1EntrySkorostValue = StringVar()
instrument2EntryDiaValue = StringVar()
instrument2EntrySkorostValue = StringVar()
instrument3EntryDiaValue = StringVar()
instrument3EntrySkorostValue = StringVar()
instrument4EntryDiaValue = StringVar()
instrument4EntrySkorostValue = StringVar()
instrument5EntryDiaValue = StringVar()
instrument5EntrySkorostValue = StringVar()

# Default values (she doidat posle of file)
instrument1EntryDiaValue.set('35')
instrument1EntrySkorostValue.set('800')
instrument2EntryDiaValue.set('15')
instrument2EntrySkorostValue.set('1000')
instrument3EntryDiaValue.set('8')
instrument3EntrySkorostValue.set('1200')
instrument4EntryDiaValue.set('5')
instrument4EntrySkorostValue.set('1500')
instrument5EntryDiaValue.set('2.5')
instrument5EntrySkorostValue.set('1500')

# ********** File Menu *************
mainMenu = Menu(mainframe)
mainframe.config(menu=mainMenu)
fileManu = Menu(mainMenu)
fileManu.add_command(label="Open", command=zaredi_file_info)
mainMenu.add_cascade(label="File", menu=fileManu)

# ********** Toolbar *************
toolbar = Frame(mainframe, bg="honeydew")
openButton = Button(toolbar, text=openBXFFileButtonText, command=zaredi_file_info)
openButton.grid(row=0, padx=20, pady=2)
fileNameLabel = Label(toolbar, text="")
fileNameLabel.grid(row=0, column=1, padx=2, pady=2)
toolbar.grid(row=0, columnspan=3, sticky=W+E)

# ********** Rotate Button *************
rotateButton = Button(mainframe, text=rotateButtonText, bg="lightblue", command=rotate_element)
rotateButton.grid(row=1, column=2, sticky=W, padx=20, pady=2)

# ********** Listbox *************
listbox = Listbox(mainframe, width=50)
listbox.grid(row=2, sticky=N+S, padx=10)

# ********** Frame *************
frame = Frame(mainframe)
frame.grid(row=2, column=1, sticky=N+S)

# ********** Move Button *************
moveButton = Button(frame, text=placeOnMachineButtonText, bg="bisque", command=izberi_element_za_dupchene)
moveButton.grid(row=0, columnspan=2, sticky=N)

# ********** Instrumenti *************
instr1LabelBox = LabelFrame(frame, text=instrument1LabelText)
instr1LabelBox.grid(row=1, columnspan=2, pady=10)
dia1Label = Label(instr1LabelBox, text=diameturLabelText)
dia1Label.grid(row=0, sticky=W)
dia1Entry = Entry(instr1LabelBox, textvariable=instrument1EntryDiaValue)
dia1Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
skorost1Label = Label(instr1LabelBox, text=skorostText)
skorost1Label.grid(row=1, sticky=W)
skorost1Entry = Entry(instr1LabelBox, textvariable=instrument1EntrySkorostValue)
skorost1Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)

instr2LabelBox = LabelFrame(frame, text=instrument2LabelText)
instr2LabelBox.grid(row=2, columnspan=2, pady=10)
dia2Label = Label(instr2LabelBox, text=diameturLabelText)
dia2Label.grid(row=0, sticky=W)
dia2Entry = Entry(instr2LabelBox, textvariable=instrument2EntryDiaValue)
dia2Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
skorost2Label = Label(instr2LabelBox, text=skorostText)
skorost2Label.grid(row=1, sticky=W)
skorost2Entry = Entry(instr2LabelBox, textvariable=instrument2EntrySkorostValue)
skorost2Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)

instr3LabelBox = LabelFrame(frame, text=instrument3LabelText)
instr3LabelBox.grid(row=3, columnspan=2, pady=10)
dia3Label = Label(instr3LabelBox, text=diameturLabelText)
dia3Label.grid(row=0, sticky=W)
dia3Entry = Entry(instr3LabelBox, textvariable=instrument3EntryDiaValue)
dia3Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
skorost3Label = Label(instr3LabelBox, text=skorostText)
skorost3Label.grid(row=1, sticky=W)
skorost3Entry = Entry(instr3LabelBox, textvariable=instrument3EntrySkorostValue)
skorost3Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)

instr4LabelBox = LabelFrame(frame, text=instrument4LabelText)
instr4LabelBox.grid(row=4, columnspan=2, pady=10)
dia4Label = Label(instr4LabelBox, text=diameturLabelText)
dia4Label.grid(row=0, sticky=W)
dia4Entry = Entry(instr4LabelBox, textvariable=instrument4EntryDiaValue)
dia4Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
skorost4Label = Label(instr4LabelBox, text=skorostText)
skorost4Label.grid(row=1, sticky=W)
skorost4Entry = Entry(instr4LabelBox, textvariable=instrument4EntrySkorostValue)
skorost4Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)

instr5LabelBox = LabelFrame(frame, text=instrument5LabelText)
instr5LabelBox.grid(row=5, columnspan=2, pady=10)
dia5Label = Label(instr5LabelBox, text=diameturLabelText)
dia5Label.grid(row=0, sticky=W)
dia5Entry = Entry(instr5LabelBox, textvariable=instrument5EntryDiaValue)
dia5Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
skorost5Label = Label(instr5LabelBox, text=skorostText)
skorost5Label.grid(row=1, sticky=W)
skorost5Entry = Entry(instr5LabelBox, textvariable=instrument5EntrySkorostValue)
skorost5Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)


# ********** Generate G-Code Button *************
generateGCodeButton = Button(frame, text=generateGCodeButtonText, bg="tomato", command=suzdai_gcode_file)
generateGCodeButton.grid(row=7, columnspan=2, pady = 20, sticky=N)

# ********** Canvas *************
canvas = Canvas(mainframe, width=1100, heigh=700, bg="grey")
#Slojib bg = grey za da vijdam kude e canvas
canvas.grid(row=2, column=2, padx=20, sticky=W+E+N+S)

# ********** Masa *************
# Originalen razmer e 1500 mm na 600 mm. Mashtab (x 0.5) => duljinata e 750 i shirina e 300.
# Sledovatelno koordinatite she sa offset s nachalnata tochka. (+20)
masa = canvas.create_rectangle(20, 20, PLOT_NA_MACHINA_X*mashtab+20, PLOT_NA_MACHINA_Y*mashtab+20, fill="bisque")


mainframe.mainloop()

print ('*** END PROGRAM *************************')
