# -*- coding: utf-8 -*-
'''
Created on 22. lip 2015.

@author: spicko
'''
from studoteka import app, baseSession, session
import hashlib, json
from flask import Response
from studoteka.dbKlase import Fakultet, Ucenik, Pripada, Dnevnik
from studoteka.LoginSupport import potrebnaPrijava

@app.route('/rest/'+hashlib.sha1(('prioritetiPoFakultetu').encode()).hexdigest(), methods=['GET'])
#f10b84c033e39eb4298c01d05cd1b6cabcb45158
@potrebnaPrijava
def prioritetiPoFakultetu():
    result = {
        "status" : False
    }
    try:
        idFak = session["user_data"]["idFakulteta"]
        pripadaju = baseSession.query(Pripada).filter(Pripada.fakultet_idFakulteta == idFak)
        brojPrioriteta = [0,0,0,0,0]
        for pripada in pripadaju:
            if(pripada.prioritet == 1):
                brojPrioriteta[0] += 1
            elif (pripada.prioritet == 2):
                brojPrioriteta[1] += 1
            elif (pripada.prioritet == 3):
                brojPrioriteta[2] += 1
            elif (pripada.prioritet == 4):
                brojPrioriteta[3] += 1
            elif (pripada.prioritet == 5):
                brojPrioriteta[4] += 1
            else:
                pass
        result["podaci"] = brojPrioriteta
        result["status"] = True
        
        try:
            dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Dohvaćanje statistike - Prioriteti po fakultetu")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException, KeyError):
            baseSession.rollback()
            pass
        
    except (BaseException, KeyError):
        pass
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('postociPoFakultetu').encode()).hexdigest(), methods=['GET'])
#5beabefdf587548578e92f28f07e3c435e574bf7
@potrebnaPrijava
def postociPoFakultetu():
    result = {
        "status" : False,
        "podaci" : []
    }
    
    try:
        idFak = session["user_data"]["idFakulteta"]
        pripadaju = baseSession.query(Pripada).filter(Pripada.fakultet_idFakulteta == idFak).order_by(Pripada.postotak.desc())
        pripadaju1 = baseSession.query(Pripada).filter(Pripada.fakultet_idFakulteta == idFak).group_by(Pripada.postotak).order_by(Pripada.postotak.desc())
        lista = []
        for pripada in pripadaju:
            lista.append(pripada.postotak)
        for pripada in pripadaju1:
            a = {
                 "postotak" : pripada.postotak,
                 "broj" : lista.count(pripada.postotak)
            }
            result["podaci"].append(a)
        result["status"] = True
        
        try:
            dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Dohvaćanje statistike - Postoci po fakultetu")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException, KeyError):
            baseSession.rollback()
            pass
        
    except (BaseException, KeyError):
        pass
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('fakseviPoPrioritetuJedan').encode()).hexdigest(), methods=['GET'])
#f4af7f520c332ab2a3b8fe9a8ccd0cb9e4e65ffc
@potrebnaPrijava
def fakseviPoPrioritetuJedan():
    result = {
        "status" : False,
        "podaci" : []
    }
    try:
        pripadaju = baseSession.query(Pripada).filter(Pripada.prioritet == 1).order_by(Pripada.fakultet_idFakulteta.asc())
        pripadajuDist = baseSession.query(Pripada).filter(Pripada.prioritet == 1).group_by(Pripada.fakultet_idFakulteta)
        lista = []
        brojZapisa = 0
        for pri in pripadaju:
            lista.append(pri.fakultet.naziv)
        for pri in pripadajuDist:
            a = {
                 "naziv" : pri.fakultet.naziv,
                 "broj" : lista.count(pri.fakultet.naziv)
            }
            result["podaci"].append(a)
            brojZapisa += 1
            if brojZapisa >= 10:
                break
        result["status"] = True
        
        try:
            dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Dohvaćanje statistike - Fakulteti po prioritetima")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException, KeyError):
            baseSession.rollback()
            pass
        
    except (BaseException):
        pass
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('brojFakulteta').encode()).hexdigest(), methods=['GET'])
#84a1cb4ff816e12c4dc33d86d99ecb865fbfdd79
def brojFakulteta(nijeServis = None):
    result = {
        "status" : False
    }
    try:
        brojFak = baseSession.query(Fakultet).count()
        if nijeServis != None:
            return brojFak
        else:
            result["status"] = True
            result["brojFakulteta"] = brojFak
    except (BaseException):
        pass
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
@app.route('/rest/'+hashlib.sha1(('brojUcenika').encode()).hexdigest(), methods=['GET'])
#c4d88c85bbe961284f05acbec0f8daf4b37a9b16
def brojUcenika(nijeServis = None):
    result = {
        "status" : False
    }
    try:
        brojUce = baseSession.query(Ucenik).count()
        if nijeServis != None:
            return brojUce
        else:
            result["status"] = True
            result["brojUcenika"] = brojUce
    except (BaseException):
        pass
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')