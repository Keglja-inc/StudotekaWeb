# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app, session, baseSession

from flask import request
from studoteka.dbKlase import Fakultet, Dnevnik

from flask import Response 
from sqlalchemy import and_
import json, hashlib
from studoteka.LoginSupport import login_required
from datetime import datetime

@app.route('/rest/'+hashlib.sha1(('prijavaFakulteta').encode()).hexdigest(), methods=['POST'])
#67785cd5c043ad00c8c5e6cf227274a37feed3eb
def restPrijava(mail=None, passw = None):
    ''' REST servis za prijavu fakulteta na sustav. Funkciju je moguće koristiti kao normalnu funkciju na
    webu proslijeđivanjem parametara email, lozinka ili pozivanjem pomoću POST requesta'''
    result = {
        "status" :  False,
        "message" : "Neuspjela prijava!"
    }
    if request.method == 'POST' or (mail != None and passw != None):
        if mail != None and passw != None:
            userEmail = mail
            userPass = passw
        else:
            data = request.get_json(force=True)
            userEmail = data['email']
            userPass = data['password']
        try:
            fakultet = baseSession.query(Fakultet).filter(and_(Fakultet.email==userEmail, Fakultet.blokiran==False, \
                Fakultet.aktiviran==True, Fakultet.lozinka == hashlib.sha512(userPass.encode()).hexdigest())).first()
            if fakultet != None:
                a = {"idFakulteta" : fakultet.idFakulteta, \
                    "naziv" : fakultet.naziv, \
                    "ulica" : fakultet.ulica, \
                    "kucniBroj" : fakultet.kucniBroj, \
                    "postanskiBroj" : fakultet.postanskiBroj, \
                    "mjesto" : fakultet.mjesto, \
                    "kontaktEmail" : fakultet.kontaktEmail, \
                    "kontaktTelefon" : fakultet.kontaktTelefon, \
                    "logo" : fakultet.logo, \
                    "webStranica" : fakultet.webStranica, \
                    "visokoUciliste" : fakultet.visokoUciliste_idVisokogUcilista, \
                    "email" : fakultet.email
                }
                session['user_data'] = dict(a)
                result['status'] = True
                result['message'] = "Uspješno ste se prijavili!"
                
                try:
                    dnevnik = Dnevnik(fakultet.idFakulteta, "Fakultet", "Prijava u sustav")
                    baseSession.add(dnevnik)
                    baseSession.commit()
                except (BaseException):
                    baseSession.rollback()
                    pass
                
        except (BaseException):
            pass
    if mail != None and passw != None: #Pozvano u web aplikaciji
        return json.dumps(result)
    else: #Pozvano preko rest servisa
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')

@app.route('/rest/'+hashlib.sha1(('odjavaFakulteta').encode()).hexdigest(), methods=['GET'])
#5be715931dfd371c7dc7f1e85064812f5d9bec71
def restOdjava():
    try:
        dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Odjava sa sustava")
        baseSession.add(dnevnik)
        baseSession.commit()
    except (BaseException, KeyError):
        baseSession.rollback()
        pass
    session.pop('user_data', None)
    result = {
        "status" :  True,
        "message" : "Uspješno ste odjavljeni!"
    }
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


#Provjera dostupnosti emaila za fakultete
@app.route('/rest/'+hashlib.sha1(('checkMail').encode()).hexdigest()+'/<email>')
#723c8440eafbb47ee3c06a451838a7ce2b258b0e
def provjeriDostupnostEmaila(email, odg = True):
    ''' Funkcija provjerava dostupnost email adrese, vraća True ako je slobodna, odnosno
        False ako nije slobodna'''
    result = {
        'status' : True,
        'message' : "Upisana email adresa je slobodna."
    }
    try:
        fak = baseSession.query(Fakultet).filter(Fakultet.email == email).first()
        if fak != None and fak.aktiviran == True:
            result['status'] = False
            result['message'] = "Upisana email adresa je zauzeta!"
    except (BaseException):
        pass
    if odg: #Poziv sa rest servisa
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        
    else: #Poziv iz aplikacije
        return json.dumps(result)

#Aktivacija emaila za fakultete
@app.route('/rest/'+hashlib.sha1(('aktivirajMail').encode()).hexdigest()+'/<kod>')
#9f5a0e9de8ed801c983bf3019ca40c54f08b4a03
def aktivirajMail(kod, odg = True):
    ''' Funkcija aktivira korisnički profil pomoću adrese elektroničke pošte'''
    result = {
        'status' : False,
        'message' : "Pogreška kod aktivacije!"
    }
    try:
        fak = baseSession.query(Fakultet).filter(Fakultet.aktivacijskiKod == kod).first()
        if fak != None:
            fak.aktiviran = True
            baseSession.add(fak)
            baseSession.commit()

            result['status'] = True
            result['message'] = "Korisnički profil je uspješno aktiviran!"
    except (BaseException):
        baseSession.rollback()
    if odg:
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    else:
        return json.dumps(result)
      
    