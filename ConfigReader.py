#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

def read_instruments():    
    # _d e diametur; _s e skorost
    t1_d = 35
    t1_s = 1000
    t2_d = 15
    t2_s = 1000
    t3_d = 8
    t3_s = 1200
    t4_d = 5
    t4_s = 1500
    t5_d = 2.5
    t5_s = 1500
    t6_d = 35
    t6_s = 800
    t7_d = 15
    t7_s = 1000
    t8_d = 8
    t8_s = 1200
    t9_d = 5
    t9_s = 1500
    t10_d = 2.5
    t10_s = 1500
    
    if os.path.isfile("bxfconfig.config"):
        configFile = open("bxfconfig.config", "r")
         
        for line in configFile:
            t, vs = line.split('=')
            d, s = vs.split(';')
            if t == 'T1':
                t1_d = float(d)
                t1_s = float(s)
            elif t == 'T2':
                t2_d = float(d)
                t2_s = float(s)
            elif t == 'T3':
                t3_d = float(d)
                t3_s = float(s)
            elif t == 'T4':
                t4_d = float(d)
                t4_s = float(s)
            elif t == 'T5':
                t5_d = float(d)
                t5_s = float(s)
            elif t == 'T6':
                t6_d = float(d)
                t6_s = float(s)
            elif t == 'T7':
                t7_d = float(d)
                t7_s = float(s)
            elif t == 'T8':
                t8_d = float(d)
                t8_s = float(s)
            elif t == 'T9':
                t9_d = float(d)
                t9_s = float(s)
            elif t == 'T10':
                t10_d = float(d)
                t10_s = float(s)
        configFile.close()
        
    return {'T1':(t1_d,t1_s),'T2':(t2_d,t2_s),'T3':(t3_d,t3_s),'T4':(t4_d,t4_s),'T5':(t5_d,t5_s),'T6':(t6_d,t6_s),'T7':(t7_d,t7_s),'T8':(t8_d,t8_s),'T9':(t9_d,t9_s),'T10':(t10_d,t10_s)}

