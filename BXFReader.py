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
rotateButtonText = u'Завърти'
removeButtonText = u'Премахни'
editButtonText = u'Редактирай'
orLabelText = u' или '
openBXFFileButtonText = u'Отвори BXF файл'
createButtonText = u'Създай елемент'
placeOnMachineButtonText = u'Постави на ЛЯВА база'
placeOnMachineRightButtonText = u'Постави на ДЯСНА база'
leftBazaGrouperText = u'ЛЯВА база'
rightBazaGrouperText = u'ДЯСНА база'
instrument1LabelText = u'Инструмент 1'
instrument2LabelText = u'Инструмент 2'
instrument3LabelText = u'Инструмент 3'
instrument4LabelText = u'Инструмент 4'
instrument5LabelText = u'Инструмент 5'
diameturLabelText = u'Диаметър (мм)'
skorostText = u'Скорост (мм/мин)'
generateGCodeButtonText = u'Генериране на G код'

detailTitleText = u'Детайл'
detailImeText = u'Име на детайла: '
detailRazmeriText = u'Размери '
detailDuljinaText = u'Дължина: '
detailShirinaText = u'Ширина: '
detailDebelinaText = u'Дебелина: '

okButtonText = u'Потвърди'
cancelButtonText = u'Отхвърли'

dobaviFixLabelText = u'Добави фикс'
leftFixLabelText = u'Ляво'
centerFixLabelText = u'Централно'
rightFixLabelText = u'Дясно'
dulbochinaFixLabelText = u'Дълбочина на хоризонтален отвор:'
dobaviButtonText = u'Добави'
dobaviVerOtvorLabelText = u'Добави вертикален отвор'
dobaviHorOtvorLabelText = u'Добави хоризонтален отвор'
dobaviOtvorLabelText = u'Добави отвор'
vertikalenLabelText = u'Вертикален'
horizontalenLabelText = u'Хоризонтален'
paramFixLabelText = u'Параметри на фикса'
otstoqniePoXLabelText = u'Отстояние по хоризонтал'
otstoqniePoYLabelText = u'Отстояние по вертикал'
dulbochinaVertikalenOtvorLabelText = u'Вертикален отвор - Дълбочина'
dulbochinaHorizontOtvorYLabelText = u'Хоризонтален отвор - Дълбочина'
diameturVertikalenOtvorXLabelText = u'Вертикален отвор - Диаметър'
diameturHorizontOtvorLabelText = u'Хоризонтален отвор - Диаметър'
kopiraiPoXSimetrichnoLabelText = u'Добави фикс симетрично по ХОРИЗОНТАЛ'
kopiraiPoYSimetrichnoLabelText = u'Добави фикс симетрично по ВЕРТИКАЛ'
centralenFixLabelText = u'Постави централен фикс'
copyCentralenFixLabelText = u'Добави огледален централен фикс'
postaviFixLabelText = u'Постави фикс'
stupkaNazadLabelText = u'Стъпка назад'
izchistiFixoveLabelText = u'Изчисти фиксове' 
zapaziFixoveLabelText = u'Запази фиксове'
izbereteOpciaLabelText = u'Изберете опция за редактиране ...'
dobaviPantaLabelText = u'Добави панта'
iztriiButtonText = u'Изтрий'



''' ***************************************************************************
*** Constants
*************************************************************************** '''
ns = {'blum' : 'http://www.blum.com/bxf'}
mashtab = 0.5

PLOT_NA_MACHINA_X = 1500
PLOT_NA_MACHINA_Y = 600

''' ***************************************************************************
*** Global Variables
*************************************************************************** '''
# Elementi svurzani s SAMO s grafikata
leftOvals = []
rightOvals = []

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
izbranElementZaRedakciaInd = ''

#Dupki za g-code
dupki_za_gcode = []

prevod_za_elemnti_v_list = {}

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

    suzdai_element_duno_gornica(myroot, elementi_za_dupchene, 'Oberboden')
    suzdai_element_duno_gornica(myroot, elementi_za_dupchene, 'Unterboden')
    suzdai_element_strana(myroot, elementi_za_dupchene, 'LinkeSeitenwand')
    suzdai_element_strana(myroot, elementi_za_dupchene, 'RechteSeitenwand')
    suzdai_element_vrata(myroot, elementi_za_dupchene, 'Tuer')
    suzdai_element_vrata(myroot, elementi_za_dupchene, 'Doppeltuer')
    suzdai_element_shkafche(myroot, elementi_za_dupchene, 'Aussenschubkasten')
    suzdai_element_vrata(myroot, elementi_za_dupchene, 'Klappensystem')
    
    # Da se dobavi oshte: 

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
            dupki_map = suzdai_dupki(quader, 'xz', razmer_z, razmer_x)
        else:
            print 'Greshka -Quader tag ne e namer za ', name

        #Create object
        razmeri_map = {"x" : razmer_z, "y": razmer_x , "h":razmer_debelina}

        stana = ElementZaDupchene(name, razmeri_map, dupki_map)
        if name == 'LinkeSeitenwand':
            elements['LinkeSeitenwand'] = stana
            prevod_za_elemnti_v_list['LinkeSeitenwand'] = u'Лява страна '+str(razmer_x)+' x '+str(razmer_z)
        elif  name == 'RechteSeitenwand':
            elements['RechteSeitenwand'] = stana
            prevod_za_elemnti_v_list['RechteSeitenwand'] = u'Дясна страна '+str(razmer_x)+' x '+str(razmer_z)
        else:
            elements[name] = stana
            prevod_za_elemnti_v_list[name] = name

    else:
        print 'Greshka -', name, " ne e nameren takuv tag"

