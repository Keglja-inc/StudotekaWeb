# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app
from studoteka import baseSession
from studoteka.dbKlase import Fakultet, VisokoUciliste
from flask import Response
import json, hashlib

@app.route('/rest/'+hashlib.sha1(('popisSveucilistaFakulteta').encode()).hexdigest())
#27543538596b07668329373594a3baaf886420a4
def dohvatiSveucilistaFakultete():
    result = {
        "status" : False,
        "message" : "Neuspješno dohvaćanje!",
        "podaci" : []
    }
    try:
        for instance in baseSession.query(VisokoUciliste).order_by(VisokoUciliste.idVisokogUcilista):
            dodaj = {}
            dodaj["uciliste"] = instance.naziv
            dodaj["fakulteti"] = []
            for k in instance.fakulteti:
                fak = {
                    "naziv" : k.naziv
                }
                dodaj["fakulteti"].append(fak) 
            result["podaci"].append(dodaj)
        result["status"] = True
        result["message"] = "Podaci uspješno dohvaćeni."
    except (BaseException):
        baseSession.rollback()
        
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')

@app.route('/rest/'+hashlib.sha1(('popisFakulteta').encode()).hexdigest())
#cfddc7067c795d46f676c358dc6aacfcd20c195c
def dohvatiFakultete():
    result = {
        "status" : False,
        "message" : "Neuspješno dohvaćanje!",
        "podaci" : []
    }
    
    try:
        for instance in baseSession.query(Fakultet).order_by(Fakultet.idFakulteta):
            dodaj = {}
            dodaj["naziv"] = instance.naziv
            dodaj["url"] = instance.webStranica
            result["podaci"].append(dodaj)
        result["status"] = True
        result["message"] = "Podaci uspješno dohvaćeni."
    except (BaseException):
        pass
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')