def write_instruments(verIns, horIns, skorosti):
        if os.path.isfile("bxfconfig.config"):
            configFile = open("bxfconfig.config", "r")  
            vsichko = configFile.readlines()
            configFile.close()
            
            configFileW = open("bxfconfig.config", "w") 
            for line in vsichko:
                if line.startswith('T'):
                    t, vs = line.split('=')
                    if t == 'T1':
                        newLine = 'T1='+str(verIns['T1'])+';'+str(skorosti['T1'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T2':
                        newLine = 'T2='+str(verIns['T2'])+';'+str(skorosti['T2'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T3':
                        newLine = 'T3='+str(verIns['T3'])+';'+str(skorosti['T3'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T4':
                        newLine = 'T4='+str(verIns['T4'])+';'+str(skorosti['T4'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T5':
                        newLine = 'T5='+str(verIns['T5'])+';'+str(skorosti['T5'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T6':
                        newLine = 'T6='+str(horIns['T6'])+';'+str(skorosti['T6'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T7':
                        newLine = 'T7='+str(horIns['T7'])+';'+str(skorosti['T7'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T8':
                        newLine = 'T8='+str(horIns['T8'])+';'+str(skorosti['T8'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T9':
                        newLine = 'T9='+str(horIns['T9'])+';'+str(skorosti['T9'])+'\n'
                        configFileW.write(newLine)
                    elif t == 'T10':
                        newLine = 'T10='+str(horIns['T10'])+';'+str(skorosti['T10'])+'\n'
                        configFileW.write(newLine)
                    else:
                        configFileW.write(line)
                else:
                    configFileW.write(line)
            configFileW.close()
        else:
            print 'File bxfconfig.config does not exists. To be continued ...'
        
def sort_detail_list(detaili):
    defaultOrder = {'Oberboden':1, 'Oberboden-OTRAVHIN':2, 'Oberboden-OTRAVVOR':3, 
                    'Unterboden':4,
                    'LinkeSeitenwand':5,
                    'RechteSeitenwand':6,
                    'KorpusRueckwand':7,
                    'Tuer':8,
                    'Doppeltuer':9,
                    'Aussenschubkasten-Front':10,'Aussenschubkasten-Boden':11,'Aussenschubkasten-Rueckwand':12,
                    'Klappensystem':13,
                    'customdetail':100}
    
    sortingList = []
    
    for key, value in detaili.iteritems():
        print key
        razmer = value.razmeri
        imeValue = value.ime
        element_x = razmer['x']
        element_y = razmer['y']
        debelina = razmer['h']
        if 'Aussenschubkasten' in key:
            auss = key.split('-')
            aussName = auss[1]
            aussId = auss[3]
            if 'Front' in key:
                prevod = u'Чекмедже-'+aussName+u': Лице-'+aussId+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
                sortingPlace = defaultOrder['Aussenschubkasten-Front']
                ttuple = sortingPlace, prevod, key
            elif 'Rueckwand' in key:
                prevod = u'Чекмедже-'+aussName+u': Гръб-'+aussId+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
                sortingPlace = defaultOrder['Aussenschubkasten-Rueckwand']
                ttuple = sortingPlace, prevod, key
            elif 'Boden' in key:
                prevod = u'Чекмедже-'+aussName+u': Дъно-'+aussId+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
                sortingPlace = defaultOrder['Aussenschubkasten-Boden']
                ttuple = sortingPlace, prevod, key
            sortingList.append(ttuple)
        elif 'LinkeSeitenwand' in key:
            prevod = u'Лява страница на корпуса'+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            #prevod = pad_with_dot(u'Лява страница на корпуса', str(element_x), str(element_y))
            sortingPlace = defaultOrder['LinkeSeitenwand']
            ttuple = sortingPlace, prevod, key
            sortingList.append(ttuple)
        elif 'RechteSeitenwand' in key:
            prevod = u'Дясна страница на корпуса'+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            #prevod = pad_with_dot(u'Дясна страница на корпуса', str(element_x), str(element_y))
            sortingPlace = defaultOrder['RechteSeitenwand']
            ttuple = sortingPlace, prevod, key
            sortingList.append(ttuple)
        elif 'KorpusRueckwand' in key:
            prevod = u'Гръб на корпуса'+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            sortingPlace = defaultOrder['KorpusRueckwand']
            ttuple = sortingPlace, prevod, key
            sortingList.append(ttuple)
        elif 'Oberboden-OTRAVVOR' in key:
            prevod = u'Горна царга отпред'+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            sortingPlace = defaultOrder['Oberboden-OTRAVVOR']
            ttuple = sortingPlace, prevod, key
            sortingList.append(ttuple)
        elif 'Oberboden-OTRAVHIN' in key:
            prevod = u'Горна царга отзад'+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            sortingPlace = defaultOrder['Oberboden-OTRAVHIN']
            ttuple = sortingPlace, prevod, key    
            sortingList.append(ttuple)
        elif 'Unterboden' in key:
            prevod = u'Дъно'+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            sortingPlace = defaultOrder['Unterboden']
            ttuple = sortingPlace, prevod, key  
            sortingList.append(ttuple)
        elif 'Tuer' in key:
            prevod = u'Врата'+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            sortingPlace = defaultOrder['Tuer']
            ttuple = sortingPlace, prevod, key  
            sortingList.append(ttuple)
        elif 'Doppeltuer' in key:
            prevod = u'Двойна врата'+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            sortingPlace = defaultOrder['Tuer']
            ttuple = sortingPlace, prevod, key  
            sortingList.append(ttuple)
        elif 'customdetail' in key:
            prevod = u'Въведен детайл: '+imeValue+' ..... '+str(element_x)+' x '+str(element_y)+' x '+str(debelina)
            sortingPlace = defaultOrder['customdetail']
            ttuple = sortingPlace, prevod, key  
            sortingList.append(ttuple)
    
    return sorted(sortingList, key=lambda element: (element[0], element[1]))
    
def pad_with_dot(prevod, elementx, elementy):
    total = len(prevod) + len(elementx) + len(elementy) + 5
    stringToReturn = prevod+' '
    
    dots = 50 - total
    while dots > 0:
        stringToReturn = stringToReturn+'.'
        dots = dots - 1
    
    stringToReturn = stringToReturn+' '+elementx+' x '+elementy
    return stringToReturn
        
         
        