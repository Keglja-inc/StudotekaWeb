# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app, baseSession, session
from flask import Response, request
from studoteka.dbKlase import Interes, PonudaInteresa, Fakultet, Dnevnik
import json, hashlib
import datetime
from studoteka.LoginSupport import login_required, potrebnaPrijava


@app.route('/rest/'+hashlib.sha1(('popisInteresa').encode()).hexdigest(), methods=["GET"])
#13275cf47a74867fa3d5c02d7719e1ff28e011ba
def popisInteresa():
    '''
    Metoda ne prima parametre, a vraća sve interese iz baze podataka. Korisnik ne mora biti prijavljen za poziv. 
    '''
    result = {
        'status' : False,
        'vrijeme' : str(datetime.datetime.now()),
        'brojZapisa' : 0,
        'podaci' : []
    }
    try:
        listaInteresa = baseSession.query(Interes).order_by(Interes.idInteresa)
        for interes in listaInteresa:
            a = {'idInteresa' : interes.idInteresa,
                'naziv' : interes.naziv
            }
            result['podaci'].append(a)
        result['brojZapisa'] = len(result["podaci"])
        result["status"] = True
    except (BaseException):
        pass
        
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('popisInteresaZaOdabrati').encode()).hexdigest(), methods=['GET'])
#2e909d26d5ec066ebb42a3eb6389c1411f3b5d74
@potrebnaPrijava
def popisInteresaZaOdabrati():
    '''
    Metoda ne prima parametre. Vraća popis interesa koji fakultet može odabrati, tj. one koje nema odabrane.
    Korisnik MORA biti prijavljen za poziv.
    '''
    result = {
        'status' : False,
        'vrijeme' : str(datetime.datetime.now()),
        'brojZapisa' : 0,
        'podaci' : []
    }
    try:
        listaInteresa = baseSession.query(Interes).all()
        faks = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == session["user_data"]["idFakulteta"]).first()
        # Ovo je improvizirani način jer ovaj upit iz nekog razloga ne radi
        #listaInteresa = baseSession.query(Interes).filter(Interes.fakulteti.any(Fakultet.idFakulteta != session["user_data"]["idFakulteta"])).order_by(Interes.idInteresa)
        for i in listaInteresa:
            if faks not in i.fakulteti:
                a = {
                     "idInteresa" : i.idInteresa,
                     "naziv" : i.naziv
                }
                result["podaci"].append(a)

        result["brojZapisa"] = len(result["podaci"])
        result["status"] = True
        
        try:
            dnevnik = Dnevnik(faks.idFakulteta, "Fakultet", "Dohvaćanje interesa za odabrati")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException):
            baseSession.rollback()
            pass
        
    except (BaseException):
        pass
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')

@app.route('/rest/'+hashlib.sha1(('popisOdabranihInteresa').encode()).hexdigest(), methods=['GET'])
#caaf0ca037e2e3264afbafdfc3c69b95c878dac6
@potrebnaPrijava
def popisOdabranihInteresa():
    '''
    Metoda ne prima parametre, a vraća popis odabranih interesa za prijavljeni fakultet.
    Korisnik MORA biti prijavljen za poziv.
    '''
    result = {
        "status" : False,
        'vrijeme' : str(datetime.datetime.now()),
        'brojZapisa' : 0,
        'podaci' : []
    }
    try:
        faks = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == session["user_data"]["idFakulteta"]).first()
        for i in faks.interesi:
            a = {
                 "idInteresa" : i.idInteresa,
                 "naziv" : i.naziv
            }
            result["podaci"].append(a)
        result["brojZapisa"] = len(result["podaci"])
        result["status"] = True  
        
        try:
            dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Popis odabranih interesa")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException, KeyError):
            baseSession.rollback()
            pass
           
    except (BaseException):
        pass
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('kreirajInteres').encode()).hexdigest(), methods=['POST'])
#316f625b9e0dce032a49e3385cd4cfa1f1a7787a
@potrebnaPrijava
def kreirajInteres(nazivInteresa = None):
    '''
    Metoda za kreiranje interesa. Metoda prima podatke putem POST metode, predajom JSON-a oblika
    {"naziv": "ime interesa"} ukoliko joj nije proslijeđen parametar. Ukoliko se proslijedi parametar
    kreira se interes imena proslijeđenog u parametru.
    @param nazivInteresa: string
    Korisnik MORA biti prijavljen za poziv.
    '''
    result = {
        'status' : False,
        'message' : "Općenita greška"
    }
    
    try:
        if (nazivInteresa == None):
            data = request.get_json(force=True)
            nazivInteresa = data["naziv"]
    except KeyError:
        result["message"] = "Neispravan JSON"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        
    try:
        faks = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == session["user_data"]["idFakulteta"]).first()
        interes = baseSession.query(Interes).filter(Interes.naziv == nazivInteresa).first()
        
        if interes == None:
            baseSession.add(Interes(nazivInteresa))
            baseSession.commit()
        else:
            result["message"] = "Interes već postoji: "+interes.naziv
            return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        
        interes = baseSession.query(Interes).filter(Interes.naziv == nazivInteresa).first()
        pi = PonudaInteresa()
        pi.fakultet = faks
        pi.interes = interes
        
        baseSession.add(pi)
        baseSession.commit()
        
        result["status"] = True
        result["message"] = "Podatak je uspješno dodan."
        
        try:
            dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Kreiranje interesa")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException, KeyError):
            baseSession.rollback()
            pass
        
    except (BaseException):
        baseSession.rollback()
        
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')

