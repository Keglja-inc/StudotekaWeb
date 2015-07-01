# -*- coding: utf-8 -*-
'''
Created on 22. lip 2015.

@author: spicko
'''
from studoteka import app, baseSession
from flask import Response, request
import hashlib, datetime, json
from sqlalchemy import and_
from studoteka.dbKlase import Interes, Ucenik, JeZainteresiran, PonudaInteresa,\
    Pripada, Dnevnik

@app.route('/rest/'+hashlib.sha1(('dohvatiFakultetePoInteresima').encode()).hexdigest(), methods=['POST'])
#37ecc108d4142d31b0bac403328b644ab2cf6b9d
def dohvatiFakultetePoInteresima():
    ''' Funkcija dohvaća fakultete po prioritetima. Funkcija ne prima parametre već prihvaća POST HTTP request'''
    result = {
        'status' : False,
        'vrijeme' : str(datetime.datetime.now()),
        'poruka' : ""
    }
    data = request.get_json(force=True)
    
    try:
        listaInteresa = data["interesi"]
        ucenikEmail = data["email"]
    except (KeyError):
        result["poruka"] = "Pogreška kod podataka!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    if len(listaInteresa) == 0:
        result["poruka"] = "Niste poslali podatke!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    popis = []
    try:
        a = int(listaInteresa[0])
        popis = listaInteresa
    except ValueError:
        temp = listaInteresa[1:-1].split(", ")
        for i in temp:
            popis.append(int(i))
    
    try:
        ucenik = baseSession.query(Ucenik).filter(Ucenik.email == ucenikEmail).first()
        
        try:
            dnevnik = Dnevnik(ucenik.idUcenika, "Ucenik", "Dohvat fakulteta po interesima")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException):
            baseSession.rollback()
            pass
        
    except BaseException as e:
        result["poruka"] = "Greška kod korisnika!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        baseSession.query(JeZainteresiran).filter(JeZainteresiran.ucenik_idUcenika == ucenik.idUcenika).delete()
        baseSession.commit()
        for i in popis:
            interes = baseSession.query(Interes).filter(Interes.idInteresa == i).first()
            interesUcenika = JeZainteresiran()
            interesUcenika.interes = interes
            interesUcenika.ucenik = ucenik
            baseSession.add(interesUcenika)
        baseSession.commit()
    except BaseException:
        result["poruka"] = "Nepostojeći interesi!"
        baseSession.rollback()
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    brojOdabranihInteresa = 0
    
    try:
        spremljeniInteresi = baseSession.query(JeZainteresiran).filter(JeZainteresiran.ucenik == ucenik)
        baseSession.query(Pripada).filter(Pripada.ucenik_idUcenika == ucenik.idUcenika).delete()
        baseSession.commit()
    except (BaseException):
        result["poruka"] = "Pogreška s bazom!"
        baseSession.rollback()
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        for inte in spremljeniInteresi:
            brojOdabranihInteresa += 1
            fakultetiPonuda = baseSession.query(PonudaInteresa).filter(PonudaInteresa.interes_idInteresa == inte.interes_idInteresa)
            for fak in fakultetiPonuda:
                prip = baseSession.query(Pripada).filter(and_(Pripada.fakultet_idFakulteta == fak.fakultet.idFakulteta, Pripada.ucenik_idUcenika == ucenik.idUcenika)).first()
                if prip == None:
                    prip = Pripada()
                    prip.fakultet = fak.fakultet
                    prip.ucenik = ucenik
                    prip.brojHitova = 1
                else:
                    prip.brojHitova += 1
                baseSession.add(prip)
                baseSession.commit()
    except BaseException:
        result["poruka"] = "Pogreška kod izračuna!"
        baseSession.rollback()
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        pripadaju = baseSession.query(Pripada).filter(Pripada.ucenik == ucenik)
        for pripada in pripadaju:
            pripada.postotak = pripada.brojHitova/brojOdabranihInteresa*100
            baseSession.add(pripada)
        baseSession.commit()
    except BaseException:
        result["poruka"] = "Poreška kod izračuna postotka!"
        baseSession.rollback()
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        pripadaju = baseSession.query(Pripada).filter(Pripada.ucenik == ucenik).order_by(Pripada.postotak.desc())
        i = 1
        for pripada in pripadaju:
            pripada.prioritet = i
            i += 1
            baseSession.add(pripada)
        baseSession.commit()
    except BaseException:
        result["poruka"] = "Pogreška kod izračuna prioriteta!"
        baseSession.rollback()
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        pripadaju = baseSession.query(Pripada).filter(Pripada.ucenik == ucenik).order_by(Pripada.prioritet.asc())
        brZapisa = 0
        result["podaci"] = []
        for pripada in pripadaju:
            brZapisa += 1
            a = {
                 "nazivFakulteta" : pripada.fakultet.naziv,
                 "postotak" : pripada.postotak,
                 "url" : pripada.fakultet.webStranica
            }
            result["podaci"].append(a)
        result["status"] = True
        result["brojZapisa"] = brZapisa
    except BaseException:
        result["poruka"] = "Pogreška kod dohvata podataka!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('testFakulteti').encode()).hexdigest(), methods=['POST'])
#715e63e6474094cbfd9a05bc7719ca8b814fdba1
def testFakulteti():
    result = {
        "poruka" : "Ovo je rezultat"
    }
    
    data = request.get_json(force=True)
    result["poruka"] = "Poslal si " + data["email"] + " " + data["naziv"] + " " + data["interesi"]
    result["status"] = True
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')