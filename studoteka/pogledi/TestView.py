# -*- coding: utf-8 -*-
'''
Created on 31. svi 2015.

@author: spicko
'''
from studoteka import app, baseSession
from studoteka.dbKlase import Interes, Fakultet, Ucenik, VisokoUciliste

@app.route("/test")
def testiranje():
    '''
    for instance in baseSession.query(Fakultet).order_by(Fakultet.idFakulteta):
        print(instance.naziv)
        for zapis in instance.interesi:
            print(zapis.interes.naziv)
    print("-------------------------------------------")
    for instance in baseSession.query(Interes).order_by(Interes.idInteresa):
        print(instance.naziv)
        for zapis in instance.fakulteti:
            print(zapis.fakultet.naziv)'''
    vu = baseSession.query(VisokoUciliste).filter(VisokoUciliste.idVisokogUcilista == 1).first()
    print(vu.statusVisokogUcilista.opis)
    print(vu.tipVisokogUcilista.opis)
    return ""