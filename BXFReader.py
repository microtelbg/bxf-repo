#!/usr/bin/python
# -*- coding: utf-8 -*-
import time, os
## dd/mm/yyyy format
#import gettext

from Tkinter import *
import tkMessageBox
from tkFileDialog import askopenfilename,asksaveasfilename
from ConfigReader import read_instruments,write_instruments,sort_detail_list,write_param_za_otvori,read_param_za_otvori
from Optimizacii import optimizirai_otvori, is_dupka_duplicate

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

# Set up message catalog access
#t = gettext.translation('BXFReader', 'locale', fallback=True)
#_ = t.ugettext

''' ***************************************************************************
*** Labels
*************************************************************************** '''
rotateButtonText = u'Завърти'
removeButtonText = u'Премахни'
editButtonText = u'Редактирай'
pripluzniButtonText = u'<-- Приплъзни -->'
orLabelText = u' или '
openBXFFileButtonText = u'Отвори BXF файл'
createButtonText = u'Създай елемент'
placeOnMachineButtonText = u'Постави на ЛЯВА база'
placeOnMachineRightButtonText = u'Постави на ДЯСНА база'
leftBazaGrouperText = u'ЛЯВА база'
rightBazaGrouperText = u'ДЯСНА база'
nastroikaInstrumentButtonText = u'Настройка на инструменти'
vertikalnaGlavaText =  u'Вертикална глава'
horizontalnaGlavaText =  u'Хоризонтална глава'
instrument1LabelText = u'Инструмент 1'
instrument2LabelText = u'Инструмент 2'
instrument3LabelText = u'Инструмент 3'
instrument4LabelText = u'Инструмент 4'
instrument5LabelText = u'Инструмент 5'
diameturLabelText = u'Диаметър (мм)'
skorostText = u'Скорост (мм/мин)'
zapaziInstrFileButtonText = u'Запази настройки'
zatvoriButtonText = u'Затвори'
generateGCodeLabelText =  u'Генериране на G код'
generateGCodeButtonText = u'Генерирай G код'
iztriiGCodeButtonText = u'Изтрий G код'
zapisGCodeButtonText =  u'Запиши G код'
genHorizontOtvoriButtonText = u'Добави код за хоризонталните отвори'
genVertikalOtvoriButtonText = u'Добави код за вертикалните отвори'
pauseMejduDetailiButtonText = u'Постави пауза между левия и десния детайл'
ciklichnoPrezarejdaneButtonText = u'Презареди кода циклично'
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
raztoqnieMejduOtvori = u'Разстояние между отвори'
broiOtvori = u'Брой отвори'
paramFixLabelText = u'Параметри на фикс'
paramVertikalenOtvorText = u'Параметри на вертикален отвор'
paramHorizontalenOtvorText = u'Параметри на хоризонтален отвор'
otstoqniePoXLabelText = u'Отстояние по хоризонтал'
otstoqniePoYLabelText = u'Отстояние по вертикал'
dulbochinaVertikalenOtvorLabelText = u'Вертикален отвор - Дълбочина'
dulbochinaHorizontOtvorYLabelText = u'Хоризонтален отвор - Дълбочина'
diameturVertikalenOtvorXLabelText = u'Вертикален отвор - Диаметър'
diameturHorizontOtvorLabelText = u'Хоризонтален отвор - Диаметър'
kopiraiPoXSimetrichnoLabelText = u'Добави фикс симетрично по ХОРИЗОНТАЛ'
kopiraiPoYSimetrichnoLabelText = u'Добави фикс симетрично по ВЕРТИКАЛ'
kopiraiOtvorPoXSimetrichnoLabelText = u'Добави отвор симетрично по ХОРИЗОНТАЛ'
kopiraiOtvorPoYSimetrichnoLabelText = u'Добави отвор симетрично по ВЕРТИКАЛ'
centralenFixLabelText = u'Постави централен фикс'
copyCentralenFixLabelText = u'Добави огледален централен фикс'
postaviFixLabelText = u'Постави фикс'
stupkaNazadLabelText = u'Стъпка назад'
izchistiFixoveLabelText = u'Изчисти фиксове' 
zapaziFixoveLabelText = u'Запази фиксове'
postaviOtvorText = u'Постави отвори'
izchistiOtvoriText =  u'Изчисти отвори' 
zapaziOtvoriText = u'Запази отвори'
izbereteOpciaLabelText = u'Изберете опция за редактиране ...'
iztriiButtonText = u'Изтрий'
izchistiVsichkoButtonText = u'Изтрий всички детайли'
izchistiIzbranDetailButtonText =u'Изтрий избран детайл'
detailiLabelText = u'Детайли'

''' ***************************************************************************
*** Constants
*************************************************************************** '''
ns = {'blum' : 'http://www.blum.com/bxf'}
mashtab = 0.45

PLOT_NA_MACHINA_X = 1504
PLOT_NA_MACHINA_Y = 600

''' ***************************************************************************
*** Global Variables
*************************************************************************** '''
detNo = 1
bezopasno_z = "{0:.3f}".format(20.000) # Tova she bude izchesleno kato debelinata na materiala ot bxf + 20
TT = '' # instrumenta v momenta T1, T2, etc.
n10 = 30
gcodeInProgress = 0
# Elementi svurzani s SAMO s grafikata
leftOvals = []
rightOvals = []

#Vsichi elementi of BXF faila za dupchene
elementi_za_dupchene = {}

theSortedList = []

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
dupki_za_gcode_left = []
dupki_za_gcode_right = []

prevod_za_elemnti_v_list = {}

stepsList = None

class ElementZaDupchene(object):
    def __init__(self, ime, razmeri, dupki):
        self.ime = ime
        self.razmeri = razmeri
        self.dupki = dupki
        self.purvonachalnoPolojenie = ''
#         if debelina <= 0.0:
#             self.debelina = 18.0
#         else:
#             self.debelina = debelina

    def set_purvonachalno_polojenie(self, purvonachalnoPolojenie):
        self.purvonachalnoPolojenie = purvonachalnoPolojenie
        
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
    
    global detNo

    suzdai_element_duno_gornica(myroot, elementi_za_dupchene, 'Oberboden', detNo)
    suzdai_element_duno_gornica(myroot, elementi_za_dupchene, 'Unterboden', detNo)
    suzdai_element_grub(myroot, elementi_za_dupchene, 'KorpusRueckwand', detNo)
    suzdai_element_strana(myroot, elementi_za_dupchene, 'LinkeSeitenwand', detNo)
    suzdai_element_strana(myroot, elementi_za_dupchene, 'RechteSeitenwand', detNo)
    suzdai_element_vrata(myroot, elementi_za_dupchene, 'Tuer', detNo)
    suzdai_element_vrata(myroot, elementi_za_dupchene, 'Doppeltuer', detNo)
    suzdai_element_shkafche(myroot, elementi_za_dupchene, 'Aussenschubkasten', detNo)
    suzdai_element_vrata(myroot, elementi_za_dupchene, 'Klappensystem', detNo)
    
    detNo = detNo + 1
    
''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     KorpusRueckwand (grub na korpusa)
     Y and Z
*******************************************************************************'''        
def suzdai_element_grub(root, elements, name, bxfNo):
    parenttag = 'blum:'+name
    
    parent = root.find(parenttag, ns)
    if parent is not None:
        # Orientacia e YZ, X e debelina
        quader = parent.findall('.//blum:Quader', ns)
        if len(quader) > 0:
            hoehe = quader[0].find('blum:Hoehe', ns)
            if hoehe is not None:
                razmer_z = hoehe.text
            else:
                razmer_z = 0
                print 'Greshka - Hoehe tag ne e nameren za ', name
            
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
            razmer_debelina = float(pointc_x) - float(pos_x)
            razmer_y = float(pointc_y) - float(pos_y)
            
            #Dupki
            dupki_map = suzdai_dupki(quader, 'yz', razmer_y, razmer_z, name)
            
            #Create object
            razmeri_map = {"x" : razmer_y, "y": razmer_z , "h":razmer_debelina}

            grub = ElementZaDupchene(name, razmeri_map, dupki_map)
            elements['DET:'+str(bxfNo)+'KorpusRueckwand'] = grub
        else:
            print 'Greshka -Quader tag ne e namer za ', name

        
''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     LinkeSeitenwand (lqva strana)
     RechteSeitenwand (dqsna strana)
     X and Z
*******************************************************************************'''
def suzdai_element_strana(root, elements, name, bxfNo):
    parenttag = 'blum:'+name
    parent = root.find(parenttag, ns) #Namira samo 1 element s tozi tag. Predpolagam che samo 1 ima v bxf
    if parent is not None:
        # Orientacia e XZ, Y e debelina
        quader = parent.findall('.//blum:Quader', ns)
        if len(quader) > 0:
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
            dupki_map = suzdai_dupki(quader, 'xz', razmer_z, razmer_x, name)
            
            #Create object
            razmeri_map = {"x" : razmer_z, "y": razmer_x , "h":razmer_debelina}
    
            stana = ElementZaDupchene(name, razmeri_map, dupki_map)
            if name == 'LinkeSeitenwand':
                elements['DET:'+str(bxfNo)+'LinkeSeitenwand'] = stana
            elif  name == 'RechteSeitenwand':
                elements['DET:'+str(bxfNo)+'RechteSeitenwand'] = stana
            else:
                elements['DET:'+str(bxfNo)+name] = stana
        else:
            print 'Greshka -Quader tag ne e namer za ', name

    else:
        print name, " ne e nameren takuv tag"