''' ***************************************************************************
**** Tazi funkcia chete parametrite za dupkite
*******************************************************************************'''
def suzdai_dupki(curparent, orientation, element_x, element_y):
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
            
            if orientation == 'xy':
                dupki = {"x" : zyl_pos_y, "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            elif orientation == 'yz':
                dupki = {"x" : zyl_pos_y, "y": float(element_y) - float(zyl_pos_z), "h" : zyl_h, "r" : zyl_r}
            elif orientation == 'xz':
                dupki = {"x" : float(element_x) - float(zyl_pos_z), "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}

            dupki_list.append(dupki)
    return dupki_list

''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     KorpusRueckwand (grub)
     
     Moje sigurno da se mahne, zashtoto e sushtoto kato _vrata
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

    parent = root.find(parenttag, ns) #Namira samo 1 element s tozi tag. Predpolagam che samo 1 ima v bxf
    if parent is not None:
        quader = parent.findall('.//blum:Quader', ns)

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

            #Izchisli razmerite na tazi starna
            razmer_x = float(pointc_x) - float(pos_x)
            razmer_y = float(pointc_y) - float(pos_y)
            
            #Dupki
            dupki_map = suzdai_dupki(quader, 'xy', razmer_y, razmer_x)

            #Create object
            razmeri_map = {"x" : razmer_y, "y": razmer_x, "h":razmer_debelina}

            plot = ElementZaDupchene(name, razmeri_map, dupki_map)

            if name == 'Oberboden':
                elements['Oberboden'] = plot
                prevod_za_elemnti_v_list['Oberboden'] = u'Горен плот '+str(razmer_x)+' x '+str(razmer_y)
            elif name == 'Unterboden':
                elements['Unterboden'] = plot
                prevod_za_elemnti_v_list['Unterboden'] = u'Долен плот '+str(razmer_x)+' x '+str(razmer_y)
            else:
                elements[name] = plot
                prevod_za_elemnti_v_list[name] = name
        else:
            print 'Greshka -Quader tag ne e namer za ', name

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
                dupki_map = suzdai_dupki(quader, 'xy', razmer_y, razmer_x)

                #Create object
                razmeri_map = {"x" : razmer_y, "y": razmer_x, "h":razmer_debelina}

                dunoShkafche = ElementZaDupchene(name, razmeri_map, dupki_map)

                if name == 'Aussenschubkasten':
                    elements['Shafche-'+parentName+'Duno-'+dunoID] = dunoShkafche
                    prevod_za_elemnti_v_list['Shafche-'+parentName+'Duno-'+dunoID] = u'Чекмедже-'+parentName+u'Дъно-'+dunoID+str(razmer_x)+' x '+str(razmer_y)
                else:
                    elements[name] = dunoShkafche
                    prevod_za_elemnti_v_list[name] = name+str(razmer_x)+' x '+str(razmer_y)

            else:
                print 'Greshka -Quader tag ne e namer za ', name


        rueckwands = parent.findall('.//blum:Rueckwand', ns)
        for rueckwand in rueckwands:
            rueckwandID = rueckwand.attrib['ID']
            quader = rueckwand.findall('.//blum:Quader', ns)

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
                dupki_map = suzdai_dupki(quader, 'xy', razmer_y, razmer_x)

                #Create object
                razmeri_map = {"x" : razmer_y, "y": razmer_x, "z":razmer_debelina}

                rueckwandShkafche = ElementZaDupchene(name, razmeri_map, dupki_map)

                if name == 'Aussenschubkasten':
                    elements['Shafche-'+parentName+'Rueckwand-'+rueckwandID] = rueckwandShkafche
                    prevod_za_elemnti_v_list['Shafche-'+parentName+'Rueckwand-'+rueckwandID] = u'Чекмедже-'+parentName+'Rueckwand-'+rueckwandID+str(razmer_x)+' x '+str(razmer_y)
                else:
                    elements[name] = rueckwandShkafche
                    prevod_za_elemnti_v_list[name] = name+str(razmer_x)+' x '+str(razmer_y)

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
                dupki_map = suzdai_dupki(quader, 'yz', razmer_y, razmer_z)

                #Create object
                razmeri_map = {"x" : razmer_y, "y": razmer_z, "h" : razmer_debelina}

                vrata = ElementZaDupchene(name, razmeri_map, dupki_map)

                if name == 'Tuer':
                    ekey = 'Vrata-'+parentName+'Front-'+frontID
                    elements[ekey] = vrata
                    prevod_za_elemnti_v_list[ekey] = u'Врата - '+'ID:'+parentName+u'Лице:'+frontID+'.....'+str(razmer_y)+' x '+str(razmer_z)
                elif name == 'Doppeltuer':
                    ekey = 'Dvoina Vrata-'+parentName+'Front-'+frontID
                    elements[ekey] = vrata
                    prevod_za_elemnti_v_list[ekey] = u'Двойна Врата-'+'ID:'+parentName+u'Лице:'+frontID+'.....'+str(razmer_y)+' x '+str(razmer_z)
                elif name == 'Aussenschubkasten':
                    elements['Shafche-'+parentName+'Front-'+frontID] = vrata
                    prevod_za_elemnti_v_list['Shafche-'+parentName+'Front-'+frontID] = u'Чекмедже-'+parentName+'Front-'+frontID+'.....'+str(razmer_y)+' x '+str(razmer_z)
                elif name == 'Klappensystem':
                    elements['Vrata Aventos HF-'+parentName+'Front-'+frontID] = vrata
                    prevod_za_elemnti_v_list['Vrata Aventos HF-'+parentName+'Front-'+frontID] = u'Врата Aventos HF-'+parentName+'Front-'+frontID+'.....'+str(razmer_y)+' x '+str(razmer_z)
                else:
                    elements[name] = vrata
                    prevod_za_elemnti_v_list[name] = name+str(razmer_y)+' x '+str(razmer_z)

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
        prevod = prevod_za_elemnti_v_list[ek]
        listbox.insert(END, prevod)

    #Reset
    canvas.delete(ALL)
    canvas.create_rectangle(20, 20, PLOT_NA_MACHINA_X*mashtab+20, PLOT_NA_MACHINA_Y*mashtab+20, fill="bisque")
    
def izberi_element_za_dupchene(side):
      
    #Nameri izbrania element
    itemIndex = int(listbox.curselection()[0])
    itemValue = listbox.get(itemIndex)
    iValue = itemValue
    
    for eng, bg in prevod_za_elemnti_v_list.iteritems():
        if itemValue == bg:
            iValue = eng
            break

    izbranElement = elementi_za_dupchene[iValue]
    print izbranElement.opisanie()
    
    if side == 'L':
        #Sloji elementa v lista i purvonachalnata orientacia
        izbrani_elementi['L'] = izbranElement
        izbrani_elementi['LO'] = 0
        narisuvai_element_na_plota(izbranElement, 0, 'L', canvas, 1)
    elif side == 'R':
        #Sloji elementa v lista i purvonachalnata orientacia
        izbrani_elementi['R'] = izbranElement
        izbrani_elementi['RO'] = 0
        narisuvai_element_na_plota(izbranElement, 0, 'R', canvas, 1)

def izberi_element_za_lqva_strana():
    izberi_element_za_dupchene('L')

def izberi_element_za_dqsna_strana():
    izberi_element_za_dupchene('R')

def narisuvai_strana_na_plota(x, y, side, canvestodrawon, rotation):
    if side == 'L':
        canvestodrawon.create_rectangle(30, 30, x*mashtab+30, y*mashtab+30, fill="lightblue", tags="leftRec")
        
        if rotation == 0:
            canvestodrawon.create_line(30, 28, x*mashtab/2+30, 28, fill="purple", width=2, tags="border1")
            canvestodrawon.create_line(28, 30, 28, y*mashtab/2+30, fill="purple", width = 2, tags="border2")
        elif rotation == 1:
            canvestodrawon.create_line(x*mashtab/2+30, 28, x*mashtab+30, 28, fill="purple", width=2, tags="border1")
            canvestodrawon.create_line(x*mashtab+32, 30, x*mashtab+32, y*mashtab/2+30, fill="purple",  width=2,tags="border2")
        elif rotation == 2:
            canvestodrawon.create_line(x*mashtab+32, y*mashtab/2+30, x*mashtab+32, y*mashtab+30, fill="purple", width=2, tags="border1")
            canvestodrawon.create_line(x*mashtab/2+30, y*mashtab+32, x*mashtab+30, y*mashtab+32, fill="purple", width=2, tags="border2")
        elif rotation == 3:
            canvestodrawon.create_line(28, y*mashtab/2+30, 28, y*mashtab+30, fill="purple", width=2, tags="border1")
            canvestodrawon.create_line(30, y*mashtab+32, x*mashtab/2+30, y*mashtab+32, fill="purple", width=2, tags="border2")    
            
    elif side == 'R':
        nachalenX = PLOT_NA_MACHINA_X*mashtab+10 - x*mashtab
        kraenX = nachalenX + x*mashtab
        
        canvestodrawon.create_rectangle(nachalenX, 30, kraenX, y*mashtab+30, fill="lightgreen", tags="rightRec")

def narisuvai_dupka_na_plota(isHorizontDupka, xcoordinata, ycoordinata, dulbochina, radius, eIzvunPlota, side, canvestodrawon):
    if side == 'L':
        nachalo_x = 30 + (xcoordinata - radius)*mashtab
        krai_x = 30 + (xcoordinata + radius)*mashtab
    elif side == 'R':
        nachalo_x = 10 + (PLOT_NA_MACHINA_X - xcoordinata - radius)*mashtab
        krai_x = 10 + (PLOT_NA_MACHINA_X - xcoordinata + radius)*mashtab
    
    if isHorizontDupka == 1:
        nachalo_y = 30
        krai_y = 30 + dulbochina*mashtab
    else:     
        nachalo_y = 30 + (ycoordinata - radius)*mashtab
        krai_y = 30 + (ycoordinata + radius)*mashtab

    if eIzvunPlota == 1:
        if isHorizontDupka == 1:
            ov =  canvestodrawon.create_rectangle(nachalo_x, nachalo_y, krai_x, krai_y, fill="maroon")
        else:    
            ov = canvestodrawon.create_oval(nachalo_x, nachalo_y, krai_x, krai_y, fill="maroon")
    else:
        if isHorizontDupka == 1:
            ov =  canvestodrawon.create_rectangle(nachalo_x, nachalo_y, krai_x, krai_y, fill="red")
        else: 
            ov = canvestodrawon.create_oval(nachalo_x, nachalo_y, krai_x, krai_y, fill="blue")
    
    if side == 'L':    
        leftOvals.append(ov)
    elif side == 'R':
        rightOvals.append(ov)
    

def mahni_element_ot_lqva_baza():
    canvas.delete("leftRec")
    for ov in leftOvals:
        canvas.delete(ov)
    
    #Oshte neshta za reset
    del dupki_za_gcode[:]
    del izbrani_elementi['L']
    del izbrani_elementi['LO']

def mahni_element_ot_dqsna_baza():
    canvas.delete("rightRec")
    for ov in rightOvals:
        canvas.delete(ov)
    
    #Oshte neshta za reset
    del dupki_za_gcode[:]
    del izbrani_elementi['R']
    del izbrani_elementi['RO']

def rotate_element_lqva_baza():
    rotate_element('L', canvas)
    
def rotate_element_dqsna_baza():
    rotate_element('R', canvas)
        
def rotate_element(side, ccanvas):
    #Nameri izbrania element
    if side == 'L':
        izbranElement = izbrani_elementi['L']
        currentOrienatation = int(izbrani_elementi['LO'])
    elif side == 'R':
        izbranElement = izbrani_elementi['R']
        currentOrienatation = int(izbrani_elementi['RO'])
    
    if currentOrienatation == 3:
        newOrientation = 0
    else:
        newOrientation = currentOrienatation + 1
    
    if side == 'L':   
        izbrani_elementi['LO'] = newOrientation
        narisuvai_element_na_plota(izbranElement, newOrientation, 'L', ccanvas, 1)
    elif side == 'R':
        izbrani_elementi['RO'] = newOrientation
        narisuvai_element_na_plota(izbranElement, newOrientation, 'R', ccanvas, 1)
        
def ima_li_dupki_izvun_plota(dupki_za_proverka, rotation, element_x, element_y):
    poneEdnaDupkaIzlizaPoX = 0
    poneEdnaDupkaIzlizaPoY = 0
    
    for dupka in dupki_za_proverka:
        if rotation == 0 or rotation == 2:
            d_x = float(dupka['x'])
            d_y = float(dupka['y'])
        else:
            d_x = float(dupka['y'])
            d_y = float(dupka['x'])
            
        
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
                
def narisuvai_element_na_plota(izbranElement, rotation, side, canvestodrawon, resetCanvasInd):
    #Reset
    if resetCanvasInd == 1:
        if side == 'L':
            canvestodrawon.delete("leftRec")
            canvestodrawon.delete("border1")
            canvestodrawon.delete("border2")
            for ov in leftOvals:
                canvestodrawon.delete(ov)
        elif side == 'R':
            canvestodrawon.delete("rightRec")
            for ov in rightOvals:
                canvestodrawon.delete(ov)
    del dupki_za_gcode[:]
    
    #Vzemi razmerite na stranata
    razmeri_na_elementa = izbranElement.razmeri
    if rotation == 0 or rotation == 2:
        element_x = float(razmeri_na_elementa['x'])
        element_y = float(razmeri_na_elementa['y'])
    else:
        element_x = float(razmeri_na_elementa['y'])
        element_y = float(razmeri_na_elementa['x'])
        
    #Nachertai elementa vurhu plota na machinata
    narisuvai_strana_na_plota(element_x, element_y, side, canvestodrawon, rotation)

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
        dupkiIzvunPlot = ima_li_dupki_izvun_plota(dupki_na_elementa, rotation, element_x, element_y)
        dupkaIzvunX = dupkiIzvunPlot['IzvunX']
        dupkaIzvunY = dupkiIzvunPlot['IzvunY']
            
    for dupka in dupki_na_elementa:
        if rotation == 0 or rotation == 2:
            d_x = float(dupka['x'])
            d_y = float(dupka['y'])
            d_r = float(dupka['r'])
        else:
            d_x = float(dupka['y'])
            d_y = float(dupka['x'])
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
        
        horizontOtvor = 0
        if dupka.has_key('t'):
            if dupka['t'] == 'H':
                horizontOtvor = 1
        
        if izlizaPoX == 0 and izlizaPoY == 0:     
            # Zapazi tochnite koordinati na dupkite za g-code
            dupka_za_gcode = {"x" : d_x, "y": d_y, "h" : dulbochina, "r" : d_r, "t" : horizontOtvor}
            dupki_za_gcode.append(dupka_za_gcode)
            
            narisuvai_dupka_na_plota(horizontOtvor, d_x, d_y, dulbochina, d_r, 0, side, canvestodrawon)
        else:
            narisuvai_dupka_na_plota(horizontOtvor, d_x, d_y, dulbochina, d_r, 1, side, canvestodrawon)        

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

def pokaji_suzdai_detail_window():
    imeValue = StringVar()
    duljinaValue = StringVar()
    shirinaValue = StringVar()
    debelinaValue = StringVar()

    top = Toplevel()
    top.title(detailTitleText)
        
    imeLabel = Label(top, text=detailImeText)
    imeLabel.grid(row=0, padx=10, pady=10, sticky=W)
    imeEntry = Entry (top, textvariable=imeValue, width=30)
    imeEntry.grid(row=0, column=1, padx = 5, sticky=W)
    
    razmeriLabelBox = LabelFrame(top, text=detailRazmeriText)
    razmeriLabelBox.grid(row=1, columnspan=2, padx = 10, pady=10, sticky=W+E)
    duljinaLabel = Label(razmeriLabelBox, text=detailDuljinaText)
    duljinaLabel.grid(row=0, sticky=W)
    duljinaEntry = Entry(razmeriLabelBox, textvariable=duljinaValue)
    duljinaEntry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    shirinaLabel = Label(razmeriLabelBox, text=detailShirinaText)
    shirinaLabel.grid(row=1, sticky=W)
    shirinaEntry = Entry(razmeriLabelBox, textvariable=shirinaValue)
    shirinaEntry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    debelinaLabel = Label(razmeriLabelBox, text=detailDebelinaText)
    debelinaLabel.grid(row=2, sticky=W)
    debelinaEntry = Entry(razmeriLabelBox, textvariable=debelinaValue)
    debelinaEntry.grid(row=2, column=1, padx = 5, pady = 2, sticky=E)
    
    def zapazi_nov_detail():
        dupki_blank = []
        # Narochno sa oburnati X,Y zashtoto orientacia xy ot BXF oznachva oburnati X,Y ...Taka che ne promenqi tuk!
        razmer_x = float(duljinaValue.get())
        razmer_y = float(shirinaValue.get())
        debelina = float(debelinaValue.get())
        razmeri_map = {"x" : razmer_x, "y": razmer_y, "h":debelina}
        detail = ElementZaDupchene(imeValue.get(), razmeri_map, dupki_blank)
        ekey = 'customdetail'+imeValue.get()
        elementi_za_dupchene[ekey] = detail
        prevod_za_elemnti_v_list[ekey] = u'Въведен детайл: '+imeValue.get()+'..... '+str(razmer_x)+' x '+str(razmer_y)
        
        prevod = prevod_za_elemnti_v_list[ekey]
        listbox.insert(END, prevod)

        top.destroy()
    
    okbutton = Button(top, text=okButtonText, command=zapazi_nov_detail)
    okbutton.grid(row=2, padx = 10, pady = 10, sticky = W)
    cancelButton = Button(top, text=cancelButtonText, command=top.destroy)
    cancelButton.grid(row=2, column=1, pady = 10, sticky=W)
       
def reset_canvas():
    canvas.delete(ALL)
    canvas.create_rectangle(20, 20, PLOT_NA_MACHINA_X*mashtab+20, PLOT_NA_MACHINA_Y*mashtab+20, fill="bisque")
    for side in izbrani_elementi.keys():
        if side == 'L':
            narisuvai_element_na_plota(izbrani_elementi[side], izbrani_elementi[side+'O'], side, canvas, 0)
       
        if side == 'R':
            narisuvai_element_na_plota(izbrani_elementi[side], izbrani_elementi[side+'O'], side, canvas, 0)
            
def redaktirai_lqv_detail():
    global izbranElementZaRedakciaInd
    izbranElementZaRedakciaInd = 'L'
    pokaji_redaktirai_window('L')
    
def redaktirai_desen_detail():
    global izbranElementZaRedakciaInd
    izbranElementZaRedakciaInd = 'R'
    pokaji_redaktirai_window('R')
        
def pokaji_redaktirai_window(side):

    def on_closing():
        ramka.destroy()
        reset_canvas()
        
    def rotate_element_za_redakcia():
        rotate_element(side, rcanvas)

    def verikalenOtvorUI():
        for wid in frame1.grid_slaves():
            wid.grid_forget()
            
        lab = Label(frame1, text="Coming soon...", width= 50)
        lab.grid(row=0)
                
    def fiksUI():
        for wid in frame1.grid_slaves():
            wid.grid_forget()
        
        fiksFrame = Frame(ramka)
        fiksFrame.grid(row=2, sticky=N+S)
        
        paramFixLabelBox = LabelFrame(frame1, text=paramFixLabelText)
        paramFixLabelBox.grid(row=0, padx=5, pady=15, sticky=W+E)
        
        xLabel = Label(paramFixLabelBox, text=otstoqniePoXLabelText)
        xLabel.grid(row=1, sticky=W)
        xEntry = Entry(paramFixLabelBox, textvariable=fiksXValue)
        xEntry.grid(row=1, column=1, padx = 2, pady = 2, sticky=E)
        yLabel = Label(paramFixLabelBox, text=otstoqniePoYLabelText)
        yLabel.grid(row=2, sticky=W)
        yEntry = Entry(paramFixLabelBox, textvariable=fixYValue)
        yEntry.grid(row=2, column=1, padx = 2, pady = 2, sticky=E)
        diamXLabel = Label(paramFixLabelBox, text=diameturVertikalenOtvorXLabelText)
        diamXLabel.grid(row=3, sticky=W)
        diamXEntry = Entry(paramFixLabelBox, textvariable=fiksDiamturVerikalenOValue)
        diamXEntry.grid(row=3, column=1, padx = 2, pady = 2, sticky=E)       
        dulbXLabel = Label(paramFixLabelBox, text=dulbochinaVertikalenOtvorLabelText)
        dulbXLabel.grid(row=4, sticky=W)
        dulbXEntry = Entry(paramFixLabelBox, textvariable=fiksDulbochinaVerikalenOValue)
        dulbXEntry.grid(row=4, column=1, padx = 2, pady = 2, sticky=E)
        diamYLabel = Label(paramFixLabelBox, text=diameturHorizontOtvorLabelText)
        diamYLabel.grid(row=5, sticky=W)
        diamYEntry = Entry(paramFixLabelBox, textvariable=fiksDiamturHorizontOValue)
        diamYEntry.grid(row=5, column=1, padx = 2, pady = 2, sticky=E)
        dulbYLabel = Label(paramFixLabelBox, text=dulbochinaHorizontOtvorYLabelText)
        dulbYLabel.grid(row=6, sticky=W)
        dulbYEntry = Entry(paramFixLabelBox, textvariable=fiksDulbochinaHorizontOValue)
        dulbYEntry.grid(row=6, column=1, padx = 2, pady = 2, sticky=E)
        
        copyPoXCheckBox = Checkbutton(frame1, text=kopiraiPoXSimetrichnoLabelText, variable=simetrichnoPoXValue)
        copyPoXCheckBox.grid(row=1, sticky=W)
        copyPoYCheckBox = Checkbutton(frame1, text=kopiraiPoYSimetrichnoLabelText, variable=simetrichnoPoYValue)
        copyPoYCheckBox.grid(row=2, sticky=W)
        centralenFiksCheckBox = Checkbutton(frame1, text=centralenFixLabelText, variable=centralenFiksValue)
        centralenFiksCheckBox.grid(row=3, sticky=W)
        copyCentralenFiksCheckBox = Checkbutton(frame1, text=copyCentralenFixLabelText, variable=copyCentralenFixValue)
        copyCentralenFiksCheckBox.grid(row=4, sticky=W)
        
        postaviFixButton = Button(frame1, text=postaviFixLabelText, width=20, command=postavi_fiks)
        postaviFixButton.grid(row=5, padx = 5, pady = 5, sticky=E)
        otkajiFixButton = Button(frame1, text=stupkaNazadLabelText, width=20)
        otkajiFixButton.grid(row=6, padx = 5, pady = 5, sticky=E)
        izchistiFixButton = Button(frame1, text=izchistiFixoveLabelText, width=20)
        izchistiFixButton.grid(row=7, padx = 5, pady = 5, sticky=E)
        zapaziiFixButton = Button(frame1, text=zapaziFixoveLabelText, width=20)
        zapaziiFixButton.grid(row=8, padx = 5, pady = 5, sticky=E)
    
    def postavi_fiks():
        
        # TODO: PROVERKA DALI VECHE IMA TAKAVA DUPKA. DA NE SE DOBAVQ EDNA I SUSHTA DUPKA V LISTA!!!
        zyl_pos_x = float(fiksXValue.get())
        zyl_pos_y = float(fixYValue.get())

        zyl_h = float(fiksDulbochinaVerikalenOValue.get())
        zyl_r = float(fiksDiamturVerikalenOValue.get())/2.0
        zyl_h_hor = float(fiksDulbochinaHorizontOValue.get())
        zyl_r_hor = float(fiksDiamturHorizontOValue.get())/2.0
        
        simPoX = simetrichnoPoXValue.get()
        simPoY = simetrichnoPoYValue.get()
        centFix = centralenFiksValue.get()
        copyCentFix = copyCentralenFixValue.get()
        
        izbranElement = izbrani_elementi[izbranElementZaRedakciaInd]
        rotation = izbrani_elementi[izbranElementZaRedakciaInd+'O']
        
        dupki_na_elementa = izbranElement.dupki
        razmeri_na_elementa = izbranElement.razmeri
        if rotation == 0 or rotation == 2:
            element_x = float(razmeri_na_elementa['x'])
            element_y = float(razmeri_na_elementa['y'])
        else:
            element_x = float(razmeri_na_elementa['y'])
            element_y = float(razmeri_na_elementa['x'])
        
        # Purvate dupka (obiknoveno 100 x 34) 
        # Ne se dobavq SAMO AKO edinstventa otmetka izbrana e Centralen Fix 
        if (simPoX == 0 and simPoY == 0 and centFix == 0 and copyCentFix == 0) or simPoX == 1 or simPoY == 1: 
            if rotation == 0:
                dupka1  = {"x" : zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
                #dupka1a  = {"x" : zyl_pos_x, "y": 0, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H"}
                #dupka1b  = {"x" : zyl_pos_x+32, "y": 0, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H"}
            elif rotation == 1:
                dupka1 = {"x" : zyl_pos_y, "y": element_x - zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 2:
                dupka1 = {"x" : element_x-zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 3:
                dupka1 = {"x" : element_y-zyl_pos_y, "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
    
            dupki_na_elementa.append(dupka1)
            #dupki_na_elementa.append(dupka1a)
            #dupki_na_elementa.append(dupka1b)
        
        if simPoX == 1:
            # Vtorata dupka po X (ogledalna na dupka)
            if rotation == 0:
                dupka2 = {"x" : element_x-zyl_pos_x, "y":zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 1:
                dupka2 = {"x" : zyl_pos_y, "y": zyl_pos_x,  "h" : zyl_h, "r" : zyl_r}
            elif rotation == 2:
                dupka2 = {"x" : zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 3:
                dupka2 = {"x" : element_y-zyl_pos_y, "y": element_x-zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            dupki_na_elementa.append(dupka2)
        
        if simPoY == 1:
            # Vtorata dupka po Y (ogledalna na dupka)
            if rotation == 0:
                dupka3 = {"x" : zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 1:
                dupka3 = {"x" : element_y-zyl_pos_y, "y": element_x-zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 2:
                dupka3 = {"x" : element_x-zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 3:
                dupka3 = {"x" : zyl_pos_y, "y": zyl_pos_x,  "h" : zyl_h, "r" : zyl_r}
            dupki_na_elementa.append(dupka3)
            
        if simPoX == 1 and simPoY == 1:
            if rotation == 0:
                dupka4 =  {"x" : element_x-zyl_pos_x, "y": element_y- zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 1:
                dupka4 = {"x" : element_y-zyl_pos_y, "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 2:
                dupka4 = {"x" : zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 3:
                dupka4 = {"x" : zyl_pos_y, "y": element_x-zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            dupki_na_elementa.append(dupka4)

        if centFix == 1:
            center_zyl_pos_x = element_x/2
             
            if rotation == 0:
                dupka5 = {"x" : center_zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 1:
                dupka5 = {"x" : zyl_pos_y, "y": center_zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 2:
                dupka5 = {"x" : center_zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 3:
                dupka5 = {"x" : element_y-zyl_pos_y, "y": center_zyl_pos_x, "h" : zyl_h, "r" : zyl_r}            
            dupki_na_elementa.append(dupka5) 
        
        if copyCentFix == 1:
            center_zyl_pos_x = element_x/2
            
            if rotation == 0:
                dupka6 = {"x" : center_zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 1:
                dupka6 = {"x" : element_y-zyl_pos_y, "y": center_zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 2:
                dupka6 = {"x" : center_zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r}
            elif rotation == 3:
                dupka6 = {"x" : zyl_pos_y, "y": center_zyl_pos_x, "h" : zyl_h, "r" : zyl_r}  
            dupki_na_elementa.append(dupka6) 

        print dupki_na_elementa
        # Narisuvai
        rcanvas.delete(ALL)
        narisuvai_element_na_plota(izbranElement, izbrani_elementi[izbranElementZaRedakciaInd+'O'], izbranElementZaRedakciaInd, rcanvas, 0)
        
    ramka = Toplevel()
    ramka.title(editButtonText)
    ramka.protocol("WM_DELETE_WINDOW", on_closing)
         
    rtoolbar = Frame(ramka, bg="honeydew")
    rtoolbar.grid(row=0, columnspan=2, sticky=W+E)
    dLabel = Label(rtoolbar, text=detailTitleText)
    dLabel.grid(row=0, padx=10, pady=5,sticky=W)
    iLabel = Label(rtoolbar, text='')
    iLabel.grid(row=0, column=1, pady=5, sticky=W)
    
    buttonFrame = Frame(ramka)
    buttonFrame.grid(row=1, columnspan=2, sticky=W)
    fixButton = Button(buttonFrame, text=dobaviFixLabelText, command=fiksUI)
    fixButton.grid(row=0, padx = 2, pady = 2, sticky=W)
    verikalenOtvorButton = Button(buttonFrame, text=dobaviVerOtvorLabelText, command=verikalenOtvorUI)
    verikalenOtvorButton.grid(row=0, column=1, padx = 2, pady = 2,sticky=W)
    horizontalenOtvorButton = Button(buttonFrame, text=dobaviHorOtvorLabelText, command=verikalenOtvorUI)
    horizontalenOtvorButton.grid(row=0, column=2, padx = 2, pady = 2, sticky=W)
    pantaButton = Button(buttonFrame, text=dobaviPantaLabelText, command=verikalenOtvorUI)
    pantaButton.grid(row=0, column=3, padx = 2, pady = 2, sticky=W)
    zavurtiButton = Button(buttonFrame, text=rotateButtonText, bg="lightblue", command=rotate_element_za_redakcia)
    zavurtiButton.grid(row=0, column=4, padx = 2, pady = 2, sticky=W)
    
    frame1 = Frame(ramka)
    frame1.grid(row=2, sticky=N+S)
    label1 = Label(frame1, text=izbereteOpciaLabelText, width= 50)
    label1.grid(row=0, pady = 20)
    
    rcanvas = Canvas(ramka, width=1000, heigh=700, bg="grey")
    rcanvas.grid(row=2, column=1, padx=20, sticky=W+E+N+S)
    
    # Narisuvai elementa na plota
    narisuvai_element_na_plota(izbrani_elementi[side], izbrani_elementi[side+'O'], side, rcanvas, 0)
       
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

leftBazaCheckBox = IntVar()
rightBazaCheckBox = IntVar()

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

''' ***************************************************************************
*** Variables za stoinosti na fiksovete
*************************************************************************** '''
fiksXValue = StringVar()
fixYValue = StringVar()
fiksDiamturVerikalenOValue = StringVar()
fiksDulbochinaVerikalenOValue = StringVar()
fiksDiamturHorizontOValue = StringVar()
fiksDulbochinaHorizontOValue = StringVar()
simetrichnoPoXValue = IntVar()
simetrichnoPoYValue = IntVar()
centralenFiksValue = IntVar()
copyCentralenFixValue = IntVar()

# Default values (she doidat posle of file)
fiksXValue.set('100')
fixYValue.set('34')
fiksDiamturVerikalenOValue.set('15')
fiksDulbochinaVerikalenOValue.set('14')
fiksDiamturHorizontOValue.set('8')
fiksDulbochinaHorizontOValue.set('28')
        
        
# ********** File Menu *************
mainMenu = Menu(mainframe)
mainframe.config(menu=mainMenu)
fileManu = Menu(mainMenu)
fileManu.add_command(label="Open", command=zaredi_file_info)
mainMenu.add_cascade(label="File", menu=fileManu)

# ********** Toolbar *************
toolbar = Frame(mainframe, bg="honeydew")
toolbar.grid(row=0, columnspan=4, sticky=W+E)

openButton = Button(toolbar, text=openBXFFileButtonText, command=zaredi_file_info)
openButton.grid(row=0, column=0, padx=10, pady=2,  sticky=W)
orLabel = Label(toolbar, text=orLabelText)
orLabel.grid(row=0, column=1, padx=10, pady=2,  sticky=W)
createButton = Button(toolbar, text=createButtonText, command=pokaji_suzdai_detail_window)
createButton.grid(row=0, column=2, padx=10, pady=2,  sticky=W)
fileNameLabel = Label(toolbar, text="")
fileNameLabel.grid(row=0, column=3, padx=10, pady=2,  sticky=W)


# ********** Rotate Button *************
leftBazaLabelBox = LabelFrame(mainframe, text=leftBazaGrouperText)
leftBazaLabelBox.grid(row=1, column=2, sticky=W, padx=20, pady=2)
rotateButtonLeftBaza = Button(leftBazaLabelBox, text=rotateButtonText, bg="lightblue", command=rotate_element_lqva_baza)
rotateButtonLeftBaza.grid(row=0, sticky=W, padx=2, pady=2)
removeElementButtonLeftBaza = Button(leftBazaLabelBox, text=removeButtonText, bg="lightblue", command=mahni_element_ot_lqva_baza)
removeElementButtonLeftBaza.grid(row=0, column=1, sticky=W, padx=2, pady=2)
editButtonLeftBaza = Button(leftBazaLabelBox, text=editButtonText, bg="lightblue", command=redaktirai_lqv_detail)
editButtonLeftBaza.grid(row=0, column=2, sticky=W, padx=2, pady=2)

rightBazaLabelBox = LabelFrame(mainframe, text=rightBazaGrouperText)
rightBazaLabelBox.grid(row=1, column=3, sticky=W, padx=20, pady=2)
rotateButtonRightBaza = Button(rightBazaLabelBox, text=rotateButtonText, bg="lightblue", command=rotate_element_dqsna_baza)
rotateButtonRightBaza.grid(row=0, sticky=W, padx=2, pady=2)
removeElementButtonRightBaza = Button(rightBazaLabelBox, text=removeButtonText, bg="lightblue", command=mahni_element_ot_dqsna_baza)
removeElementButtonRightBaza.grid(row=0, column=1, sticky=W, padx=2, pady=2)
editButtonRightBaza = Button(rightBazaLabelBox, text=editButtonText, bg="lightblue", command=redaktirai_desen_detail)
editButtonRightBaza.grid(row=0, column=2, sticky=W, padx=2, pady=2)

# ********** Listbox *************
listbox = Listbox(mainframe, width=50)
listbox.grid(row=2, sticky=N+S, padx=10)

# ********** Frame *************
frame = Frame(mainframe)
frame.grid(row=2, column=1, sticky=N+S)

# ********** Move Button *************
slojiLqvaBazaButton = Button(frame, text=placeOnMachineButtonText, bg="bisque", command=izberi_element_za_lqva_strana)
slojiLqvaBazaButton.grid(row=0, padx = 3, sticky=N)

slojiDqsnaBazaButton = Button(frame, text=placeOnMachineRightButtonText, bg="bisque", command=izberi_element_za_dqsna_strana)
slojiDqsnaBazaButton.grid(row=0, column=1, padx = 3, sticky=N)

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
canvas.grid(row=2, column=2, columnspan = 2, padx=20, sticky=W+E+N+S)

# ********** Masa *************
# Originalen razmer e 1500 mm na 600 mm. Mashtab (x 0.5) => duljinata e 750 i shirina e 300.
# Sledovatelno koordinatite she sa offset s nachalnata tochka. (+20)
masa = canvas.create_rectangle(20, 20, PLOT_NA_MACHINA_X*mashtab+20, PLOT_NA_MACHINA_Y*mashtab+20, fill="bisque")


mainframe.mainloop()

print ('*** END PROGRAM *************************')
