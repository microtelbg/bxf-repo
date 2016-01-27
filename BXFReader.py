#!/usr/bin/python
# -*- coding: utf-8 -*-

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
instrumentiLabelText = 'Инструменти'

''' ***************************************************************************
*** Global Variables
*************************************************************************** '''
ns = {'blum' : 'http://www.blum.com/bxf'}
mashtab = 0.5
filename = 'tester.bxf'

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
    print elementi_za_dupchene
    for ek, ev in elementi_za_dupchene.iteritems():
        listbox.insert(END, ek)

def izberi_element_za_dupchene():
      
    #Nameri izbrania element
    itemIndex = int(listbox.curselection()[0])
    itemValue = listbox.get(itemIndex)

    izbranElement = elementi_za_dupchene[itemValue]

    #Sloji elementa v lista i purvonachalnata orientacia
    izbrani_elementi['L'] = izbranElement
    izbrani_elementi['LO'] = 0

    print izbranElement.opisanie()

    narisuvai_po_horizontalata(izbranElement, 0)

def narisuvai_strana_na_plota(shirina, duljina):
    canvas.create_rectangle(30, 30, shirina+30, duljina+30, fill="lightblue")

def narisuvai_dupka_na_plota(xcoordinata, ycoordinata, radius):
    nachalo_x = 30 + (xcoordinata - radius)
    nachalo_y = 30 + (ycoordinata - radius)
    krai_x = 30 + (xcoordinata + radius)
    krai_y = 30 + (ycoordinata + radius)

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

    if newOrientation == 0:
        narisuvai_po_horizontalata(izbranElement, newOrientation)
    elif newOrientation == 1:
        narisuvai_po_verticalata(izbranElement, newOrientation)
    elif newOrientation == 2:
        narisuvai_po_horizontalata(izbranElement, newOrientation)
    elif newOrientation == 3:
        narisuvai_po_verticalata(izbranElement, newOrientation)
        

def narisuvai_po_horizontalata(izbranElement, rotation):
    #Reset
    canvas.delete(ALL)
    canvas.create_rectangle(20, 20, 770, 320, fill="bisque")

    #Vzemi razmerite na stranata
    razmeri_na_elementa = izbranElement.razmeri
    orientacia_na_elementa = razmeri_na_elementa['orientation']
    if orientacia_na_elementa == 'xz':
        masa_x = float(razmeri_na_elementa['z'])*mashtab
        masa_y = float(razmeri_na_elementa['x'])*mashtab
    elif orientacia_na_elementa == 'yz':
        masa_x = float(razmeri_na_elementa['y'])*mashtab
        masa_y = float(razmeri_na_elementa['z'])*mashtab
    elif orientacia_na_elementa == 'xy':
        masa_x = float(razmeri_na_elementa['y'])*mashtab
        masa_y = float(razmeri_na_elementa['x'])*mashtab

    #Nachertai elementa vurhu plota na machinata
    narisuvai_strana_na_plota(masa_x, masa_y)

    dupki_na_elementa = izbranElement.dupki
    for dupka in dupki_na_elementa:
        if orientacia_na_elementa == 'xz':
            d_x = float(dupka['z'])*mashtab
            d_y = float(dupka['x'])*mashtab
            d_r = float(dupka['r'])*mashtab
        elif orientacia_na_elementa == 'yz':
            d_x = float(dupka['y'])*mashtab
            d_y = float(dupka['z'])*mashtab
            d_r = float(dupka['r'])*mashtab
        elif orientacia_na_elementa == 'xy':
            d_x = float(dupka['y'])*mashtab
            d_y = float(dupka['x'])*mashtab
            d_r = float(dupka['r'])*mashtab
        
        if rotation == 2:
            d_x = masa_x - d_x
            d_y = masa_y - d_y
                 
        narisuvai_dupka_na_plota(d_x, d_y, d_r)

        

def narisuvai_po_verticalata(izbranElement, rotation):
    #Reset
    canvas.delete(ALL)
    canvas.create_rectangle(20, 20, 770, 320, fill="bisque")

    #Vzemi razmerite na stranata
    razmeri_na_elementa = izbranElement.razmeri
    orientacia_na_elementa = razmeri_na_elementa['orientation']
    if orientacia_na_elementa == 'xz':
        masa_x = float(razmeri_na_elementa['x'])*mashtab
        masa_y = float(razmeri_na_elementa['z'])*mashtab
    elif orientacia_na_elementa == 'yz':
        masa_x = float(razmeri_na_elementa['z'])*mashtab
        masa_y = float(razmeri_na_elementa['y'])*mashtab
    elif orientacia_na_elementa == 'xy':
        masa_x = float(razmeri_na_elementa['x'])*mashtab
        masa_y = float(razmeri_na_elementa['y'])*mashtab

    #Nachertai elementa vurhu plota na machinata
    narisuvai_strana_na_plota(masa_x, masa_y)

    dupki_na_elementa = izbranElement.dupki
    for dupka in dupki_na_elementa:
        if orientacia_na_elementa == 'xz':
            d_x = float(dupka['x'])*mashtab
            d_y = float(dupka['z'])*mashtab
            d_r = float(dupka['r'])*mashtab
        elif orientacia_na_elementa == 'yz':
            d_x = float(dupka['z'])*mashtab
            d_y = float(dupka['y'])*mashtab
            d_r = float(dupka['r'])*mashtab
        elif orientacia_na_elementa == 'xy':
            d_x = float(dupka['x'])*mashtab
            d_y = float(dupka['y'])*mashtab
            d_r = float(dupka['r'])*mashtab
            
        if rotation == 1:
            d_x = masa_x - d_x
        elif rotation == 3:
            d_y = masa_y - d_y
            
        narisuvai_dupka_na_plota(d_x, d_y, d_r)


print ('*** BEGIN PROGRAM *************************')
mainframe = Tk()
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
instrumentiLabel = Label(frame, text=instrumentiLabelText)
instrumentiLabel.grid(row=1, columnspan=2, pady=10)

instr1Label = Label(frame, text='1:')
instr1Label.grid(row=2, sticky=W)

instr1Entry = Entry(frame)
instr1Entry.grid(row=2, column=1, sticky=E)

instr2Label = Label(frame, text='2:')
instr2Label.grid(row=3, sticky=W)

instr2Entry = Entry(frame)
instr2Entry.grid(row=3, column=1, sticky=E)

instr3Label = Label(frame, text='3:')
instr3Label.grid(row=4, sticky=W)

instr3Entry = Entry(frame)
instr3Entry.grid(row=4, column=1, sticky=E)

instr4Label = Label(frame, text='4:')
instr4Label.grid(row=5, sticky=W)

instr4Entry = Entry(frame)
instr4Entry.grid(row=5, column=1, sticky=E)

instr5Label = Label(frame, text='5:')
instr5Label.grid(row=6, sticky=W)

instr5Entry = Entry(frame)
instr5Entry.grid(row=6, column=1, sticky=E)
# ********** Canvas *************
canvas = Canvas(mainframe, width=1100, heigh=700, bg="grey")
#Slojib bg = grey za da vijdam kude e canvas
canvas.grid(row=2, column=2, padx=20, sticky=W+E+N+S)

# ********** Masa *************
# Originalen razmer e 1500 mm na 600 mm. Mashtab (x 0.5) => duljinata e 750 i shirina e 300.
# Sledovatelno koordinatite she sa offset s nachalnata tochka. (+20)
masa = canvas.create_rectangle(20, 20, 770, 320, fill="bisque")


mainframe.mainloop()

print ('*** END PROGRAM *************************')