''' ***************************************************************************
**** Tazi funkcia chete parametrite za dupkite
*******************************************************************************'''
def suzdai_dupki(curparent, orientation, element_x, element_y, imeNaElement):
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
                if imeNaElement == 'Unterboden':
                    dupki = {"x" : zyl_pos_y, "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
                elif imeNaElement == 'Oberboden':
                    dupki = {"x" : float(zyl_pos_y), "y": float(element_y) - float(zyl_pos_x), "h" : zyl_h, "r" : zyl_r}
                else:
                    dupki = {"x" : zyl_pos_y, "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
            elif orientation == 'yz':
                dupki = {"x" : zyl_pos_y, "y": float(zyl_pos_z), "h" : zyl_h, "r" : zyl_r}
            elif orientation == 'xz':
                if imeNaElement == 'LinkeSeitenwand':
                    dupki = {"x" : float(element_x) - float(zyl_pos_z), "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
                elif imeNaElement == 'RechteSeitenwand':
                    dupki = {"x" : float(zyl_pos_z), "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}
                else:
                    dupki = {"x" : float(zyl_pos_z), "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r}

            dupki_list.append(dupki)
    return dupki_list

''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     Oberboden(gornica)
     Unterboden(duno)
*******************************************************************************'''
def suzdai_element_duno_gornica(root, elements, name, bxfNo):
    parenttag = './/blum:'+name
    parents = root.findall(parenttag, ns) #Namira vsichki tags 
    for parent in parents:
        if name == 'Aussenschubkasten':
            parentName = parent.attrib['Name']
        else:
            parentName = ''
        boden = parent.findall('.//blum:Boden', ns)
        for duno in boden:
            dunoID = duno.attrib['ID']
            quader = duno.findall('.//blum:Quader', ns)

            if len(quader) > 0:
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
                dupki_map = suzdai_dupki(quader, 'xy', razmer_y, razmer_x, name)
    
                #Create object
                razmeri_map = {"x" : razmer_y, "y": razmer_x, "h":razmer_debelina}
    
                plot = ElementZaDupchene(name, razmeri_map, dupki_map)
    
                if name == 'Oberboden':
                    elements['DET:'+str(bxfNo)+'Oberboden-'+dunoID] = plot
                    #prevod_za_elemnti_v_list['Oberboden-'+dunoID] = u'Горен плот ('+str(dunoID)+')'+str(razmer_y)+' x '+str(razmer_x)
                elif name == 'Unterboden':
                    elements['DET:'+str(bxfNo)+'Unterboden-'+dunoID] = plot
                    #prevod_za_elemnti_v_list['Unterboden-'+dunoID] = u'Долен плот ('+str(dunoID)+')'+str(razmer_y)+' x '+str(razmer_x)
                elif name == 'Aussenschubkasten':
                    elements['DET:'+str(bxfNo)+'Aussenschubkasten-'+parentName+'-Boden-'+dunoID] = plot
                else:
                    elements['DET:'+str(bxfNo)+name] = plot
                    #prevod_za_elemnti_v_list[name] = name
            else:
                print 'Greshka -Quader tag ne e namer za ', name

    else:
        print name, " ne e nameren takuv tag"

''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     Aussenschubkasten(vunshno shkafche)
     Innenschubkasten (vutreshno shkafche)
*******************************************************************************'''
def suzdai_element_shkafche(root, elements, name, bxfNo):
    #Prednata chast na shkafcheto e sushtata kato vratichka
    suzdai_element_vrata(root, elements, name, bxfNo)
    #Dunoto na shkafcheto
    suzdai_element_duno_gornica(root, elements, name, bxfNo)

    #Dunoto chast na shkafcheto
    parenttag = './/blum:'+name
    parents = root.findall(parenttag, ns) #Namira vsichki tags
    for parent in parents:
        parentName = parent.attrib['Name']
        
        duna = parent.findall('.//blum:Holzschubkasten', ns)
        for duno in duna:
            dunoID = duno.attrib['ID']
            quader = duno.findall('.//blum:Quader', ns)

            if len(quader) > 0:
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
                dupki_map = suzdai_dupki(quader, 'xy', razmer_y, razmer_x, name)

                #Create object
                razmeri_map = {"x" : razmer_y, "y": razmer_x, "h":razmer_debelina}

                dunoShkafche = ElementZaDupchene(name, razmeri_map, dupki_map)

                if name == 'Aussenschubkasten':
                    elements['DET:'+str(bxfNo)+'Aussenschubkasten-'+parentName+'-Holzschubkasten-'+dunoID] = dunoShkafche
                else:
                    elements['DET:'+str(bxfNo)+name] = dunoShkafche

            else:
                print 'Greshka -Quader tag ne e namer za ', name


        rueckwands = parent.findall('.//blum:Rueckwand', ns)
        for rueckwand in rueckwands:
            rueckwandID = rueckwand.attrib['ID']
            quader = rueckwand.findall('.//blum:Quader', ns)

            if len(quader) > 0:
                # <Hoehe>0.0</Hoehe> visochina
                hoehe = quader[0].find('blum:Hoehe', ns)
                if hoehe is not None:
                    razmer_z = hoehe.text
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
                razmer_debelina = float(pointc_x) - float(pos_x)
                razmer_y = float(pointc_y) - float(pos_y)

                #Dupki
                dupki_map = suzdai_dupki(quader, 'yz', razmer_y, razmer_z, name)

                #Create object
                razmeri_map = {"x" : razmer_y, "y": razmer_z, "h":razmer_debelina}

                rueckwandShkafche = ElementZaDupchene(name, razmeri_map, dupki_map)

                if name == 'Aussenschubkasten':
                    elements['DET:'+str(bxfNo)+'Aussenschubkasten-'+parentName+'-Rueckwand-'+rueckwandID] = rueckwandShkafche
                    prevod_za_elemnti_v_list['Aussenschubkasten-'+parentName+'-Rueckwand-'+rueckwandID] = u'Чекмедже-'+parentName+'Rueckwand-'+rueckwandID+str(razmer_y)+' x '+str(razmer_z)
                else:
                    elements['DET:'+str(bxfNo)+name] = rueckwandShkafche
                    prevod_za_elemnti_v_list[name] = name+str(razmer_x)+' x '+str(razmer_y)

            else:
                print 'Greshka -Quader tag ne e namer za ', name
''' ***************************************************************************
**** Izpolzvai tazi funkcia za:
     Tuer(edinichka vratichka)
     Doppeltuer (dvoina vratichka)
     Aussenschubkasten (samo chast - prednata chast na shkafcheto)
*******************************************************************************'''
def suzdai_element_vrata(root, elements, name, bxfNo):
    parenttag = './/blum:'+name
    parents = root.findall(parenttag, ns) #Namira vsichki tags 
    for parent in parents:
        parentName = parent.attrib['Name']
        fronts = parent.findall('.//blum:Front', ns)
        for front in fronts:
            frontID = front.attrib['ID']
            quader = front.findall('.//blum:Quader', ns)

            if len(quader) > 0:
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
                dupki_map = suzdai_dupki(quader, 'yz', razmer_y, razmer_z, name)

                #Create object
                razmeri_map = {"x" : razmer_y, "y": razmer_z, "h" : razmer_debelina}

                vrata = ElementZaDupchene(name, razmeri_map, dupki_map)

                if name == 'Tuer':
                    ekey = 'DET:'+str(bxfNo)+'Tuer-'+parentName+'Front-'+frontID
                    elements[ekey] = vrata
                elif name == 'Doppeltuer':
                    ekey = 'DET:'+str(bxfNo)+'Doppeltuer-'+parentName+'Front-'+frontID
                    elements[ekey] = vrata
                elif name == 'Aussenschubkasten':
                    elements['DET:'+str(bxfNo)+'Aussenschubkasten-'+parentName+'-Front-'+frontID] = vrata
                elif name == 'Klappensystem':
                    elements['DET:'+str(bxfNo)+'Klappensystem-'+parentName+'Front-'+frontID] = vrata
                else:
                    elements['DET:'+str(bxfNo)+name] = vrata

            else:
                print 'Greshka -Quader tag ne e namer za ', name

def zaredi_file_info():
    myfilename = askopenfilename(filetypes=(("BXF files", "*.bxf"), ("All files", "*.*")))

    # 1. Procheti BXF file
    cheti_bxf_file(myfilename)

    # 2. Pokaji izbrania file
    fileNameLabel['text'] = myfilename

    global theSortedList
    theSortedList = sort_detail_list(elementi_za_dupchene)
    
    # 3. Populti lista s elementi
    listbox.delete(0, END)
    for ek in theSortedList:
        prevod = ek[1]
        listbox.insert(END, prevod)
    
    #Reset
    canvas.delete(ALL)
    canvas.create_rectangle(20, 20, PLOT_NA_MACHINA_X*mashtab+20, PLOT_NA_MACHINA_Y*mashtab+20, fill="bisque")

def izchisti_vschki_detaili():
    elementi_za_dupchene.clear()
    theSortedList[:]
    listbox.delete(0, END)
    if len(izbrani_elementi) > 0:
        if izbrani_elementi.has_key('L'):
            mahni_element_ot_lqva_baza()
        if izbrani_elementi.has_key('R'):
            mahni_element_ot_dqsna_baza()
        
def izchisti_izbrania_detail():  
    itemIndex = int(listbox.curselection()[0])
    itemValue = listbox.get(itemIndex)   
    iValue = itemValue   
    
    indexToDelete = 0
    for item in theSortedList:
        indexToDelete = indexToDelete + 1
        if itemValue == item[1]:
            iValue = item[2]
            break     
        
    if len(izbrani_elementi) > 0:
        if izbrani_elementi.has_key('L') and izbrani_elementi['L'] == elementi_za_dupchene[iValue]:
            mahni_element_ot_lqva_baza()
        if izbrani_elementi.has_key('R') and izbrani_elementi['R'] == elementi_za_dupchene[iValue]:
            mahni_element_ot_dqsna_baza()
                  
    del elementi_za_dupchene[iValue]            
    del theSortedList[indexToDelete]
   
    listbox.delete(ANCHOR)
       
def izberi_element_za_dupchene(side, orienation, pripluzvane):
    
    if pripluzvane == 1:
        if side == 'L':
            narisuvai_element_na_plota(izbrani_elementi['L'], orienation, 'L', canvas, 1, 1)
        else:
            narisuvai_element_na_plota(izbrani_elementi['R'], orienation, 'R', canvas, 1, 1)
        
    else:
        #Nameri izbrania element
        itemIndex = int(listbox.curselection()[0])
        itemValue = listbox.get(itemIndex)
        iValue = itemValue
        
        for item in theSortedList:
            if itemValue == item[1]:
                iValue = item[2]
                break
    
        izbranElement = elementi_za_dupchene[iValue]
        izbranElement.purvonachalnoPolojenie = ''
        
        if side == 'L':
            #Sloji elementa v lista i purvonachalnata orientacia
            izbrani_elementi['L'] = izbranElement
            izbrani_elementi['LO'] = orienation
            narisuvai_element_na_plota(izbranElement, orienation, 'L', canvas, 1, 0)
        elif side == 'R':
            #Sloji elementa v lista i purvonachalnata orientacia
            izbrani_elementi['R'] = izbranElement
            izbrani_elementi['RO'] = orienation
            narisuvai_element_na_plota(izbranElement, orienation, 'R', canvas, 1, 0)

def izberi_element_za_lqva_strana():
    izberi_element_za_dupchene('L', 0, 0)
    pripluzniButton.config(state="normal")

def izberi_element_za_dqsna_strana():
    izberi_element_za_dupchene('R', 0, 0)
    pripluzniButton.config(state="normal")

def narisuvai_strana_na_plota(stranaPoX, stranaPoY, side, canvestodrawon, rotation, pripluzvaneInd):
    
    borderLength = 30
    
    if side == 'L':
        detail = izbrani_elementi['L']
        color = "lightblue"
        purPol = 'L'
        if detail.purvonachalnoPolojenie == 'R':
            color = "lightgreen"
            purPol = 'R'
            
        canvestodrawon.create_rectangle(30, 30, stranaPoX*mashtab+30, stranaPoY*mashtab+30, fill=color, tags="leftRec")
                
        if pripluzvaneInd == 1 and purPol == 'R':   
            b1Coord = izbrani_elementi['LB1'] 
            b1_x1 = b1Coord[0]
            b1_y1 = b1Coord[1]
            b1_x2 = b1Coord[2]
            b1_y2 = b1Coord[3]
            
            b2Coord =  izbrani_elementi['LB2'] 
            b2_x1 = b2Coord[0]
            b2_y1 = b2Coord[1]
            b2_x2 = b2Coord[2]
            b2_y2 = b2Coord[3]
            
            #nachalenX = PLOT_NA_MACHINA_X*mashtab + stranaPoX*mashtab
            kraenX = stranaPoX*mashtab+20
            
            if rotation == 0:
                canvestodrawon.create_line(stranaPoX*mashtab, 28, stranaPoX*mashtab+30, 28, fill="purple", width=2, tags="border1")
                canvestodrawon.create_line(stranaPoX*mashtab+32, 30, stranaPoX*mashtab+32, borderLength+30, fill="purple",  width=2,tags="border2")
            elif rotation == 1:
                canvestodrawon.create_line(stranaPoX*mashtab+32, stranaPoY*mashtab, stranaPoX*mashtab+32, stranaPoY*mashtab+30, fill="purple", width=2, tags="border2")
                canvestodrawon.create_line(stranaPoX*mashtab, stranaPoY*mashtab+32, stranaPoX*mashtab+30, stranaPoY*mashtab+32, fill="purple", width=2, tags="border1")
            elif rotation == 2:
                canvestodrawon.create_line(28, stranaPoY*mashtab, 28, stranaPoY*mashtab+30, fill="purple", width=2, tags="border2")
                canvestodrawon.create_line(30, stranaPoY*mashtab+32, borderLength+30, stranaPoY*mashtab+32, fill="purple", width=2, tags="border1")  
            elif rotation == 3:
                canvestodrawon.create_line(30, 28, borderLength+30, 28, fill="purple", width=2, tags="border1")
                canvestodrawon.create_line(28, 30, 28, borderLength+30, fill="purple", width = 2, tags="border2")
                
                
#                 b1_x1 = kraenX - (PLOT_NA_MACHINA_X*mashtab- b1_x1) #nachalenX - b1_x1 - 18
#                 b1_x2 = b1_x1 + borderLength
#                 b2_x1 = kraenX - (PLOT_NA_MACHINA_X*mashtab- b2_x1)
#                 b2_x2 = b2_x1
#             
#                 canvestodrawon.create_line(b1_x1, b1_y1, b1_x2, b1_y2, fill="purple", width=2, tags="border1")
#                 canvestodrawon.create_line(b2_x1, b2_y1, b2_x2, b2_y2, fill="purple", width=2, tags="border2")
        
        else:
            if rotation == 0:
                canvestodrawon.create_line(30, 28, borderLength+30, 28, fill="purple", width=2, tags="border1")
                canvestodrawon.create_line(28, 30, 28, borderLength+30, fill="purple", width = 2, tags="border2")
            elif rotation == 1:
                canvestodrawon.create_line(stranaPoX*mashtab, 28, stranaPoX*mashtab+30, 28, fill="purple", width=2, tags="border1")
                canvestodrawon.create_line(stranaPoX*mashtab+32, 30, stranaPoX*mashtab+32, borderLength+30, fill="purple",  width=2,tags="border2")
            elif rotation == 2:
                canvestodrawon.create_line(stranaPoX*mashtab+32, stranaPoY*mashtab, stranaPoX*mashtab+32, stranaPoY*mashtab+30, fill="purple", width=2, tags="border2")
                canvestodrawon.create_line(stranaPoX*mashtab, stranaPoY*mashtab+32, stranaPoX*mashtab+30, stranaPoY*mashtab+32, fill="purple", width=2, tags="border1")
            elif rotation == 3:
                canvestodrawon.create_line(28, stranaPoY*mashtab, 28, stranaPoY*mashtab+30, fill="purple", width=2, tags="border2")
                canvestodrawon.create_line(30, stranaPoY*mashtab+32, borderLength+30, stranaPoY*mashtab+32, fill="purple", width=2, tags="border1")    
            
    elif side == 'R':
        detail = izbrani_elementi['R']
        color = "lightgreen"
        purPol = 'R'
        if detail.purvonachalnoPolojenie == 'L':
            color = "lightblue"
            purPol = 'L'
            
        nachalenX = PLOT_NA_MACHINA_X*mashtab+10 - stranaPoX*mashtab
        kraenX = nachalenX + stranaPoX*mashtab
        
        canvestodrawon.create_rectangle(nachalenX, 30, kraenX, stranaPoY*mashtab+30, fill=color, tags="rightRec")
            
        if pripluzvaneInd == 1 and purPol == 'L':   
            b1Coord = izbrani_elementi['RB1'] 
            b1_x1 = b1Coord[0]
            b1_y1 = b1Coord[1]
            b1_x2 = b1Coord[2]
            b1_y2 = b1Coord[3]
            
            b2Coord =  izbrani_elementi['RB2'] 
            b2_x1 = b2Coord[0]
            b2_y1 = b2Coord[1]
            b2_x2 = b2Coord[2]
            b2_y2 = b2Coord[3]
            
            if rotation == 0:
                canvestodrawon.create_line(nachalenX-2, 28, nachalenX+borderLength, 28, fill="purple", width=2, tags="border3")
                canvestodrawon.create_line(nachalenX-2, 28, nachalenX-2, borderLength+30,  fill="purple", width=2, tags="border4")  
            elif rotation == 1:
                b1_x1 = nachalenX + b1_x1 - 30
                b1_x2 = b1_x1 + borderLength
                b2_x1 = nachalenX + b2_x1 - 30
                b2_x2 = b2_x1
                
                canvestodrawon.create_line(PLOT_NA_MACHINA_X*mashtab+10-borderLength, 28, PLOT_NA_MACHINA_X*mashtab+10, 28, fill="purple", width=2, tags="border3")
                canvestodrawon.create_line(kraenX+2, 32, kraenX+2, borderLength+30, fill="purple", width = 2, tags="border4")
            elif rotation == 2:
                canvestodrawon.create_line(kraenX+2, stranaPoY*mashtab+30-borderLength, kraenX+2, stranaPoY*mashtab+32, fill="purple", width=2, tags="border4")
                canvestodrawon.create_line(kraenX-borderLength,stranaPoY*mashtab+32,kraenX+2, stranaPoY*mashtab+32, fill="purple",  width=2,tags="border3")
            elif rotation == 3:
                canvestodrawon.create_line(nachalenX-2, stranaPoY*mashtab, nachalenX-2, stranaPoY*mashtab+30, fill="purple", width=2, tags="border4")
                canvestodrawon.create_line(nachalenX-2, stranaPoY*mashtab+30, nachalenX+borderLength, stranaPoY*mashtab+30,fill="purple", width=2, tags="border3")
            
            #canvestodrawon.create_line(b1_x1, b1_y1, b1_x2, b1_y2, fill="purple", width=2, tags="border3")
            #canvestodrawon.create_line(b2_x1, b2_y1, b2_x2, b2_y2, fill="purple", width=2, tags="border4")
        
        else:
            if rotation == 0:
                canvestodrawon.create_line(PLOT_NA_MACHINA_X*mashtab+10-borderLength, 28, PLOT_NA_MACHINA_X*mashtab+10, 28, fill="purple", width=2, tags="border3")
                canvestodrawon.create_line(kraenX+2, 32, kraenX+2, borderLength+30, fill="purple", width = 2, tags="border4")
            elif rotation == 1:
                canvestodrawon.create_line(kraenX+2, stranaPoY*mashtab+30-borderLength, kraenX+2, stranaPoY*mashtab+32, fill="purple", width=2, tags="border4")
                canvestodrawon.create_line(kraenX-borderLength,stranaPoY*mashtab+32,kraenX+2, stranaPoY*mashtab+32, fill="purple",  width=2,tags="border3")
            elif rotation == 2:
                canvestodrawon.create_line(nachalenX-2, stranaPoY*mashtab, nachalenX-2, stranaPoY*mashtab+30, fill="purple", width=2, tags="border4")
                canvestodrawon.create_line(nachalenX-2, stranaPoY*mashtab+30, nachalenX+borderLength, stranaPoY*mashtab+30,fill="purple", width=2, tags="border3")
            elif rotation == 3:
                canvestodrawon.create_line(nachalenX-2, 28, nachalenX+borderLength, 28, fill="purple", width=2, tags="border3")
                canvestodrawon.create_line(nachalenX-2, 28, nachalenX-2, borderLength+30,  fill="purple", width=2, tags="border4")   

def narisuvai_dupka_na_plota(isHorizontDupka, xcoordinata, ycoordinata, dulbochina, radius, eIzvunPlota, side, canvestodrawon, stranaX, stranaY):
    onX = 0
    onY = 0
    if stranaX == xcoordinata:
        onX = 1
    if stranaY == ycoordinata:
        onY = 1
    
    if side == 'L':
        zeroCoordinate = 30
    elif side == 'R':
        zeroCoordinate = (PLOT_NA_MACHINA_X-stranaX)*mashtab+10

    if isHorizontDupka == 1:
        if ycoordinata == 0:
            nachalo_x = zeroCoordinate + (xcoordinata - radius)*mashtab
            krai_x = zeroCoordinate + (xcoordinata + radius)*mashtab
            nachalo_y = 30
            krai_y = 30 + dulbochina*mashtab

        if xcoordinata == 0:
            nachalo_x = zeroCoordinate
            krai_x = zeroCoordinate + dulbochina*mashtab
            nachalo_y = 30 + (ycoordinata- radius)*mashtab
            krai_y = 30 + (ycoordinata + radius)*mashtab
           
        if onY == 1:
            nachalo_x = zeroCoordinate + (xcoordinata - radius)*mashtab
            krai_x = zeroCoordinate + (xcoordinata + radius)*mashtab
            nachalo_y = 30 + ycoordinata*mashtab
            krai_y = 30 + (ycoordinata - dulbochina)*mashtab
          
        if onX == 1:    
            nachalo_x = zeroCoordinate + (xcoordinata - dulbochina)*mashtab
            krai_x = zeroCoordinate + (xcoordinata)*mashtab
            nachalo_y = 30 + (ycoordinata - radius)*mashtab
            krai_y = 30 + (ycoordinata + radius)*mashtab
    else:
        nachalo_x = zeroCoordinate + (xcoordinata - radius)*mashtab
        krai_x = zeroCoordinate + (xcoordinata + radius)*mashtab 
        nachalo_y = 30 + (ycoordinata - radius)*mashtab
        krai_y = 30 + (ycoordinata + radius)*mashtab

    if side == 'L':
        otag = 'lov'+ str(len(leftOvals)+1)
    else:
        otag = 'rov'+ str(len(rightOvals)+1)
        
    if eIzvunPlota == 1:
        if isHorizontDupka == 1:
            ov =  canvestodrawon.create_rectangle(nachalo_x, nachalo_y, krai_x, krai_y, fill="maroon", tag=otag)
        else:    
            ov = canvestodrawon.create_oval(nachalo_x, nachalo_y, krai_x, krai_y, fill="maroon", tag=otag)
    else:
        if isHorizontDupka == 1:
            ov =  canvestodrawon.create_rectangle(nachalo_x, nachalo_y, krai_x, krai_y, fill="blue", tag=otag)
        else: 
            ov = canvestodrawon.create_oval(nachalo_x, nachalo_y, krai_x, krai_y, fill="blue", tag=otag)
    
    if side == 'L':    
        leftOvals.append(ov)
    elif side == 'R':
        rightOvals.append(ov)
    

def mahni_element_ot_lqva_baza():
    canvas.delete("leftRec")
    canvas.delete("border1")
    canvas.delete("border2")
    
    cnt = 1
    while cnt <= len(leftOvals):
        otag = 'lov'+str(cnt)
        canvas.delete(otag)
        cnt = cnt + 1
    
    #Oshte neshta za reset
    del dupki_za_gcode_left[:]
    del izbrani_elementi['L']
    del izbrani_elementi['LO']
    if izbrani_elementi.has_key('LB1'):
        del izbrani_elementi['LB1']
        del izbrani_elementi['LB2']

def mahni_element_ot_dqsna_baza():
    canvas.delete("rightRec")
    canvas.delete("border3")
    canvas.delete("border4")
    
    cnt = 1
    while cnt <= len(rightOvals):
        otag = 'rov'+str(cnt)
        canvas.delete(otag)
        cnt = cnt + 1
    
    #Oshte neshta za reset
    del dupki_za_gcode_right[:]
    del izbrani_elementi['R']
    del izbrani_elementi['RO']
    if izbrani_elementi.has_key('RB1'):
        del izbrani_elementi['RB1']
        del izbrani_elementi['RB2']

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
    
    pripluzniInd = 0
    if side == 'L':   
        izbrani_elementi['LO'] = newOrientation
        if izbrani_elementi.has_key('LB1'):
            pripluzniInd = 1
        narisuvai_element_na_plota(izbranElement, newOrientation, 'L', ccanvas, 1, pripluzniInd)
    elif side == 'R':
        izbrani_elementi['RO'] = newOrientation
        if izbrani_elementi.has_key('RB1'):
            pripluzniInd = 1
        narisuvai_element_na_plota(izbranElement, newOrientation, 'R', ccanvas, 1, pripluzniInd)
        
def ima_li_dupki_izvun_plota(dupki_za_proverka, rotation, side, element_x, element_y):
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
        
        if rotation == 0:
            d_x1 = d_x
            d_y1 = d_y
        elif rotation == 1:
            d_y1 = d_y
            d_x1 = element_x - d_x
        elif rotation == 2:
            d_x1 = element_x - d_x
            d_y1 = element_y - d_y
        elif rotation == 3:
            d_x1 = d_x
            d_y1 = element_y - d_y
        
        # Dobavi radiusa za da imame nai krainata tochka
        d_y1 = d_y1 + d_r
        
        if side == 'L':
            d_x1 = d_x1 + d_r
        
        if side == 'R':
            d_x1 = d_x1 - d_r
            d_x1 = d_x1 + (PLOT_NA_MACHINA_X-element_x)
               
        if poneEdnaDupkaIzlizaPoX == 0:
            if d_x1 > PLOT_NA_MACHINA_X or d_x1 < 0:
                poneEdnaDupkaIzlizaPoX = 1
            
        if poneEdnaDupkaIzlizaPoY == 0:
            if d_y1 > PLOT_NA_MACHINA_Y:
                poneEdnaDupkaIzlizaPoY = 1    
        
    dupkiIzvunPlota = {}
    dupkiIzvunPlota["IzvunX"] = poneEdnaDupkaIzlizaPoX
    dupkiIzvunPlota["IzvunY"] = poneEdnaDupkaIzlizaPoY
    
    return dupkiIzvunPlota
                
def narisuvai_element_na_plota(izbranElement, rotation, side, canvestodrawon, resetCanvasInd, pripluzvaneInd):
    if side == 'L':
        del dupki_za_gcode_left[:]
    elif side == 'R':
        del dupki_za_gcode_right[:]
        
    #Reset
    if resetCanvasInd == 1:
        if side == 'L':
            canvestodrawon.delete("leftRec")
            canvestodrawon.delete("border1")
            canvestodrawon.delete("border2")
            cnt = 1
            while cnt <= len(leftOvals):
                otag = 'lov'+str(cnt)
                canvestodrawon.delete(otag)
                cnt = cnt + 1  
        elif side == 'R':
            canvestodrawon.delete("rightRec")
            canvestodrawon.delete("border3")
            canvestodrawon.delete("border4")
            
            cnt = 1
            while cnt <= len(rightOvals):
                otag = 'rov'+str(cnt)
                canvestodrawon.delete(otag)
                cnt = cnt + 1            
            
    #Vzemi razmerite na stranata
    razmeri_na_elementa = izbranElement.razmeri
    if rotation == 0 or rotation == 2:
        element_x = float(razmeri_na_elementa['x'])
        element_y = float(razmeri_na_elementa['y'])
    else:
        element_x = float(razmeri_na_elementa['y'])
        element_y = float(razmeri_na_elementa['x'])
        
    #Nachertai elementa vurhu plota na machinata
    narisuvai_strana_na_plota(element_x, element_y, side, canvestodrawon, rotation, pripluzvaneInd)

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
        dupkiIzvunPlot = ima_li_dupki_izvun_plota(dupki_na_elementa, rotation, side, element_x, element_y)
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
            if (side == 'L'and d_x > element_x/2+35) or (side == 'R' and d_x < element_x/2+35):
                izlizaPoX = 1
        
        if dupkaIzvunY == 1:
            if d_y > element_y/2 or d_y > PLOT_NA_MACHINA_Y:
                izlizaPoY = 1
        
        horizontOtvor = 0
        if dupka.has_key('t'):
            if dupka['t'] == 'H':
                horizontOtvor = 1
        
        if izlizaPoX == 0 and izlizaPoY == 0:     
            # Zapazi tochnite koordinati na dupkite za g-code
            if horizontOtvor == 1:
                if dupka.has_key('f'):
                    dupka_za_gcode = {"x" : d_x, "y": d_y, "h" : dulbochina, "r" : d_r, "t" : horizontOtvor, "f" : dupka['f'], "defh" : dupka['defh']}
                else:
                    dupka_za_gcode = {"x" : d_x, "y": d_y, "h" : dulbochina, "r" : d_r, "t" : horizontOtvor}
            else:   
                dupka_za_gcode = {"x" : d_x, "y": d_y, "h" : dulbochina, "r" : d_r, "t" : horizontOtvor}
                
            if side == 'L':
                dupki_za_gcode_left.append(dupka_za_gcode)
            elif side == 'R':
                dupki_za_gcode_right.append(dupka_za_gcode)
            
            narisuvai_dupka_na_plota(horizontOtvor, d_x, d_y, dulbochina, d_r, 0, side, canvestodrawon, element_x, element_y)
        else:
            narisuvai_dupka_na_plota(horizontOtvor, d_x, d_y, dulbochina, d_r, 1, side, canvestodrawon, element_x, element_y)        

def pripluzni_element():
    rotation = 0
    if izbrani_elementi.has_key('L'):
        detail =  izbrani_elementi['L']
        rotation = izbrani_elementi['LO']
        border1Coord = canvas.coords('border1')
        border2Coord = canvas.coords('border2')
        
        if detail.purvonachalnoPolojenie == '':
            detail.purvonachalnoPolojenie = 'L'
        
        izbrani_elementi['R'] = detail
        izbrani_elementi['RO'] = rotation
        izbrani_elementi['RB1'] = border1Coord
        izbrani_elementi['RB2'] = border2Coord
        
        mahni_element_ot_lqva_baza()
        izberi_element_za_dupchene('R', rotation, 1)
    elif izbrani_elementi.has_key('R'):
        detail = izbrani_elementi['R']
        rotation = izbrani_elementi['RO']
        border3Coord = canvas.coords('border3')
        border4Coord = canvas.coords('border4')
        
        if detail.purvonachalnoPolojenie == '':
            detail.purvonachalnoPolojenie = 'R'
        
        izbrani_elementi['L'] = detail
        izbrani_elementi['LO'] = rotation
        izbrani_elementi['LB1'] = border3Coord
        izbrani_elementi['LB2'] = border4Coord
        
        mahni_element_ot_dqsna_baza()
        izberi_element_za_dupchene('L', rotation, 1)

def nastroika_na_instrumenti():
    def on_closing_inst():
        top.destroy()
        
    def save_instruments():
        vertikalniInstrumenti = definirai_instrumenti('V')
        horizontalniInstrumenti = definirai_instrumenti('H')
        skorosti = definirai_skorosti()
        write_instruments(vertikalniInstrumenti, horizontalniInstrumenti, skorosti)
        
    top = Toplevel()
    top.title(nastroikaInstrumentButtonText)
    top.protocol("WM_DELETE_WINDOW", on_closing_inst)
    
    frame1 = LabelFrame(top, text=vertikalnaGlavaText)
    frame1.grid(row=0, padx = 20, pady=10)
    frame2 = LabelFrame(top, text=horizontalnaGlavaText)
    frame2.grid(row=0, column=1, padx = 20, pady=10)
    
    instr1LabelBox = LabelFrame(frame1, text=instrument1LabelText)
    instr1LabelBox.grid(row=1, columnspan=2, pady=10)
    dia1Label = Label(instr1LabelBox, text=diameturLabelText)
    dia1Label.grid(row=0, sticky=W)
    dia1Entry = Entry(instr1LabelBox, textvariable=vginstrument1EntryDiaValue)
    dia1Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost1Label = Label(instr1LabelBox, text=skorostText)
    skorost1Label.grid(row=1, sticky=W)
    skorost1Entry = Entry(instr1LabelBox, textvariable=vginstrument1EntrySkorostValue)
    skorost1Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    instr2LabelBox = LabelFrame(frame1, text=instrument2LabelText)
    instr2LabelBox.grid(row=2, columnspan=2, pady=10)
    dia2Label = Label(instr2LabelBox, text=diameturLabelText)
    dia2Label.grid(row=0, sticky=W)
    dia2Entry = Entry(instr2LabelBox, textvariable=vginstrument2EntryDiaValue)
    dia2Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost2Label = Label(instr2LabelBox, text=skorostText)
    skorost2Label.grid(row=1, sticky=W)
    skorost2Entry = Entry(instr2LabelBox, textvariable=vginstrument2EntrySkorostValue)
    skorost2Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    instr3LabelBox = LabelFrame(frame1, text=instrument3LabelText)
    instr3LabelBox.grid(row=3, columnspan=2, pady=10)
    dia3Label = Label(instr3LabelBox, text=diameturLabelText)
    dia3Label.grid(row=0, sticky=W)
    dia3Entry = Entry(instr3LabelBox, textvariable=vginstrument3EntryDiaValue)
    dia3Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost3Label = Label(instr3LabelBox, text=skorostText)
    skorost3Label.grid(row=1, sticky=W)
    skorost3Entry = Entry(instr3LabelBox, textvariable=vginstrument3EntrySkorostValue)
    skorost3Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    instr4LabelBox = LabelFrame(frame1, text=instrument4LabelText)
    instr4LabelBox.grid(row=4, columnspan=2, pady=10)
    dia4Label = Label(instr4LabelBox, text=diameturLabelText)
    dia4Label.grid(row=0, sticky=W)
    dia4Entry = Entry(instr4LabelBox, textvariable=vginstrument4EntryDiaValue)
    dia4Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost4Label = Label(instr4LabelBox, text=skorostText)
    skorost4Label.grid(row=1, sticky=W)
    skorost4Entry = Entry(instr4LabelBox, textvariable=vginstrument4EntrySkorostValue)
    skorost4Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    instr5LabelBox = LabelFrame(frame1, text=instrument5LabelText)
    instr5LabelBox.grid(row=5, columnspan=2, pady=10)
    dia5Label = Label(instr5LabelBox, text=diameturLabelText)
    dia5Label.grid(row=0, sticky=W)
    dia5Entry = Entry(instr5LabelBox, textvariable=vginstrument5EntryDiaValue)
    dia5Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost5Label = Label(instr5LabelBox, text=skorostText)
    skorost5Label.grid(row=1, sticky=W)
    skorost5Entry = Entry(instr5LabelBox, textvariable=vginstrument5EntrySkorostValue)
    skorost5Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    # Horizontalni instrumenti
    instr1LabelBox = LabelFrame(frame2, text=instrument1LabelText)
    instr1LabelBox.grid(row=1, columnspan=2, pady=10)
    dia1Label = Label(instr1LabelBox, text=diameturLabelText)
    dia1Label.grid(row=0, sticky=W)
    dia1Entry = Entry(instr1LabelBox, textvariable=hginstrument1EntryDiaValue)
    dia1Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost1Label = Label(instr1LabelBox, text=skorostText)
    skorost1Label.grid(row=1, sticky=W)
    skorost1Entry = Entry(instr1LabelBox, textvariable=hginstrument1EntrySkorostValue)
    skorost1Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    instr2LabelBox = LabelFrame(frame2, text=instrument2LabelText)
    instr2LabelBox.grid(row=2, columnspan=2, pady=10)
    dia2Label = Label(instr2LabelBox, text=diameturLabelText)
    dia2Label.grid(row=0, sticky=W)
    dia2Entry = Entry(instr2LabelBox, textvariable=hginstrument2EntryDiaValue)
    dia2Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost2Label = Label(instr2LabelBox, text=skorostText)
    skorost2Label.grid(row=1, sticky=W)
    skorost2Entry = Entry(instr2LabelBox, textvariable=hginstrument2EntrySkorostValue)
    skorost2Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    instr3LabelBox = LabelFrame(frame2, text=instrument3LabelText)
    instr3LabelBox.grid(row=3, columnspan=2, pady=10)
    dia3Label = Label(instr3LabelBox, text=diameturLabelText)
    dia3Label.grid(row=0, sticky=W)
    dia3Entry = Entry(instr3LabelBox, textvariable=hginstrument3EntryDiaValue)
    dia3Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost3Label = Label(instr3LabelBox, text=skorostText)
    skorost3Label.grid(row=1, sticky=W)
    skorost3Entry = Entry(instr3LabelBox, textvariable=hginstrument3EntrySkorostValue)
    skorost3Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    instr4LabelBox = LabelFrame(frame2, text=instrument4LabelText)
    instr4LabelBox.grid(row=4, columnspan=2, pady=10)
    dia4Label = Label(instr4LabelBox, text=diameturLabelText)
    dia4Label.grid(row=0, sticky=W)
    dia4Entry = Entry(instr4LabelBox, textvariable=hginstrument4EntryDiaValue)
    dia4Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost4Label = Label(instr4LabelBox, text=skorostText)
    skorost4Label.grid(row=1, sticky=W)
    skorost4Entry = Entry(instr4LabelBox, textvariable=hginstrument4EntrySkorostValue)
    skorost4Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    instr5LabelBox = LabelFrame(frame2, text=instrument5LabelText)
    instr5LabelBox.grid(row=5, columnspan=2, pady=10)
    dia5Label = Label(instr5LabelBox, text=diameturLabelText)
    dia5Label.grid(row=0, sticky=W)
    dia5Entry = Entry(instr5LabelBox, textvariable=hginstrument5EntryDiaValue)
    dia5Entry.grid(row=0, column=1, padx = 5, pady = 2, sticky=E)
    skorost5Label = Label(instr5LabelBox, text=skorostText)
    skorost5Label.grid(row=1, sticky=W)
    skorost5Entry = Entry(instr5LabelBox, textvariable=hginstrument5EntrySkorostValue)
    skorost5Entry.grid(row=1, column=1, padx = 5, pady = 2, sticky=E)
    
    zapaziNastorikiButton = Button(top, text=zapaziInstrFileButtonText, command=save_instruments)
    zapaziNastorikiButton.grid(row=1, padx = 15, pady = 10, sticky='E')
    zatvoriButton = Button(top, text=zatvoriButtonText, command=on_closing_inst)
    zatvoriButton.grid(row=1, column=1,padx = 15, pady = 10,  sticky='E')

def iztrii_temp_gcode_file():
    #iztrii_stupki()
    if os.path.isfile("sample123.txt"):
        os.remove("sample123.txt")
    global gcodeInProgress
    gcodeInProgress = 0
    global n10
    n10 = 30
    
    if stepsList is not None:
        stepsList.delete(0, END)
    
    
def zapishi_gcode_file():
    global n10
    global gcodeInProgress
    
    saveFileName = asksaveasfilename(filetypes=(("GCode files", "*.txt"), ("All files", "*.*")))
    if not saveFileName.endswith('.txt'):
        saveFileName = saveFileName + u'.txt'
    
    tempFile = open("sample123.txt", "r")
    gCodeFile = open(saveFileName, "w")
    
    gCodeFile.write("("+saveFileName+")\n")
    for line in tempFile:
        gCodeFile.write(line)
         
    tempFile.close()
     
    ciklichnoPrezarejdane = ciklichnoPrezarejdaneGCodeValue.get()
     
    #Sloji krai na G-Code
    if ciklichnoPrezarejdane == 1:
        krai ='N'+str(n10)+'M47\n'
        n10 = n10 + 10
         
        gCodeFile.write(krai)
    else:    
        krai1 = 'N'+str(n10)+'G00Z'+str(bezopasno_z)+'\n'
        n10 = n10 + 10
        krai2 = 'N'+str(n10)+'G00X'+str("{0:.3f}".format(PLOT_NA_MACHINA_X/2))+'Y0.000\n'
        n10 = n10 + 10
        krai3 = 'N'+str(n10)+'M09\n'
        n10 = n10 + 10
        krai4 ='N'+str(n10)+'M30\n'
        n10 = n10 + 10
         
        gCodeFile.write(krai1)
        gCodeFile.write(krai2)
        gCodeFile.write(krai3)
        gCodeFile.write(krai4)        
        
    gCodeFile.close()
    
    #iztrii_stupki()
    stepsList.delete(0, END)
    
    #Delete Temp file:
    iztrii_temp_gcode_file()

def definirai_instrumenti(HorV):
    if HorV == 'V':
        vgInst1Diam = float(vginstrument1EntryDiaValue.get())
        vgInst2Diam = float(vginstrument2EntryDiaValue.get())
        vgInst3Diam = float(vginstrument3EntryDiaValue.get())
        vgInst4Diam = float(vginstrument4EntryDiaValue.get())
        vgInst5Diam = float(vginstrument5EntryDiaValue.get())
        
        return {'T1':vgInst1Diam, 'T2':vgInst2Diam, 'T3':vgInst3Diam, 'T4':vgInst4Diam, 'T5':vgInst5Diam}
    elif HorV == 'H':
        vgInst6Diam = float(hginstrument1EntryDiaValue.get())
        vgInst7Diam = float(hginstrument2EntryDiaValue.get())
        vgInst8Diam = float(hginstrument3EntryDiaValue.get())
        vgInst9Diam = float(hginstrument4EntryDiaValue.get())
        vgInst10Diam = float(hginstrument5EntryDiaValue.get())
        
        return {'T6':vgInst6Diam, 'T7':vgInst7Diam, 'T8':vgInst8Diam, 'T9':vgInst9Diam, 'T10':vgInst10Diam}

def definirai_skorosti():
    t1Skorost = float(vginstrument1EntrySkorostValue.get())
    t2Skorost = float(vginstrument2EntrySkorostValue.get())
    t3Skorost = float(vginstrument3EntrySkorostValue.get())
    t4Skorost = float(vginstrument4EntrySkorostValue.get())
    t5Skorost = float(vginstrument5EntrySkorostValue.get())
    t6Skorost = float(hginstrument1EntrySkorostValue.get())
    t7Skorost = float(hginstrument2EntrySkorostValue.get())
    t8Skorost = float(hginstrument3EntrySkorostValue.get())
    t9Skorost = float(hginstrument4EntrySkorostValue.get())
    t10Skorost = float(hginstrument5EntrySkorostValue.get())
    
    return {'T1':t1Skorost,'T2':t2Skorost,'T3':t3Skorost,'T4':t4Skorost,'T5':t5Skorost,'T6':t6Skorost,'T7':t7Skorost,'T8':t8Skorost,'T9':t9Skorost,'T10':t10Skorost,'T11':t6Skorost}

def izberi_skorost(skorostMap, instrument):
    skorost = 0
    for k,v in skorostMap.iteritems():
        if k == instrument:
            skorost = v
            break
    return skorost
        
def izberi_instrument(instrMap, diametur, zaFiks):    
    instT = 'INVALID'
    
    # Ako probivame fiksove i diameturka na T6 i T7 sa ravni, izberi T11 (2 instrumenta zaedno)
    if zaFiks == 1:
        if instrMap['T6'] == instrMap['T7']:
            instT = 'T11'
    
    if instT == 'INVALID':
        for k,v in instrMap.iteritems():
            if v == diametur:
                instT = k
                break
    return instT

def napravi_comment_za_polojenieto(side):
    polojenie = ''
    orientation = izbrani_elementi[side]
    rameriMap = izbrani_elementi[side[0]].razmeri
    razmeri = str(rameriMap['x'])+' x '+str(rameriMap['y'])
    if orientation == 0:
        polojenie = 'Detail '+razmeri+' na 0 gradusa'
    elif orientation == 1:
        polojenie = 'Detail '+razmeri+' na 90 gradusa'
    elif orientation == 2:
        polojenie = 'Detail '+razmeri+' na 180 gradusa'
    elif orientation == 3:
        polojenie = 'Detail '+razmeri+' na 270 gradusa'
        
    return polojenie   

def ima_li_lipsvash_instrument(verGlavaInst, horGlavaInst):  
    if len(dupki_za_gcode_left) > 0:
        for dupka in dupki_za_gcode_left:
            diam = dupka['r']*2
            if dupka['t'] == 1:
                if not diam in horGlavaInst.values():
                    print 'lipsva horizontalna glava'
                    return diam
            else:
                if not diam in verGlavaInst.values():
                    print 'lipsva vertikalna glava'
                    return diam
        
        for dupka in dupki_za_gcode_right:
            diam = dupka['r']*2
            if dupka['t'] == 1:
                if not diam in horGlavaInst.values():
                    print 'lipsva horizontalna glava'
                    return diam
            else:
                if not diam in verGlavaInst.values():
                    print 'lipsva vertikalna glava'
                    return diam
            
        return 0    
            
def suzdai_gcode_file():  
    # Line iterator
    global n10
    global TT 
    global gcodeInProgress    
    bezopasno_z = "{0:.3f}".format(20.000) # Tova she bude izchesleno kato debelinata na materiala ot bxf + 20
    instrumentiZaVerGlava = definirai_instrumenti('V')
    instrumentiZaHorizGlava = definirai_instrumenti('H')
    
    lispvashDiametur = ima_li_lipsvash_instrument(instrumentiZaVerGlava, instrumentiZaHorizGlava)
    if lispvashDiametur > 0:
        iztrii_temp_gcode_file()
        msgLipsInst = u'Липсва инструмент с диаметър: '+str(lispvashDiametur)+ u' мм. Поставете липсващия инструмент и генерирайте кода отново.'
        tkMessageBox.showinfo(title=u'Внимание', message=msgLipsInst)
        return
    
    skorostZaInstrumenti = definirai_skorosti()
    t11instrument = 0
    if hginstrument1EntryDiaValue.get() == hginstrument2EntryDiaValue.get():
        t11instrument = 1

    # Stoinosti na g-code (horizontalni otvori, vertikalni, pause, ciklichno)
    napraviHorizontalniOtvori = genHorizontOtvoriGCodeValue.get()
    napraviVertiklaniOtvori = genVertikalOtvoriGCodeValue.get()
    postaviPausa = pauseMejduDetailiGCodeValue.get()
    
    # Koga samo da dobavi vs. koga e nov file i ima comments on top     
    if os.path.isfile("sample123.txt"):
        print "File sample123.text exists. Dabavi ..."
        fw = open("sample123.txt", "a")
    else:    
        fw = open("sample123.txt", "a")
        
    # SLOJI KOMENTARI ZA POLOJENIETO NA DETAILA

    if gcodeInProgress == 0:
        ''' COMENTARI '''
        # Stoinosti na instrumentite
        dateTimeLine = '('+time.strftime("%d/%m/%Y")+')\n' # or try today = datetime.date.today()
        fw.write(dateTimeLine)
 
    else:
        n10 = 30
        
    leftHorizontDupkiNeOpt = []
    leftVertikalDupkiNeOpt = []
    rightHorizontDupkiNeOpt = []
    rightVertikalDupkiNeOpt = [] 
    
    ''' COMENTARI '''
    # Tova e samo za komentar v g-code za da vidq koq sled koq dupka se dupchi
    if len(dupki_za_gcode_left) > 0:
#         fw.write('(Lqva Baza Otvori:)\n')
        fw.write('(Lqva Baza: '+napravi_comment_za_polojenieto('LO')+')\n')
    for dupka in dupki_za_gcode_left:
        if dupka['t'] == 1:
            if napraviHorizontalniOtvori == 1 and dupka['y']== 0:
                leftHorizontDupkiNeOpt.append(dupka)
#                 dupkaLine = "(Horizontalen otvor: " + 'X:'+ str(dupka['x']) + ', Y:' + str(dupka['y']) +', R:'+ str(dupka['r']) + ', H:'+str(dupka['h'])+')\n'
#                 fw.write(dupkaLine)
        else:
            if napraviVertiklaniOtvori == 1:
                leftVertikalDupkiNeOpt.append(dupka)
#                 dupkaLine = "(Vertikalen otvor: " + 'X:'+ str(dupka['x']) + ', Y:' + str(dupka['y']) +', R:'+ str(dupka['r']) + ', H:'+str(dupka['h'])+')\n'
#                 fw.write(dupkaLine)
    
    if len(dupki_za_gcode_right) > 0:
#         fw.write('(Dqsna Baza Otvori:)\n')     
        fw.write('(Dqsna Baza: '+napravi_comment_za_polojenieto('RO')+')\n')
    for dupka in dupki_za_gcode_right:
        if dupka['t'] == 1:
            if napraviHorizontalniOtvori == 1 and dupka['y']== 0:
                rightHorizontDupkiNeOpt.append(dupka)
#                 dupkaLine = "(Horizontalen otvor: " + 'X:'+ str(dupka['x']) + ', Y:' + str(dupka['y']) +', R:'+ str(dupka['r']) + ', H:'+str(dupka['h'])+')\n'
#                 fw.write(dupkaLine)   
        else:
            if napraviVertiklaniOtvori == 1:
                rightVertikalDupkiNeOpt.append(dupka)      
#                 dupkaLine = "(Vertikalen otvor: " + 'X:'+ str(dupka['x']) + ', Y:' + str(dupka['y']) +', R:'+ str(dupka['r']) + ', H:'+str(dupka['h'])+')\n'
#                 fw.write(dupkaLine)   
    
    #Optimizacia
    if len(leftVertikalDupkiNeOpt) > 0:
        leftVertikalDupki = optimizirai_otvori(leftVertikalDupkiNeOpt)
    else:
        leftVertikalDupki = []
    if len(leftHorizontDupkiNeOpt) > 0:
        leftHorizontDupki = optimizirai_otvori(leftHorizontDupkiNeOpt)
    else:
        leftHorizontDupki = []
    if len(rightHorizontDupkiNeOpt) > 0:
        rightHorizontDupki = optimizirai_otvori(rightHorizontDupkiNeOpt)
    else:
        rightHorizontDupki = []
    if len(rightVertikalDupkiNeOpt) > 0:
        rightVertikalDupki = optimizirai_otvori(rightVertikalDupkiNeOpt)
    else:
        rightVertikalDupki = []
    
    # Nameri instrument za purvata dupka
    razmerNachalnaDupka = 0
    typeHiliV =  'H'
    if napraviHorizontalniOtvori == 1 and len(leftHorizontDupki) > 0:
        dup = leftHorizontDupki[0]
        razmerNachalnaDupka = dup['r']*2      
    elif napraviVertiklaniOtvori == 1 and razmerNachalnaDupka == 0 and len(leftVertikalDupki) > 0:
        dup = leftVertikalDupki[0]
        razmerNachalnaDupka = dup['r']*2
        typeHiliV =  'V'   
    elif napraviHorizontalniOtvori == 1 and razmerNachalnaDupka == 0 and len(rightHorizontDupki) > 0:
        dup = rightHorizontDupki[0]
        razmerNachalnaDupka = dup['r']*2  
    elif napraviVertiklaniOtvori == 1 and razmerNachalnaDupka == 0 and len(rightVertikalDupki) > 0:
        dup = rightVertikalDupki[0]
        razmerNachalnaDupka = dup['r']*2
        typeHiliV =  'V' 
    
    #if gcodeInProgress == 0 or TT=='':    
    # Logika za liniite na g-coda
    if typeHiliV == 'V':
        TT = izberi_instrument(instrumentiZaVerGlava, razmerNachalnaDupka, 0)
    else:
        zaFiks = 0
        if dup.has_key('f'):
            if dup['f'] == 1:
                zaFiks = 1
        TT = izberi_instrument(instrumentiZaHorizGlava, razmerNachalnaDupka, zaFiks)
        
    HT = 'H'+TT[1:]
    vzemiInstrument = 'N'+str(n10)+TT+'M06\n'
    n10 = n10 + 10
    predpazvaneNaZ = 'N'+str(n10)+'G00G43Z'+str(bezopasno_z)+HT+'\n'
    n10 = n10 + 10
    zavurtiNaMaxOboroti = 'N'+str(n10)+'S6000M03\n'
    n10 = n10 + 10
    
    if gcodeInProgress == 0:
        prediNachalnoPozicionirane = 'N'+str(n10)+'G94\n'
        n10 = n10 + 10
    
        # Nachalo na g-code
        fw.write('N10G00G21G17G90G40G49G80\n')    
        fw.write('N20G71G91.1\n')  
        
    fw.write(vzemiInstrument)
    fw.write(predpazvaneNaZ)
    fw.write(zavurtiNaMaxOboroti)
    
    if gcodeInProgress == 0:
        fw.write(prediNachalnoPozicionirane)
    
    def gcode_lines_za_dupka(dupka, typeHiliV, baza, locDebelinaMaterial):  
        global TT       
        global n10 
        
        dulbochinaNaDupkata = dupka['h']
        
        SD = "{0:.1f}".format(izberi_skorost(skorostZaInstrumenti, TT))
        
        # Vij kakuv instrument triabva da polzvash
        if typeHiliV == 'V':
            instrZaDupka = izberi_instrument(instrumentiZaVerGlava, dupka['r']*2, 0)
        else:
            if dupka.has_key('f'):
                instrZaDupka = izberi_instrument(instrumentiZaHorizGlava, dupka['r']*2, 1)
                if instrZaDupka == 'T11':
                    dulbochinaNaDupkata = dupka['defh']
            else:
                instrZaDupka = izberi_instrument(instrumentiZaHorizGlava, dupka['r']*2, 0)
            locDebelinaMaterial = 0
        
        purvonachaloZ = "{0:.3f}".format(locDebelinaMaterial + 10)   
        if typeHiliV == 'H':
            purvonachaloZ = "{0:.3f}".format(locDebelinaMaterial + 10)
            
        if instrZaDupka != TT:  
            # Smeni instrumenta
            TT = instrZaDupka
            HT = 'H'+TT[1:]
            SD = "{0:.1f}".format(izberi_skorost(skorostZaInstrumenti, TT))
            vzemiInstrument = 'N'+str(n10)+TT+'M06\n'
            n10 = n10 + 10
            fw.write(vzemiInstrument)
            d4Line = 'N'+str(n10)+'G43'+HT+'\n'
            fw.write(d4Line)
            n10 = n10 + 10
            zavurtiNaMaxOboroti = 'N'+str(n10)+'S6000M03\n'
            n10 = n10 + 10
            fw.write(zavurtiNaMaxOboroti)
        
        xKoordinata = dupka['x']
        if baza == 'R':
            razmeri_na_elementa = izbrani_elementi['R'].razmeri
            if izbrani_elementi['RO'] == 0 or izbrani_elementi['RO'] == 2:
                element_x = float(razmeri_na_elementa['x'])
            else:
                element_x = float(razmeri_na_elementa['y'])
 
            xKoordinata = (PLOT_NA_MACHINA_X-element_x) + dupka['x']
            
        d1Line = 'N'+str(n10)+'G00X'+str("{0:.3f}".format(xKoordinata))+'Y'+str("{0:.3f}".format(dupka['y']))+"Z"+str(purvonachaloZ)+'\n'
        n10 = n10 + 10
        fw.write(d1Line)
        krainoZ = "{0:.3f}".format(float(locDebelinaMaterial) - dulbochinaNaDupkata)
        d2Line = 'N'+str(n10)+'G1X'+str("{0:.3f}".format(xKoordinata))+'Y'+str("{0:.3f}".format(dupka['y']))+"Z"+str(krainoZ)+'F'+SD+'\n'
        n10 = n10 + 10
        fw.write(d2Line)   
        d3Line = 'N'+str(n10)+'G00X'+str("{0:.3f}".format(xKoordinata))+'Y'+str("{0:.3f}".format(dupka['y']))+"Z"+str(purvonachaloZ)+'\n'
        n10 = n10 + 10
        fw.write(d3Line)
    
    def postavi_pauza(bezopasno_z):
        global n10
        fw.write('N'+str(n10)+'G00X'+str("{0:.3f}".format(PLOT_NA_MACHINA_X/2))+'Y0.000Z'+str(bezopasno_z)+'\n')
        n10 = n10 + 10
        fw.write('N'+str(n10)+'M5 M1\n')
        n10 = n10 + 10
        
    
    debelinaMaterialLqvo = 0
    debelinaMaterialDqsno = 0
    
    if len(leftVertikalDupki) > 0:
        razmerDet = izbrani_elementi['L'].razmeri
        debelinaMaterialLqvo = float(razmerDet['h'])
    if len(rightVertikalDupki) > 0:
        razmerDet = izbrani_elementi['R'].razmeri
        debelinaMaterialDqsno = float(razmerDet['h'])
        
    if napraviHorizontalniOtvori == 1:
        #Dupki - LQVA BAZA, HORIZONTAL
        for dupka in leftHorizontDupki:
            if t11instrument == 0:
                gcode_lines_za_dupka(dupka, 'H', 'L', debelinaMaterialLqvo)
            else:
                if dupka.has_key('f'):
                    if dupka['f'] == 1:
                        gcode_lines_za_dupka(dupka, 'H', 'L', debelinaMaterialLqvo)
                else:
                    gcode_lines_za_dupka(dupka, 'H', 'L', debelinaMaterialLqvo)
                       
    if napraviVertiklaniOtvori == 1:
        #Dupki - LQVA BAZA, VERTIKAL
        for dupka in leftVertikalDupki:
            gcode_lines_za_dupka(dupka, 'V', 'L', debelinaMaterialLqvo)
        
    if napraviHorizontalniOtvori == 1:
        #Dupki - DQSNA BAZA, HORIZONTAL
        for dupka in rightHorizontDupki:
            if t11instrument == 0:
                gcode_lines_za_dupka(dupka, 'H', 'R', debelinaMaterialDqsno)
            else:
                if dupka.has_key('f'):
                    if dupka['f'] == 1:
                        gcode_lines_za_dupka(dupka, 'H', 'R', debelinaMaterialDqsno)
                else:
                    gcode_lines_za_dupka(dupka, 'H', 'R', debelinaMaterialDqsno)
        
    if napraviVertiklaniOtvori == 1:   
        #Dupki - DQSNA BAZA, VERTIKAL    
        for dupka in rightVertikalDupki:
            gcode_lines_za_dupka(dupka, 'V', 'R', debelinaMaterialDqsno)
    
    if postaviPausa == 1:
        postavi_pauza(bezopasno_z)
    
    # Kraq na G-code
    fw.close()
    
    pokaji_stupki(napraviHorizontalniOtvori, napraviVertiklaniOtvori, len(leftHorizontDupki), len(leftVertikalDupki), len(rightHorizontDupki), len(rightVertikalDupki))
    
    gcodeInProgress = 1

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
    
    def zapazi_nov_detail(*args):
        dupki_blank = []
        # Narochno sa oburnati X,Y zashtoto orientacia xy ot BXF oznachva oburnati X,Y ...Taka che ne promenqi tuk!
        razmer_x = float(duljinaValue.get())
        razmer_y = float(shirinaValue.get())
        debelina = float(debelinaValue.get())
        razmeri_map = {"x" : razmer_x, "y": razmer_y, "h":debelina}
        detail = ElementZaDupchene(imeValue.get(), razmeri_map, dupki_blank)
        ekey = 'customdetail'+imeValue.get()
        elementi_za_dupchene[ekey] = detail
        prevod = u'ВД: '+imeValue.get()+' ..... '+str(razmer_x)+' x '+str(razmer_y)+' x '+str(debelina)
        
        global theSortedList
        theSortedList.append((100, prevod, ekey))
        
        listbox.insert(END, prevod)

        top.destroy()
    
    okbutton = Button(top, text=okButtonText, command=zapazi_nov_detail)
    okbutton.bind('<Return>', zapazi_nov_detail)
    okbutton.grid(row=2, padx = 10, pady = 10, sticky = W)
    cancelButton = Button(top, text=cancelButtonText, command=top.destroy)
    cancelButton.grid(row=2, column=1, pady = 10, sticky=W)
       
def reset_canvas():
    canvas.delete(ALL)
    canvas.create_rectangle(20, 20, PLOT_NA_MACHINA_X*mashtab+20, PLOT_NA_MACHINA_Y*mashtab+20, fill="bisque")
    for side in izbrani_elementi.keys():
        if side == 'L':
            narisuvai_element_na_plota(izbrani_elementi[side], izbrani_elementi[side+'O'], side, canvas, 0, 0)
       
        if side == 'R':
            narisuvai_element_na_plota(izbrani_elementi[side], izbrani_elementi[side+'O'], side, canvas, 0, 0)
            
def redaktirai_lqv_detail():
    global izbranElementZaRedakciaInd
    izbranElementZaRedakciaInd = 'L'
    pokaji_redaktirai_window('L')

def redaktirai_desen_detail(): 
    global izbranElementZaRedakciaInd
    izbranElementZaRedakciaInd = 'R'
    pokaji_redaktirai_window('R')
           
def pokaji_redaktirai_window(side):
    
    listOfFiksove = []
    listOfVertikali = []
    listOfHorizontali = []

    def on_closing():
        ramka.destroy()
        reset_canvas()
        
    def rotate_element_za_redakcia():
        rotate_element(side, rcanvas)

    def verikalenOtvorUI():
        for wid in frame1.grid_slaves():
            wid.grid_forget()
        natisti_button_prop('vertikal')
        
        #Populni default stoinosti
        defStoinosti = read_param_za_otvori('vertikal')
        if len(defStoinosti) > 0:
            vertikalenOtvorXValue.set(defStoinosti[0])
            vertikalenOtvorYValue.set(defStoinosti[1])
            vertikalenOtvorDiamValue.set(defStoinosti[2])
            vertikalenOtvorDulbochinaValue.set(defStoinosti[3])
            raztoqnieMejduVertikalniValue.set(defStoinosti[4])
            broiVertikalniOtvoriValue.set(defStoinosti[5])
        
        voFrame = LabelFrame(frame1, text=paramVertikalenOtvorText)
        voFrame.grid(row=0, padx=5, pady=15, sticky=W+E)
        
        xLabel = Label(voFrame, text=otstoqniePoXLabelText)
        xLabel.grid(row=1, sticky=W)
        xEntry = Entry(voFrame, textvariable=vertikalenOtvorXValue)
        xEntry.grid(row=1, column=1, padx = 2, pady = 2, sticky=E)
        yLabel = Label(voFrame, text=otstoqniePoYLabelText)
        yLabel.grid(row=2, sticky=W)
        yEntry = Entry(voFrame, textvariable=vertikalenOtvorYValue)
        yEntry.grid(row=2, column=1, padx = 2, pady = 2, sticky=E)
        diamXLabel = Label(voFrame, text=diameturVertikalenOtvorXLabelText)
        diamXLabel.grid(row=3, sticky=W)
        diamXEntry = Entry(voFrame, textvariable=vertikalenOtvorDiamValue)
        diamXEntry.grid(row=3, column=1, padx = 2, pady = 2, sticky=E)       
        dulbXLabel = Label(voFrame, text=dulbochinaVertikalenOtvorLabelText)
        dulbXLabel.grid(row=4, sticky=W)
        dulbXEntry = Entry(voFrame, textvariable=vertikalenOtvorDulbochinaValue)
        dulbXEntry.grid(row=4, column=1, padx = 2, pady = 2, sticky=E)
        
        raztoqnieLabel = Label(voFrame, text=raztoqnieMejduOtvori)
        raztoqnieLabel.grid(row=5, sticky=W)
        raztoqnieEntry = Entry(voFrame, textvariable=raztoqnieMejduVertikalniValue)
        raztoqnieEntry.grid(row=5, column=1, padx = 2, pady = 2, sticky=E)
        broiLabel = Label(voFrame, text=broiOtvori)
        broiLabel.grid(row=6, sticky=W)
        broiEntry = Entry(voFrame, textvariable=broiVertikalniOtvoriValue)
        broiEntry.grid(row=6, column=1, padx = 2, pady = 2, sticky=E)
        
        copyPoXCheckBox = Checkbutton(frame1, text=kopiraiOtvorPoXSimetrichnoLabelText, variable=simetrichnoOtvorPoXValue)
        copyPoXCheckBox.grid(row=1, sticky=W)
        copyPoYCheckBox = Checkbutton(frame1, text=kopiraiOtvorPoYSimetrichnoLabelText, variable=simetrichnoOtvorPoYValue)
        copyPoYCheckBox.grid(row=2, sticky=W)
        
        postaviFixButton = Button(frame1, text=postaviOtvorText, width=20, command=postavi_vertikalni_otvori)
        postaviFixButton.grid(row=5, padx = 5, pady = 5, sticky=E)
        otkajiFixButton = Button(frame1, text=stupkaNazadLabelText, width=20, command=iztrii_posleden_vertikalen)
        otkajiFixButton.grid(row=6, padx = 5, pady = 5, sticky=E)
        izchistiFixButton = Button(frame1, text=izchistiOtvoriText, width=20, command=iztrii_vsichki_vertikalni)
        izchistiFixButton.grid(row=7, padx = 5, pady = 5, sticky=E)
        zapaziiFixButton = Button(frame1, text=zapaziOtvoriText, width=20, command=on_closing)
        zapaziiFixButton.grid(row=8, padx = 5, pady = 5, sticky=E)
    
    def horizontalenOtvorUI():
        for wid in frame1.grid_slaves():
            wid.grid_forget()
        natisti_button_prop('horizontal')
        
        defStoinosti = read_param_za_otvori('horizontal')
        if len(defStoinosti) > 0:
            horizontalenOtvorXValue.set(defStoinosti[0])
            horizontalenOtvorDiamValue.set(defStoinosti[2])
            dulbochinaHorizontalenOtvorValue.set(defStoinosti[3])
            raztoqnieMejduHorizontalenValue.set(defStoinosti[4])
            broiHorizontalniOtvoriValue.set(defStoinosti[5])   
            
        hoFrame = LabelFrame(frame1, text=paramHorizontalenOtvorText)
        hoFrame.grid(row=0, padx=5, pady=15, sticky=W+E)
        
        xLabel = Label(hoFrame, text=otstoqniePoXLabelText)
        xLabel.grid(row=1, sticky=W)
        xEntry = Entry(hoFrame, textvariable=horizontalenOtvorXValue)
        xEntry.grid(row=1, column=1, padx = 2, pady = 2, sticky=E)

        diamXLabel = Label(hoFrame, text=diameturHorizontOtvorLabelText)
        diamXLabel.grid(row=2, sticky=W)
        diamXEntry = Entry(hoFrame, textvariable=horizontalenOtvorDiamValue)
        diamXEntry.grid(row=2, column=1, padx = 2, pady = 2, sticky=E)       
        dulbXLabel = Label(hoFrame, text=dulbochinaHorizontOtvorYLabelText)
        dulbXLabel.grid(row=3, sticky=W)
        dulbXEntry = Entry(hoFrame, textvariable=dulbochinaHorizontalenOtvorValue)
        dulbXEntry.grid(row=3, column=1, padx = 2, pady = 2, sticky=E)
        raztoqnieLabel = Label(hoFrame, text=raztoqnieMejduOtvori)
        raztoqnieLabel.grid(row=4, sticky=W)
        raztoqnieEntry = Entry(hoFrame, textvariable=raztoqnieMejduHorizontalenValue)
        raztoqnieEntry.grid(row=4, column=1, padx = 2, pady = 2, sticky=E)
        broiLabel = Label(hoFrame, text=broiOtvori)
        broiLabel.grid(row=5, sticky=W)
        broiEntry = Entry(hoFrame, textvariable=broiHorizontalniOtvoriValue)
        broiEntry.grid(row=5, column=1, padx = 2, pady = 2, sticky=E)
        copyPoXCheckBox = Checkbutton(frame1, text=kopiraiOtvorPoXSimetrichnoLabelText, variable=simetrichnoHorizontalenOtvorPoXValue)
        copyPoXCheckBox.grid(row=1, sticky=W)
        copyPoYCheckBox = Checkbutton(frame1, text=kopiraiOtvorPoYSimetrichnoLabelText, variable=simetrichnoHorizontalenOtvorPoYValue)
        copyPoYCheckBox.grid(row=2, sticky=W)
        
        postaviFixButton = Button(frame1, text=postaviOtvorText, width=20, command=postavi_horizontalni_otvori)
        postaviFixButton.grid(row=5, padx = 5, pady = 5, sticky=E)
        otkajiFixButton = Button(frame1, text=stupkaNazadLabelText, width=20, command=iztrii_posleden_horizontalen)
        otkajiFixButton.grid(row=6, padx = 5, pady = 5, sticky=E)
        izchistiFixButton = Button(frame1, text=izchistiOtvoriText, width=20, command=iztrii_vsichki_horizontalni)
        izchistiFixButton.grid(row=7, padx = 5, pady = 5, sticky=E)
        zapaziiFixButton = Button(frame1, text=zapaziOtvoriText, width=20, command=on_closing)
        zapaziiFixButton.grid(row=8, padx = 5, pady = 5, sticky=E)
                
    def fiksUI():
        for wid in frame1.grid_slaves():
            wid.grid_forget()
        natisti_button_prop('fiks')
        
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
        otkajiFixButton = Button(frame1, text=stupkaNazadLabelText, width=20, command=iztrii_posleden_fiks)
        otkajiFixButton.grid(row=6, padx = 5, pady = 5, sticky=E)
        izchistiFixButton = Button(frame1, text=izchistiFixoveLabelText, width=20, command=iztrii_vsichki_fiksove)
        izchistiFixButton.grid(row=7, padx = 5, pady = 5, sticky=E)
        zapaziiFixButton = Button(frame1, text=zapaziFixoveLabelText, width=20, command=on_closing)
        zapaziiFixButton.grid(row=8, padx = 5, pady = 5, sticky=E)
    
    def iztrii_vsichki_fiksove():
        iztrii_vsichki_otvori('fiks')
        
    def iztrii_posleden_fiks():
        iztrii_posleden_otvor('fiks')
    
    def iztrii_vsichki_horizontalni():
        iztrii_vsichki_otvori('horizontal')
        
    def iztrii_posleden_horizontalen():
        iztrii_posleden_otvor('horizontal')
        
    def iztrii_vsichki_vertikalni():
        iztrii_vsichki_otvori('vertikal')
        
    def iztrii_posleden_vertikalen():
        iztrii_posleden_otvor('vertikal')
        
    def iztrii_vsichki_otvori(vid):
        izbranElement = izbrani_elementi[izbranElementZaRedakciaInd]
        dupki_na_elementa = izbranElement.dupki
        dupkiBezOtvori = []
        
        if(vid == 'fiks'):
            del listOfFiksove[:]
          
            for fiks in dupki_na_elementa:
                if not (fiks.has_key('fv') or fiks.has_key('f')):
                    dupkiBezOtvori.append(fiks)
                    
        elif(vid == 'vertikal'):
            del listOfVertikali[:]
            
            for verOtvor in dupki_na_elementa:
                if verOtvor.has_key('fv') or verOtvor.has_key('f'):
                    dupkiBezOtvori.append(verOtvor)
                if not verOtvor.has_key('t'):
                    dupkiBezOtvori.append(verOtvor)
                elif verOtvor['t'] == 'H':
                    dupkiBezOtvori.append(verOtvor)   
                    
        elif(vid == 'horizontal'):
            del listOfHorizontali[:]
            
            for horOtvor in dupki_na_elementa:
                if horOtvor.has_key('fv') or horOtvor.has_key('f'):
                    dupkiBezOtvori.append(horOtvor)
                if not horOtvor.has_key('t'):
                    dupkiBezOtvori.append(horOtvor)
                elif horOtvor['t'] == 'V':
                    dupkiBezOtvori.append(horOtvor)   
                    
        del dupki_na_elementa[:]
        izbranElement.dupki = dupkiBezOtvori
        
        rcanvas.delete(ALL)
        narisuvai_element_na_plota(izbranElement, izbrani_elementi[izbranElementZaRedakciaInd+'O'], izbranElementZaRedakciaInd, rcanvas, 0, 0)
    
    def iztrii_posleden_otvor(vid):
        if vid == 'fiks':
            if len(listOfFiksove) > 0:
                d1 = listOfFiksove.pop()
                d2 = listOfFiksove.pop()
                d3 = listOfFiksove.pop()
                
                izbranElement = izbrani_elementi[izbranElementZaRedakciaInd]
                dupki_na_elementa = izbranElement.dupki
                
                dupki_na_elementa.remove(d1)
                dupki_na_elementa.remove(d2)
                dupki_na_elementa.remove(d3)
                
                rcanvas.delete(ALL)
                narisuvai_element_na_plota(izbranElement, izbrani_elementi[izbranElementZaRedakciaInd+'O'], izbranElementZaRedakciaInd, rcanvas, 0, 0)
                
        elif vid == 'vertikal':
            if len(listOfVertikali) > 0:
                vd = listOfVertikali.pop()
                
                izbranElement = izbrani_elementi[izbranElementZaRedakciaInd]
                dupki_na_elementa = izbranElement.dupki
                
                dupki_na_elementa.remove(vd)
                rcanvas.delete(ALL)
                narisuvai_element_na_plota(izbranElement, izbrani_elementi[izbranElementZaRedakciaInd+'O'], izbranElementZaRedakciaInd, rcanvas, 0, 0)
        elif vid == 'horizontal':
            if len(listOfHorizontali) > 0:
                hd = listOfHorizontali.pop()
                
                izbranElement = izbrani_elementi[izbranElementZaRedakciaInd]
                dupki_na_elementa = izbranElement.dupki
                
                dupki_na_elementa.remove(hd)
                rcanvas.delete(ALL)
                narisuvai_element_na_plota(izbranElement, izbrani_elementi[izbranElementZaRedakciaInd+'O'], izbranElementZaRedakciaInd, rcanvas, 0, 0)
            
    def postavi_fiks():
        postavi_dupki('fiks')
    
    def postavi_vertikalni_otvori():
        postavi_dupki('vertikal')
        
    def postavi_horizontalni_otvori():
        postavi_dupki('horizontal')
        
    def postavi_dupki(vid):
        dulbochina25 = 25.0
        raztoqnie = 32
        
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
        
        centFix = 0
        copyCentFix = 0
        zyl_h_hor = 0
        zyl_r_hor = 0
        zyl_h = 0
        zyl_r = 0
        if vid == 'fiks':
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
        elif vid == 'vertikal':
            zyl_pos_x = float(vertikalenOtvorXValue.get())
            zyl_pos_y = float(vertikalenOtvorYValue.get())
            zyl_h = float(vertikalenOtvorDulbochinaValue.get())
            zyl_r = float(vertikalenOtvorDiamValue.get())/2.0
            raztoqnie_mejdu_otvori = float(raztoqnieMejduVertikalniValue.get())
            broi_otvori = broiVertikalniOtvoriValue.get()
    
            simPoX = simetrichnoOtvorPoXValue.get()
            simPoY = simetrichnoOtvorPoYValue.get()
            
            # Zapishi gi vuv file kato default values
            write_param_za_otvori(vid, zyl_pos_x, zyl_pos_y, zyl_r*2, zyl_h, raztoqnie_mejdu_otvori, broi_otvori)
        elif vid == 'horizontal':
            zyl_pos_x = float(horizontalenOtvorXValue.get())
            zyl_pos_y = 0.0
            zyl_h_hor = float(dulbochinaHorizontalenOtvorValue.get())
            zyl_r_hor = float(horizontalenOtvorDiamValue.get())/2.0
            raztoqnie_mejdu_otvori = float(raztoqnieMejduHorizontalenValue.get())
            broi_otvori = broiHorizontalniOtvoriValue.get()
    
            simPoX = simetrichnoHorizontalenOtvorPoXValue.get()
            simPoY = simetrichnoHorizontalenOtvorPoYValue.get()
            
            # Zapishi gi vuv file kato default values
            write_param_za_otvori(vid, zyl_pos_x, zyl_pos_y, zyl_r_hor*2, zyl_h_hor, raztoqnie_mejdu_otvori, broi_otvori)
        
        # Purvate dupka (obiknoveno 100 x 34) 
        # Ne se dobavq SAMO AKO edinstventa otmetka izbrana e Centralen Fix 
        # Keys: "f" is for fiks, param 1 (vzemi koordinatite na tazi dupka za T11 - 2 instrumenta zaedno)
        #       "defh" - default dulbochina koqto usera e vkaral (28 e standartna). Need pak za T11 logic.
        #       "fv" - fiks vertikalen otvor  - triabva mi kogato iztrivame vsichki fiksove, parametura nqma znachenie
        if (simPoX == 0 and simPoY == 0 and centFix == 0 and copyCentFix == 0) or simPoX == 1 or simPoY == 1: 
            if rotation == 0:
                dupka1  = {"x" : zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r, "t" : "V", "fv" : 1}
                dupka1a  = {"x" : zyl_pos_x, "y": 0, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka1b  = {"x" : zyl_pos_x-raztoqnie, "y": 0, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 1:
                dupka1 = {"x" : zyl_pos_y, "y": element_x - zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka1a  = {"x" : 0, "y": element_x - zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka1b  = {"x" : 0, "y": element_x - zyl_pos_x+raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 2:
                dupka1 = {"x" : element_x-zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka1a  = {"x" : element_x-zyl_pos_x, "y": element_y, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka1b  = {"x" : element_x-zyl_pos_x+raztoqnie, "y": element_y, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 3:
                dupka1 = {"x" : element_y-zyl_pos_y, "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka1a  = {"x" : element_y, "y": zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka1b  = {"x" : element_y, "y": zyl_pos_x-raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
    
            if vid == 'fiks':
                if not is_dupka_duplicate(dupka1, dupki_na_elementa):
                    dupki_na_elementa.append(dupka1)
                    listOfFiksove.append(dupka1)
                if not is_dupka_duplicate(dupka1b, dupki_na_elementa):    
                    dupki_na_elementa.append(dupka1b)
                    listOfFiksove.append(dupka1b)
                if not is_dupka_duplicate(dupka1a, dupki_na_elementa):    
                    dupki_na_elementa.append(dupka1a)
                    listOfFiksove.append(dupka1a)
            elif vid == 'vertikal':
                if not is_dupka_duplicate(dupka1, dupki_na_elementa):
                    del dupka1['fv']
                    dupka1['t'] = "V"
                    dupki_na_elementa.append(dupka1)
                    listOfVertikali.append(dupka1)
                    if broi_otvori > 1 and raztoqnie_mejdu_otvori > 0:
                        cnt = 1
                        while cnt < broi_otvori:
                            if rotation == 0:
                                novX = dupka1['x'] + raztoqnie_mejdu_otvori*cnt
                                novY = dupka1['y']
                            elif rotation == 1:
                                novX = dupka1['x'] 
                                novY = dupka1['y'] - raztoqnie_mejdu_otvori*cnt
                            elif rotation == 2:
                                novX = dupka1['x'] - raztoqnie_mejdu_otvori*cnt
                                novY = dupka1['y']
                            elif rotation == 3:
                                novX = dupka1['x'] 
                                novY = dupka1['y'] + raztoqnie_mejdu_otvori*cnt
                             
                            if ((rotation == 0 or rotation == 2) and (element_x >= novX and novX >= 0 and element_y >= novY and novY >= 0)) or ((rotation == 1 or rotation == 3) and (element_y >= novX and novX >= 0 and element_x >= novY and novY >= 0)):
                                dupkaV = {"x" :novX, "y": novY, "h" : zyl_h, "r" : zyl_r, "t" : "V"}
                                if not is_dupka_duplicate(dupkaV, dupki_na_elementa):
                                    dupki_na_elementa.append(dupkaV)
                                    listOfVertikali.append(dupkaV)
                            cnt = cnt+1
            elif vid == 'horizontal':
                if not is_dupka_duplicate(dupka1a, dupki_na_elementa):
                    del dupka1a['f']
                    del dupka1a['defh']
                    dupki_na_elementa.append(dupka1a)
                    listOfHorizontali.append(dupka1a)
                    if broi_otvori > 1 and raztoqnie_mejdu_otvori > 0:
                        cnt = 1
                        while cnt < broi_otvori:
                            if rotation == 0:
                                novX = dupka1a['x'] + raztoqnie_mejdu_otvori*cnt
                                novY = dupka1a['y']
                            elif rotation == 1:
                                novX = dupka1a['x'] 
                                novY = dupka1a['y'] - raztoqnie_mejdu_otvori*cnt
                            elif rotation == 2:
                                novX = dupka1a['x'] - raztoqnie_mejdu_otvori*cnt
                                novY = dupka1a['y']
                            elif rotation == 3:
                                novX = dupka1a['x'] 
                                novY = dupka1a['y'] + raztoqnie_mejdu_otvori*cnt
                                
                            if ((rotation == 0 or rotation == 2) and (element_x >= novX and novX >= 0 and element_y >= novY and novY >= 0)) or ((rotation == 1 or rotation == 3) and (element_y >= novX and novX >= 0 and element_x >= novY and novY >= 0)):
                                dupkaH = {"x" :novX, "y": novY, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H"}
                                if not is_dupka_duplicate(dupkaH, dupki_na_elementa):
                                    dupki_na_elementa.append(dupkaH)
                                    listOfHorizontali.append(dupkaH)
                            cnt = cnt+1   
                            
        if simPoX == 1:
            # Vtorata dupka po X (ogledalna na dupka)
            if rotation == 0:
                dupka2 = {"x" : element_x-zyl_pos_x, "y":zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka2a  = {"x" : element_x-zyl_pos_x, "y": 0, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka2b  = {"x" : element_x-zyl_pos_x+raztoqnie, "y": 0, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 1:
                dupka2 = {"x" : zyl_pos_y, "y": zyl_pos_x,  "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka2a  = {"x" : 0, "y": zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka2b  = {"x" : 0, "y": zyl_pos_x-raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 2:
                dupka2 = {"x" : zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka2a  = {"x" : zyl_pos_x, "y": element_y, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka2b  = {"x" : zyl_pos_x-raztoqnie, "y": element_y, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 3:
                dupka2 = {"x" : element_y-zyl_pos_y, "y": element_x-zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka2a  = {"x" : element_y, "y": element_x-zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka2b  = {"x" : element_y, "y": element_x-zyl_pos_x+raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
             
            if vid == 'fiks':
                if not is_dupka_duplicate(dupka2, dupki_na_elementa):
                    dupki_na_elementa.append(dupka2)
                    listOfFiksove.append(dupka2)
                if not is_dupka_duplicate(dupka2b, dupki_na_elementa):    
                    dupki_na_elementa.append(dupka2b)
                    listOfFiksove.append(dupka2b)
                if not is_dupka_duplicate(dupka2a, dupki_na_elementa):    
                    dupki_na_elementa.append(dupka2a)
                    listOfFiksove.append(dupka2a)
            elif vid == 'vertikal':
                if not is_dupka_duplicate(dupka2, dupki_na_elementa):
                    del dupka2['fv']
                    dupka2['t'] = "V"
                    dupki_na_elementa.append(dupka2)
                    listOfVertikali.append(dupka2)
                    if broi_otvori > 1 and raztoqnie_mejdu_otvori > 0:
                        cnt = 1
                        while cnt < broi_otvori:
                            if rotation == 0:
                                novX = dupka2['x'] - raztoqnie_mejdu_otvori*cnt
                                novY = dupka2['y']
                            elif rotation == 1:
                                novX = dupka2['x'] 
                                novY = dupka2['y'] + raztoqnie_mejdu_otvori*cnt
                            elif rotation == 2:
                                novX = dupka2['x'] + raztoqnie_mejdu_otvori*cnt
                                novY = dupka2['y']
                            elif rotation == 3:
                                novX = dupka2['x'] 
                                novY = dupka2['y'] - raztoqnie_mejdu_otvori*cnt
                                
                            if ((rotation == 0 or rotation == 2) and (element_x >= novX and novX >= 0 and element_y >= novY and novY >= 0)) or ((rotation == 1 or rotation == 3) and (element_y >= novX and novX >= 0 and element_x >= novY and novY >= 0)):
                                dupkaV = {"x" :novX, "y": novY, "h" : zyl_h, "r" : zyl_r, "t" : "V"}
                                if not is_dupka_duplicate(dupkaV, dupki_na_elementa):
                                    dupki_na_elementa.append(dupkaV)
                                    listOfVertikali.append(dupkaV)
                            cnt = cnt+1
            elif vid == 'horizontal':
                if not is_dupka_duplicate(dupka2a, dupki_na_elementa):
                    del dupka2a['f']
                    del dupka2a['defh']
                    dupki_na_elementa.append(dupka2a)
                    listOfHorizontali.append(dupka2a)
                    if broi_otvori > 1 and raztoqnie_mejdu_otvori > 0:
                        cnt = 1
                        while cnt < broi_otvori:
                            if rotation == 0:
                                novX = dupka2a['x'] - raztoqnie_mejdu_otvori*cnt
                                novY = dupka2a['y']
                            elif rotation == 1:
                                novX = dupka2a['x'] 
                                novY = dupka2a['y'] + raztoqnie_mejdu_otvori*cnt
                            elif rotation == 2:
                                novX = dupka2a['x'] + raztoqnie_mejdu_otvori*cnt
                                novY = dupka2a['y']
                            elif rotation == 3:
                                novX = dupka2a['x'] 
                                novY = dupka2a['y'] - raztoqnie_mejdu_otvori*cnt
                                
                            if ((rotation == 0 or rotation == 2) and (element_x >= novX and novX >= 0 and element_y >= novY and novY >= 0)) or ((rotation == 1 or rotation == 3) and (element_y >= novX and novX >= 0 and element_x >= novY and novY >= 0)):
                                dupkaH = {"x" :novX, "y": novY, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H"}
                                if not is_dupka_duplicate(dupkaH, dupki_na_elementa):
                                    dupki_na_elementa.append(dupkaH)
                                    listOfHorizontali.append(dupkaH)
                            cnt = cnt+1  

        
        if simPoY == 1:
            # Vtorata dupka po Y (ogledalna na dupka)
            if rotation == 0:
                dupka3 = {"x" : zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka3a  = {"x" : zyl_pos_x, "y": element_y, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka3b  = {"x" : zyl_pos_x-raztoqnie, "y": element_y, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 1:
                dupka3 = {"x" : element_y-zyl_pos_y, "y": element_x-zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka3a  = {"x" : element_y, "y": element_x-zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka3b  = {"x" : element_y, "y": element_x-zyl_pos_x+raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 2:
                dupka3 = {"x" : element_x-zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka3a  = {"x" : element_x-zyl_pos_x, "y": 0, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka3b  = {"x" : element_x-zyl_pos_x+raztoqnie, "y": 0, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 3:
                dupka3 = {"x" : zyl_pos_y, "y": zyl_pos_x,  "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka3a  = {"x" : 0, "y": zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka3b  = {"x" : 0, "y": zyl_pos_x-raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                
            if vid == 'fiks':
                if not is_dupka_duplicate(dupka3, dupki_na_elementa):
                    dupki_na_elementa.append(dupka3)
                    listOfFiksove.append(dupka3)
                if not is_dupka_duplicate(dupka3b, dupki_na_elementa):    
                    dupki_na_elementa.append(dupka3b)
                    listOfFiksove.append(dupka3b)
                if not is_dupka_duplicate(dupka3a, dupki_na_elementa):    
                    dupki_na_elementa.append(dupka3a)
                    listOfFiksove.append(dupka3a)
            elif vid == 'vertikal':
                if not is_dupka_duplicate(dupka3, dupki_na_elementa):
                    del dupka3['fv']
                    dupka3['t'] = "V"
                    dupki_na_elementa.append(dupka3)
                    listOfVertikali.append(dupka3)
                    if broi_otvori > 1 and raztoqnie_mejdu_otvori > 0:
                        cnt = 1
                        while cnt < broi_otvori:
                            if rotation == 0:
                                novX = dupka3['x'] + raztoqnie_mejdu_otvori*cnt
                                novY = dupka3['y']
                            elif rotation == 1:
                                novX = dupka3['x'] 
                                novY = dupka3['y'] - raztoqnie_mejdu_otvori*cnt
                            elif rotation == 2:
                                novX = dupka3['x'] - raztoqnie_mejdu_otvori*cnt
                                novY = dupka3['y']
                            elif rotation == 3:
                                novX = dupka3['x'] 
                                novY = dupka3['y'] + raztoqnie_mejdu_otvori*cnt
                                
                            if ((rotation == 0 or rotation == 2) and (element_x >= novX and novX >= 0 and element_y >= novY and novY >= 0)) or ((rotation == 1 or rotation == 3) and (element_y >= novX and novX >= 0 and element_x >= novY and novY >= 0)):
                                dupkaV = {"x" :novX, "y":  novY, "h" : zyl_h, "r" : zyl_r, "t" : "V"}
                                if not is_dupka_duplicate(dupkaV, dupki_na_elementa):
                                    dupki_na_elementa.append(dupkaV)
                                    listOfVertikali.append(dupkaV)
                            cnt = cnt+1
            elif vid == 'horizontal':
                if not is_dupka_duplicate(dupka3a, dupki_na_elementa):
                    del dupka3a['f']
                    del dupka3a['defh']
                    dupki_na_elementa.append(dupka3a)
                    listOfHorizontali.append(dupka3a)
                    if broi_otvori > 1 and raztoqnie_mejdu_otvori > 0:
                        cnt = 1
                        while cnt < broi_otvori:
                            if rotation == 0:
                                novX = dupka3a['x'] + raztoqnie_mejdu_otvori*cnt
                                novY = dupka3a['y']
                            elif rotation == 1:
                                novX = dupka3a['x'] 
                                novY = dupka3a['y'] - raztoqnie_mejdu_otvori*cnt
                            elif rotation == 2:
                                novX = dupka3a['x'] - raztoqnie_mejdu_otvori*cnt
                                novY = dupka3a['y']
                            elif rotation == 3:
                                novX = dupka3a['x'] 
                                novY = dupka3a['y'] + raztoqnie_mejdu_otvori*cnt
                                
                            if ((rotation == 0 or rotation == 2) and (element_x >= novX and novX >= 0 and element_y >= novY and novY >= 0)) or ((rotation == 1 or rotation == 3) and (element_y >= novX and novX >= 0 and element_x >= novY and novY >= 0)):
                                dupkaH = {"x" :novX, "y": novY, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H"}
                                if not is_dupka_duplicate(dupkaH, dupki_na_elementa):
                                    dupki_na_elementa.append(dupkaH)
                                    listOfHorizontali.append(dupkaH)
                            cnt = cnt+1  

            
        if simPoX == 1 and simPoY == 1:
            if rotation == 0:
                dupka4 =  {"x" : element_x-zyl_pos_x, "y": element_y- zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka4a  = {"x" : element_x-zyl_pos_x, "y": element_y, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka4b  = {"x" : element_x-zyl_pos_x+raztoqnie, "y": element_y, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 1:
                dupka4 = {"x" : element_y-zyl_pos_y, "y": zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka4a  = {"x" : element_y, "y": zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka4b  = {"x" : element_y, "y": zyl_pos_x-raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 2:
                dupka4 = {"x" : zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka4a  = {"x" : zyl_pos_x, "y": 0, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka4b  = {"x" : zyl_pos_x-raztoqnie, "y": 0, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 3:
                dupka4 = {"x" : zyl_pos_y, "y": element_x-zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka4a  = {"x" : 0, "y": element_x-zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka4b  = {"x" : 0, "y": element_x-zyl_pos_x+raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                
            if vid == 'fiks':
                if not is_dupka_duplicate(dupka4, dupki_na_elementa):
                    dupki_na_elementa.append(dupka4)
                    listOfFiksove.append(dupka4)
                if not is_dupka_duplicate(dupka4b, dupki_na_elementa):    
                    dupki_na_elementa.append(dupka4b)
                    listOfFiksove.append(dupka4b)
                if not is_dupka_duplicate(dupka4a, dupki_na_elementa):    
                    dupki_na_elementa.append(dupka4a)
                    listOfFiksove.append(dupka4a)
            elif vid == 'vertikal':
                if not is_dupka_duplicate(dupka4, dupki_na_elementa):
                    del dupka4['fv']
                    dupka4['t'] = "V"
                    dupki_na_elementa.append(dupka4)
                    listOfVertikali.append(dupka4)
                    if broi_otvori > 1 and raztoqnie_mejdu_otvori > 0:
                        cnt = 1
                        while cnt < broi_otvori:
                            if rotation == 0:
                                novX = dupka4['x'] - raztoqnie_mejdu_otvori*cnt
                                novY = dupka4['y']
                            elif rotation == 1:
                                novX = dupka4['x'] 
                                novY = dupka4['y'] + raztoqnie_mejdu_otvori*cnt
                            elif rotation == 2:
                                novX = dupka4['x'] + raztoqnie_mejdu_otvori*cnt
                                novY = dupka4['y']
                            elif rotation == 3:
                                novX = dupka4['x'] 
                                novY = dupka4['y'] - raztoqnie_mejdu_otvori*cnt
                                
                            if ((rotation == 0 or rotation == 2) and (element_x >= novX and novX >= 0 and element_y >= novY and novY >= 0)) or ((rotation == 1 or rotation == 3) and (element_y >= novX and novX >= 0 and element_x >= novY and novY >= 0)):
                                dupkaV = {"x" :novX, "y": novY, "h" : zyl_h, "r" : zyl_r, "t" : "V"}
                                if not is_dupka_duplicate(dupkaV, dupki_na_elementa):
                                    dupki_na_elementa.append(dupkaV)
                                    listOfVertikali.append(dupkaV)
                            cnt = cnt+1
            elif vid == 'horizontal':
                if not is_dupka_duplicate(dupka4a, dupki_na_elementa):
                    del dupka4a['f']
                    del dupka4a['defh']
                    dupki_na_elementa.append(dupka4a)
                    listOfHorizontali.append(dupka4a)
                    if broi_otvori > 1 and raztoqnie_mejdu_otvori > 0:
                        cnt = 1
                        while cnt < broi_otvori:
                            if rotation == 0:
                                novX = dupka4a['x'] - raztoqnie_mejdu_otvori*cnt
                                novY = dupka4a['y']
                            elif rotation == 1:
                                novX = dupka4a['x'] 
                                novY = dupka4a['y'] + raztoqnie_mejdu_otvori*cnt
                            elif rotation == 2:
                                novX = dupka4a['x'] + raztoqnie_mejdu_otvori*cnt
                                novY = dupka4a['y']
                            elif rotation == 3:
                                novX = dupka4a['x'] 
                                novY = dupka4a['y'] - raztoqnie_mejdu_otvori*cnt
                                
                            if ((rotation == 0 or rotation == 2) and (element_x >= novX and novX >= 0 and element_y >= novY and novY >= 0)) or ((rotation == 1 or rotation == 3) and (element_y >= novX and novX >= 0 and element_x >= novY and novY >= 0)):
                                dupkaH = {"x" :novX, "y": novY, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H"}
                                if not is_dupka_duplicate(dupkaH, dupki_na_elementa):
                                    dupki_na_elementa.append(dupkaH)
                                    listOfHorizontali.append(dupkaH)
                            cnt = cnt+1  

            
        if centFix == 1:
            center_zyl_pos_x = element_x/2
             
            if rotation == 0:
                dupka5 = {"x" : center_zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka5a  = {"x" : center_zyl_pos_x, "y": 0, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka5b  = {"x" : center_zyl_pos_x+raztoqnie, "y": 0, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 1:
                dupka5 = {"x" : zyl_pos_y, "y": center_zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka5a  = {"x" : 0, "y": center_zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka5b  = {"x" : 0, "y": center_zyl_pos_x-raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 2:
                dupka5 = {"x" : center_zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka5a  = {"x" : center_zyl_pos_x, "y": element_y, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka5b  = {"x" : center_zyl_pos_x-raztoqnie, "y": element_y, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
            elif rotation == 3:
                dupka5 = {"x" : element_y-zyl_pos_y, "y": center_zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka5a  = {"x" : element_y, "y": center_zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                dupka5b  = {"x" : element_y, "y": center_zyl_pos_x+raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                            
            if not is_dupka_duplicate(dupka5, dupki_na_elementa):
                dupki_na_elementa.append(dupka5)
                listOfFiksove.append(dupka5)
            if not is_dupka_duplicate(dupka5b, dupki_na_elementa):    
                dupki_na_elementa.append(dupka5b)
                listOfFiksove.append(dupka5b)
            if not is_dupka_duplicate(dupka5a, dupki_na_elementa):    
                dupki_na_elementa.append(dupka5a)
                listOfFiksove.append(dupka5a)
            
        if copyCentFix == 1:
            center_zyl_pos_x = element_x/2
            
            if rotation == 0:
                dupka6 = {"x" : center_zyl_pos_x, "y": element_y-zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka6a  = {"x" : center_zyl_pos_x, "y": element_y, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka6b  = {"x" : center_zyl_pos_x+raztoqnie, "y": element_y, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 1:
                dupka6 = {"x" : element_y-zyl_pos_y, "y": center_zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka6a  = {"x" : element_y, "y": center_zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka6b  = {"x" : element_y, "y": center_zyl_pos_x-raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 2:
                dupka6 = {"x" : center_zyl_pos_x, "y": zyl_pos_y, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}
                dupka6a  = {"x" : center_zyl_pos_x, "y": 0, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka6b  = {"x" : center_zyl_pos_x-raztoqnie, "y": 0, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
            elif rotation == 3:
                dupka6 = {"x" : zyl_pos_y, "y": center_zyl_pos_x, "h" : zyl_h, "r" : zyl_r,"t" : "V", "fv" : 1}  
                dupka6a  = {"x" : 0, "y": center_zyl_pos_x, "h" : zyl_h_hor, "r" : zyl_r_hor, "t" : "H", "f" : 0, "defh" : zyl_h_hor}
                dupka6b  = {"x" : 0, "y": center_zyl_pos_x+raztoqnie, "h" : dulbochina25, "r" : zyl_r_hor, "t" : "H", "f" : 1, "defh" : zyl_h_hor}
                
            if not is_dupka_duplicate(dupka6, dupki_na_elementa):
                dupki_na_elementa.append(dupka6)
                listOfFiksove.append(dupka6)
            if not is_dupka_duplicate(dupka6b, dupki_na_elementa):    
                dupki_na_elementa.append(dupka6b)
                listOfFiksove.append(dupka6b) 
            if not is_dupka_duplicate(dupka6a, dupki_na_elementa):    
                dupki_na_elementa.append(dupka6a)
                listOfFiksove.append(dupka6a)

        # Narisuvai
        rcanvas.delete(ALL)
        narisuvai_element_na_plota(izbranElement, izbrani_elementi[izbranElementZaRedakciaInd+'O'], izbranElementZaRedakciaInd, rcanvas, 0, 0)
        
    ramka = Toplevel()
    ramka.geometry("%dx%d+0+0" % (screenWidth, screenHeight-100))
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
    horizontalenOtvorButton = Button(buttonFrame, text=dobaviHorOtvorLabelText, command=horizontalenOtvorUI)
    horizontalenOtvorButton.grid(row=0, column=2, padx = 2, pady = 2, sticky=W)
    zavurtiButton = Button(buttonFrame, text=rotateButtonText, bg="lightblue", command=rotate_element_za_redakcia)
    zavurtiButton.grid(row=0, column=3, padx = 2, pady = 2, sticky=W)
    
    frame1 = Frame(ramka)
    frame1.grid(row=2, sticky=N+S)
    label1 = Label(frame1, text=izbereteOpciaLabelText, width= 50)
    label1.grid(row=0, pady = 20)
    
    rcanvasFrame = Frame(ramka, bd=2, relief=SUNKEN)
    rcanvasFrame.grid(row=2, column=1, columnspan = 2, padx=20, sticky=W+E+N+S)
    rxscrollbar = Scrollbar(rcanvasFrame, orient=HORIZONTAL)
    rxscrollbar.grid(row=1, column=0,sticky=E+W)
    ryscrollbar = Scrollbar(rcanvasFrame)
    ryscrollbar.grid(row=0, column=1, sticky=N+S)
    rcanvas = Canvas(rcanvasFrame, bg="grey", bd=0, width=canvasW+200, heigh=canvasH, scrollregion=(0, 0, 2000, 2000),
                    xscrollcommand=rxscrollbar.set,
                    yscrollcommand=ryscrollbar.set)
    rcanvas.grid(row=0, column=0, sticky=N+S+E+W)
    rxscrollbar.config(command=rcanvas.xview)
    ryscrollbar.config(command=rcanvas.yview)

    def natisti_button_prop(vid):
        if vid == 'fiks':
            fixButton.config(relief=SUNKEN)
            verikalenOtvorButton.config(relief=RAISED)
            horizontalenOtvorButton.config(relief=RAISED)
        elif vid == 'vertikal':
            fixButton.config(relief=RAISED)
            verikalenOtvorButton.config(relief=SUNKEN)
            horizontalenOtvorButton.config(relief=RAISED) 
        elif vid == 'horizontal':
            fixButton.config(relief=RAISED)
            verikalenOtvorButton.config(relief=RAISED)
            horizontalenOtvorButton.config(relief=SUNKEN) 
    
    # Narisuvai elementa na plota
    narisuvai_element_na_plota(izbrani_elementi[side], izbrani_elementi[side+'O'], side, rcanvas, 0, 0)
 
def pokaji_stupki(horInd, verInd, numHDLB, numVDLB, numHDDB, numVDDB):
    line1 = u'Стъпка'
    if numHDLB > 0 or numVDLB > 0:
        line1 = line1 + u' ...Лява Б.--'
        if horInd == 1:
            line1 = line1 + u' Х:'+str(numHDLB)
        if verInd == 1:
            line1 = line1 + u' В:'+str(numVDLB)
            
    if numHDDB > 0 or numVDDB > 0:
        line1 = line1 + u' ...Дясна Б.--'
        if horInd == 1:
            line1 = line1 + u' Х:'+str(numHDDB)
        if verInd == 1:
            line1 = line1 + u' В:'+str(numVDDB)
            
    if line1 != u'Стъпка':
        stepsList.insert(END, line1)

def iztrii_stupki():
    stepsList.delete(0, END)
                   
print ('*** BEGIN PROGRAM *************************')
iztrii_temp_gcode_file()
instrumentiOtConfig = read_instruments()
    
mainframe = Tk()
#mainframe.geometry('450x450+500+300') - Use that for window size
screenWidth,screenHeight=mainframe.winfo_screenwidth(),mainframe.winfo_screenheight()

# Resolution
useLowerResolution = 0
canvasW = 1100
canvasH = 700
listboxW = 50
listboxH = 40
if screenWidth <= 1400:
    canvasW = 720
    listboxW = 30
    listboxH = 30
    useLowerResolution = 1
if screenHeight <= 800:
    canvasH = 550
    useLowerResolution = 1
    
mainframe.geometry("%dx%d+0+0" % (screenWidth, screenHeight-100))



''' ***************************************************************************
*** Variables za stoinosti na instrumentite
*************************************************************************** '''
# VERTIKALNA GLAVA -vg
vginstrument1EntryDiaValue = StringVar()
vginstrument1EntrySkorostValue = StringVar()
vginstrument2EntryDiaValue = StringVar()
vginstrument2EntrySkorostValue = StringVar()
vginstrument3EntryDiaValue = StringVar()
vginstrument3EntrySkorostValue = StringVar()
vginstrument4EntryDiaValue = StringVar()
vginstrument4EntrySkorostValue = StringVar()
vginstrument5EntryDiaValue = StringVar()
vginstrument5EntrySkorostValue = StringVar()

# HORIZONTALNA GLAVA -vg
hginstrument1EntryDiaValue = StringVar()
hginstrument1EntrySkorostValue = StringVar()
hginstrument2EntryDiaValue = StringVar()
hginstrument2EntrySkorostValue = StringVar()
hginstrument3EntryDiaValue = StringVar()
hginstrument3EntrySkorostValue = StringVar()
hginstrument4EntryDiaValue = StringVar()
hginstrument4EntrySkorostValue = StringVar()
hginstrument5EntryDiaValue = StringVar()
hginstrument5EntrySkorostValue = StringVar()

# Default values (she doidat posle of file)
vginstrument1EntryDiaValue.set(instrumentiOtConfig['T1'][0])
vginstrument1EntrySkorostValue.set(instrumentiOtConfig['T1'][1])
vginstrument2EntryDiaValue.set(instrumentiOtConfig['T2'][0])
vginstrument2EntrySkorostValue.set(instrumentiOtConfig['T2'][1])
vginstrument3EntryDiaValue.set(instrumentiOtConfig['T3'][0])
vginstrument3EntrySkorostValue.set(instrumentiOtConfig['T3'][1])
vginstrument4EntryDiaValue.set(instrumentiOtConfig['T4'][0])
vginstrument4EntrySkorostValue.set(instrumentiOtConfig['T4'][1])
vginstrument5EntryDiaValue.set(instrumentiOtConfig['T5'][0])
vginstrument5EntrySkorostValue.set(instrumentiOtConfig['T5'][1])

hginstrument1EntryDiaValue.set(instrumentiOtConfig['T6'][0])
hginstrument1EntrySkorostValue.set(instrumentiOtConfig['T6'][1])
hginstrument2EntryDiaValue.set(instrumentiOtConfig['T7'][0])
hginstrument2EntrySkorostValue.set(instrumentiOtConfig['T7'][1])
hginstrument3EntryDiaValue.set(instrumentiOtConfig['T8'][0])
hginstrument3EntrySkorostValue.set(instrumentiOtConfig['T8'][1])
hginstrument4EntryDiaValue.set(instrumentiOtConfig['T9'][0])
hginstrument4EntrySkorostValue.set(instrumentiOtConfig['T9'][1])
hginstrument5EntryDiaValue.set(instrumentiOtConfig['T10'][0])
hginstrument5EntrySkorostValue.set(instrumentiOtConfig['T10'][1])

genHorizontOtvoriGCodeValue = IntVar()
genVertikalOtvoriGCodeValue = IntVar()
pauseMejduDetailiGCodeValue = IntVar()
ciklichnoPrezarejdaneGCodeValue = IntVar()

genHorizontOtvoriGCodeValue.set(1)
genVertikalOtvoriGCodeValue.set(1)

leftBazaCheckBox = IntVar()
rightBazaCheckBox = IntVar()

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
        
''' ***************************************************************************
*** Variables za stoinosti na vertikalnite otvori
*************************************************************************** '''
vertikalenOtvorXValue = StringVar()
vertikalenOtvorYValue = StringVar()
vertikalenOtvorDiamValue = StringVar()
vertikalenOtvorDulbochinaValue = StringVar()
raztoqnieMejduVertikalniValue = StringVar()
broiVertikalniOtvoriValue = IntVar()
simetrichnoOtvorPoXValue = IntVar()
simetrichnoOtvorPoYValue = IntVar()

raztoqnieMejduVertikalniValue.set('0')
broiVertikalniOtvoriValue.set(1)
''' ***************************************************************************
*** Variables za stoinosti na horizontalnite otvori
*************************************************************************** '''
horizontalenOtvorXValue = StringVar()
horizontalenOtvorDiamValue = StringVar()
dulbochinaHorizontalenOtvorValue = StringVar()
raztoqnieMejduHorizontalenValue = StringVar()
broiHorizontalniOtvoriValue = IntVar()
simetrichnoHorizontalenOtvorPoXValue = IntVar()
simetrichnoHorizontalenOtvorPoYValue = IntVar()

raztoqnieMejduHorizontalenValue.set('0')
broiHorizontalniOtvoriValue.set(1)
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

# ********** Buttons za masata *************
buttonsZaMasataFrame = Frame(mainframe)
buttonsZaMasataFrame.grid(row=1, column=2, columnspan=2, sticky=W+E)

leftBazaLabelBox = LabelFrame(buttonsZaMasataFrame, text=leftBazaGrouperText)
leftBazaLabelBox.grid(row=0, sticky=W, padx=20, pady=2)
rotateButtonLeftBaza = Button(leftBazaLabelBox, text=rotateButtonText, bg="lightblue", command=rotate_element_lqva_baza)
rotateButtonLeftBaza.grid(row=0, sticky=W, padx=2, pady=2)
removeElementButtonLeftBaza = Button(leftBazaLabelBox, text=removeButtonText, bg="lightblue", command=mahni_element_ot_lqva_baza)
removeElementButtonLeftBaza.grid(row=0, column=1, sticky=W, padx=2, pady=2)
editButtonLeftBaza = Button(leftBazaLabelBox, text=editButtonText, bg="lightblue", command=redaktirai_lqv_detail)
editButtonLeftBaza.grid(row=0, column=2, sticky=W, padx=2, pady=2)

pripluzniButton = Button(buttonsZaMasataFrame, text=pripluzniButtonText, bg="lightblue", state=DISABLED, command=pripluzni_element)
rightBazaLabelBox = LabelFrame(buttonsZaMasataFrame, text=rightBazaGrouperText)
if useLowerResolution == 1:
    pripluzniButton.grid(row=0, column=1, padx=50, pady =5, sticky=S)
    rightBazaLabelBox.grid(row=0, column=2, sticky=W,padx=20, pady=2)
else:
    pripluzniButton.grid(row=0, column=1, padx=100, pady =5, sticky=S)
    rightBazaLabelBox.grid(row=0, column=2, sticky=E, padx=20, pady=2)
rotateButtonRightBaza = Button(rightBazaLabelBox, text=rotateButtonText, bg="lightblue", command=rotate_element_dqsna_baza)
rotateButtonRightBaza.grid(row=0, sticky=W, padx=2, pady=2)
removeElementButtonRightBaza = Button(rightBazaLabelBox, text=removeButtonText, bg="lightblue", command=mahni_element_ot_dqsna_baza)
removeElementButtonRightBaza.grid(row=0, column=1, sticky=W, padx=2, pady=2)
editButtonRightBaza = Button(rightBazaLabelBox, text=editButtonText, bg="lightblue", command=redaktirai_desen_detail)
editButtonRightBaza.grid(row=0, column=2, sticky=W, padx=2, pady=2)

# ********** Listbox *************
listboxLabelFrame = LabelFrame(mainframe, text=detailiLabelText)
listboxLabelFrame.grid(row=2, sticky=N+S, padx=10)
listboxHorizontalScrollbar = Scrollbar(listboxLabelFrame,  orient=HORIZONTAL)
listboxHorizontalScrollbar.grid(row=1, column=0, sticky=E+W)
listboxVerticalScrollbar = Scrollbar(listboxLabelFrame, orient=VERTICAL)
listboxVerticalScrollbar.grid(row=0, column=1, sticky=N+S)
listbox = Listbox(listboxLabelFrame, width=listboxW, height=listboxH, xscrollcommand=listboxHorizontalScrollbar.set, yscrollcommand=listboxVerticalScrollbar.set)
listbox.grid(row=0, sticky=N+S, padx=10)
listboxHorizontalScrollbar.config(command=listbox.xview)
listboxVerticalScrollbar.config(command=listbox.yview)

iztriiVsichkoButton = Button(listboxLabelFrame, text=izchistiVsichkoButtonText, command=izchisti_vschki_detaili)
iztriiDetailButton = Button(listboxLabelFrame, text=izchistiIzbranDetailButtonText, command=izchisti_izbrania_detail)
if useLowerResolution == 1:
    iztriiVsichkoButton.grid(row=4, padx = 10, pady=5, sticky=E)
    iztriiDetailButton.grid(row=5, padx=10, sticky=E)
else:
    iztriiVsichkoButton.grid(row=4, padx = 10, pady=10, sticky=W)
    iztriiDetailButton.grid(row=4, padx=10, pady=10, sticky=E)

# ********** Frame *************
frame = Frame(mainframe)
frame.grid(row=2, column=1, sticky=N+S)

# ********** Move Button *************
slojiLqvaBazaButton = Button(frame, text=placeOnMachineButtonText, bg="bisque", command=izberi_element_za_lqva_strana)
slojiLqvaBazaButton.grid(row=0, padx = 3, sticky=N)

slojiDqsnaBazaButton = Button(frame, text=placeOnMachineRightButtonText, bg="bisque", command=izberi_element_za_dqsna_strana)
slojiDqsnaBazaButton.grid(row=0, column=1, padx = 3, sticky=N)

# ********** Instrumenti *************
nastorikaNaInstrButton = Button(frame, text=nastroikaInstrumentButtonText, command=nastroika_na_instrumenti)
nastorikaNaInstrButton.grid(row=1, columnspan=2, padx=3, pady=30)

# ********** Generate G-Code Button *************
gCodeLableBox = LabelFrame(frame, text=generateGCodeLabelText)
gCodeLableBox.grid(row=2, columnspan=3, padx = 20, sticky=N+S+W+E)

genHorOtvoriButton= Checkbutton(gCodeLableBox, text=genHorizontOtvoriButtonText, variable=genHorizontOtvoriGCodeValue)
genHorOtvoriButton.grid(row=1, sticky=W)
genVerOtvoriButton= Checkbutton(gCodeLableBox, text=genVertikalOtvoriButtonText, variable=genVertikalOtvoriGCodeValue)
genVerOtvoriButton.grid(row=2, sticky=W)
pauseButton= Checkbutton(gCodeLableBox, text=pauseMejduDetailiButtonText, variable=pauseMejduDetailiGCodeValue)
pauseButton.grid(row=3, sticky=W)
ciklichnoButton= Checkbutton(gCodeLableBox, text=ciklichnoPrezarejdaneButtonText, variable=ciklichnoPrezarejdaneGCodeValue)
ciklichnoButton.grid(row=4, sticky=W)

buttonBar = Frame(gCodeLableBox)
buttonBar.grid(row=5)
generateGCodeButton = Button(buttonBar, text=generateGCodeButtonText, bg="tomato", command=suzdai_gcode_file)
generateGCodeButton.grid(row=0, padx= 3, pady = 10, sticky=W)
iztriiGCodeButton = Button(buttonBar, text=iztriiGCodeButtonText, bg="tomato", command=iztrii_temp_gcode_file)
iztriiGCodeButton.grid(row=0, column=1,padx = 3, pady = 10)
zapisGCodeButton = Button(buttonBar, text=zapisGCodeButtonText, bg="tomato", command=zapishi_gcode_file)
zapisGCodeButton.grid(row=0, column=2, padx = 3, pady = 10, sticky=E)

# ********** List box - Steps *************
stepsList = Listbox(frame, height = 15)
stepsList.grid(row=3, padx = 2, pady = 30, columnspan=2,sticky=N+S+W+E)
    
# ********** Canvas *************
canvasFrame = Frame(mainframe, bd=2, relief=SUNKEN)
canvasFrame.grid(row=2, column=2, columnspan = 2, padx=10, sticky=W+E+N+S)
xscrollbar = Scrollbar(canvasFrame, orient=HORIZONTAL)
xscrollbar.grid(row=1, column=0,sticky=E+W)
yscrollbar = Scrollbar(canvasFrame)
yscrollbar.grid(row=0, column=1, sticky=N+S)
canvas = Canvas(canvasFrame, bd=0, width=canvasW, heigh=canvasH, scrollregion=(0, 0, 2000, 2000),
                xscrollcommand=xscrollbar.set,
                yscrollcommand=yscrollbar.set)
canvas.grid(row=0, column=0, sticky=N+S+E+W)
xscrollbar.config(command=canvas.xview)
yscrollbar.config(command=canvas.yview)

#canvas = Canvas(mainframe, width=1100, heigh=700, bg="grey")
#Slojib bg = grey za da vijdam kude e canvas
#canvas.grid(row=2, column=2, columnspan = 2, padx=20, sticky=W+E+N+S)

# ********** Masa *************
# Originalen razmer e 1500 mm na 600 mm. Mashtab (x 0.5) => duljinata e 750 i shirina e 300.
# Sledovatelno koordinatite she sa offset s nachalnata tochka. (+20)
masa = canvas.create_rectangle(20, 20, PLOT_NA_MACHINA_X*mashtab+20, PLOT_NA_MACHINA_Y*mashtab+20, fill="bisque")

mainframe.update()
mainframe.minsize(mainframe.winfo_width(), mainframe.winfo_height())
mainframe.mainloop()

print ('*** END PROGRAM *************************')