@app.route('/rest/'+hashlib.sha1(('obrisiInteres').encode()).hexdigest(), methods=['POST'])
#2ec62787fcf982c59b9479aebb41837ea9049008
@potrebnaPrijava
def obrisiInteres(idInteresa=None):
    '''
    Metoda prihvaća HTTP metodu post u kojoj putem JOSN objekta šalje ID interesa koji se želi izbrisati iz baze.
    uobliku JSON objekta jednostavan i sadrži samo ID interesa
    {
        "idInteresa" : int
    }
    Moguće je proslijediti i parametar ID interesa
    @param idInteresa: int
    Korisnik MORA biti prijavljen za poziv.
    '''
    result = {
        'status' : False,
        'message' : "Općenita greška"
    }
    
    try:
        if (idInteresa == None):
            data = request.get_json(force=True)
            idInteresa = data["idInteresa"]
    except KeyError:
        result["message"] = "Neispravan JSON"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        baseSession.query(Interes).filter(Interes.idInteresa == idInteresa).first().delete()
        baseSession.commit()
        result["message"] = "Zapis je uspješno obrisan."
        
        try:
            dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Brisanje interesa")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException, KeyError):
            baseSession.rollback()
            pass
        
    except (BaseException):
        baseSession.rollback()
        result["message"] = "Greška kod brisanja zapisa."
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('dodajInteres').encode()).hexdigest(), methods=['POST'])
#052913f65b5b31417c4ca8740ea799cea8b1417b
@potrebnaPrijava
def dodajInteres (listaId = None):
    '''
    Metoda dodaje listu interesa za pojedini fakultet. Ignoriraju se interesi koji već postoje.
    Metoda prima listu ID-a preko parametra
    @param listaId: [int, int, ..., int]
    Ukoliko parametar nije proslijeđen, metoda preuzima podatke iz POST requesta, iz JSON objekta strukture
    {"idLista":[int, int, ..., int]} 
    Korisnik MORA biti prijavljen za poziv.
    '''
    result = {
        'status' : False,
        'message' : "",
        'podaci' : []
    }
    
    try:
        if listaId == None:
            data = request.get_json(force=True)
            listaId = data["idLista"]
    except KeyError:
        result["message"] = "Neispravan JSON"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        idFaksa = session["user_data"]["idFakulteta"]
        faks = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == idFaksa).first()
        listaInteresa = baseSession.query(Interes).filter(Interes.idInteresa.in_(listaId)) #svi interesi prema zadanim ID
        
        for interes in listaInteresa:
            if interes not in faks.interesi:
                faks.interesi.append(interes)
                result["podaci"].append(interes.naziv)
        baseSession.add(faks)
        baseSession.commit()
        result["status"] = True
        result["message"] = "Interesi su uspješno dodani."
        
        try:
            dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Odabir interesa")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException, KeyError):
            baseSession.rollback()
            pass
        
    except (BaseException, KeyError):
        baseSession.rollback()
        result["message"] = "Pogreška kod dodavanja interesa!"
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('ukloniInteres').encode()).hexdigest(), methods=['POST'])
#7339216846bf1e056325acc6e97f4540bd8698c5
@potrebnaPrijava
def ukloniInteres(listaId = None):
    '''Metoda ukladnja interes s popisa odabranih interesa za prijavljenog korisnika. Metoda također prima parametre
    @param listaId: [int, int, ..., int] 
    kao i listu ID interesa u obliku JSON objekta preko POST metode
    JSON izgleda ovako
    Izgled J
    {
        "idInteresa" : [int, int, ..., int]
    }
    Korisnik MORA biti prijavljen za poziv.
    '''
    result = {
        'status' : False,
        'message' : "Općenita greška"
    }
    try:
        if listaId == None:
            data = request.get_json(force=True)
            listaId = data["idLista"]
    except KeyError:
        result["message"] = "Neispravan JSON"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        idFaksa = session["user_data"]["idFakulteta"]
        faks = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == idFaksa).first()
        listaInteresa = baseSession.query(Interes).filter(Interes.idInteresa.in_(listaId))
        
        for interes in listaInteresa:
            if interes in faks.interesi:
                faks.interesi.remove(interes)
        baseSession.add(faks)
        baseSession.commit()
        result["status"] = True
        result["message"] = "Interesi su uspješno uklonjeni."
        
        try:
            dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Uklanjanje interesa")
            baseSession.add(dnevnik)
            baseSession.commit()
        except (BaseException, KeyError):
            baseSession.rollback()
            pass
        
    except (BaseException, KeyError):
        baseSession.rollback()
        result["message"] = "Greška kod uklanjanja interesa."
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')