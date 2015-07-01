# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app, baseSession
from flask import request, Response
from sqlalchemy import and_
from studoteka.dbKlase import Ucenik, Dnevnik
import json, hashlib


#REST ZA UČENIKE -> REGISTRACIJA I PRIJAVA
@app.route('/rest/' + hashlib.sha1(('restRegistracijaUcenika').encode()).hexdigest(), methods=['POST'])
#0e3a5ba1f993b60805694759ba4b882afef53281
def restRegistracijaUcenika():
    result = {
        'status' : False,
        'message' : "Neuspješna registracija!"
    }
    #if request.method == 'POST':
    data = request.get_json(force=True)
    try:
        email = data["email"]
        lozinka = data["lozinka"]
        ime = data["ime"]
        prezime = data["prezime"]
    except KeyError:
        result["message"] = "Pogrešni podaci!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8') 
       
    try:
        ucenik = baseSession.query(Ucenik).filter(Ucenik.email == email).first()
        if ucenik == None:
            noviUcenik = Ucenik()
            noviUcenik.email = email
            noviUcenik.lozinka = lozinka
            noviUcenik.ime = ime
            noviUcenik.prezime = prezime
            baseSession.add(noviUcenik)
            baseSession.commit()
            result['status'] = True
            result['message'] = "Uspješno ste se registrirali."
        else:
            result['message'] = "Upisana email adresa je zauzeta!"
    except (BaseException, KeyError):
        result["message"] = "Pogreška s bazom!"
        baseSession.rollback()
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


#Prijava učenika
@app.route('/rest/'+hashlib.sha1(('restPrijavaUcenika').encode()).hexdigest(), methods=['POST'])
#3982bb6a86fec50fd20ee0c3cd6ff474f4ceb78e
def restPrijavaUcenika():
    ''' REST servis za prijavu ucenika na sustav.'''
    result = {
        "status" :  False,
        "message" : "Neuspjesna prijava!"
    }
    data = request.get_json(force=True)
    
    try:
        email = data["email"]
        lozinka = data["lozinka"]
    except KeyError:
        result["message"] = "Pogrešni podaci!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        ucenik = baseSession.query(Ucenik).filter(and_(Ucenik.email == email, Ucenik.lozinka == lozinka)).first()
        if ucenik != None:
            a = {"idUcenika" : ucenik.idUcenika, \
                "ime" : ucenik.ime, \
                "prezime" : ucenik.prezime, \
                "email" : ucenik.email
            }
            result['status'] = True
            result['message'] = "Uspjesno ste se prijavili."
            result['podaci'] = a
            
            try:
                dnevnik = Dnevnik(ucenik.idUcenika, "Ucenik", "Prijava u sustav")
                baseSession.add(dnevnik)
                baseSession.commit()
            except (BaseException):
                baseSession.rollback()
                pass
    except (BaseException, KeyError):
        result["message"] = "Pogreška s bazom!"
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')

@app.route('/rest/' + hashlib.sha1(('restAzuriranjeProfilaUcenika').encode()).hexdigest(), methods=['POST'])
#dea967a98088c17395a09180ffb441c9e935f2ce
def restAzuriranjeProfilaUcenika():
    result = {
        'status' : False,
        'message' : "Neuspješno ažuriranje profila!"
    }
    
    try:
        data = request.get_json(force=True)
        idUcenika = data["idUcenika"]
        ime = data["ime"]
        prezime = data["prezime"]
        email = data["email"]
        lozinka = data["lozinka"]
        ponovljenaLozinka = data["ponovljenaLozinka"]
        
        if lozinka != ponovljenaLozinka:
            result["message"] = "Lozinke se ne podudaraju!"
            return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    except KeyError:
        result["message"] = "Pogrešan JSON!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        ucenik = baseSession.query(Ucenik).filter(Ucenik.idUcenika == idUcenika).first()
        if ucenik != None:
            azuriraj = False
            if ucenik.ime != ime:
                ucenik.ime = ime
                azuriraj = True
            if ucenik.prezime != prezime:
                ucenik.prezime = prezime
                azuriraj = True
            if ucenik.email != email:
                tempUcenik = baseSession.query(Ucenik).filter(Ucenik.email == email).first()
                if tempUcenik == None:
                    ucenik.email = email
                    azuriraj = True
                else:
                    result["message"] = "Email adresa je zauzeta"
                    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
            if ucenik.lozinka != lozinka:
                ucenik.lozinka = lozinka
                azuriraj = True
            if azuriraj == True:
                baseSession.add(ucenik)
                baseSession.commit()
                result["status"] = True
                result["message"] = "Uspješno ste ažurirali profil."
                
                try:
                    dnevnik = Dnevnik(idUcenika, "Ucenik", "Azuriranje profila")
                    baseSession.add(dnevnik)
                    baseSession.commit()
                except (BaseException):
                    baseSession.rollback()
                    pass
        else:
            result["message"] = "Nepostojeći učenik!"
    except (BaseException):
        baseSession.rollback()
        result["message"] = "Pogreška s bazom!"
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')