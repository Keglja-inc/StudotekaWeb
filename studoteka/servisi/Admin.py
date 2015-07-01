# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app, baseSession
from flask import redirect, request, Response
import hashlib, json
from studoteka.dbKlase import Fakultet, VisokoUciliste, Dnevnik
from studoteka.LoginSupport import admin_required

@app.route('/vrati')
def vrati():
    baseSession.rollback()
    return redirect('/')

#Izračun sha1 za naziv rest funkcija -> MAKNUTI kod production!
@app.route('/naziv/<name>')
def naziv(name):
    ''' Funkcija za dohvaćanjanje imena REST poziva. Kod poziva proslijeđuje se naziv i
        vraća se vrijednost sažetka sa SHA1 algoritmom'''
    return hashlib.sha1(name.encode()).hexdigest()


#CRUD rest akcije za jTable widget
@app.route('/rest/'+hashlib.sha1(('listAction').encode()).hexdigest(), methods=['POST'])
#84002239b8bb525bad1cc689fee5569d98462307
@admin_required
def listAction():
    ''' Funkcija dohvaća sve fakultete koji su registrirani. Čisto za potrebe CRUD.'''
    result = {
        'Result' : "ERROR",
        'Message' : "Neuspješno dohvaćanje zapisa!",
        'Records' : []
    }
    
    try:
        pocetak = int(request.args.get("jtStartIndex"))
        velicinaStranice = int(request.args.get("jtPageSize"))
    except KeyError as e:
        result["Message"] = "Pogreška kod zahtjeva!"+str(e)
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    ukupniBroj = 0
    try:
        popisFakulteta = baseSession.query(Fakultet).order_by(Fakultet.idFakulteta)
        for instance in popisFakulteta:
            a = {"idFakulteta" : instance.idFakulteta, 
                "naziv" : instance.naziv, 
                "ulica" : instance.ulica, 
                "kucniBroj" : instance.kucniBroj, 
                "postanskiBroj" : instance.postanskiBroj, 
                "mjesto" : instance.mjesto, 
                "kontaktEmail" : instance.kontaktEmail, 
                "kontaktTelefon" : instance.kontaktTelefon, 
                "logo" : instance.logo, 
                "webStranica" : instance.webStranica, 
                "visokoUciliste" : instance.visokoUciliste_idVisokogUcilista, 
                "email" : instance.email, 
                "lozinka" : instance.lozinka
                }
            result['Records'].append(a)
            ukupniBroj += 1
        result['Result'] = "OK"
        result['Message'] = "Successfull."
        result["TotalRecordCount"] = ukupniBroj
    except (BaseException) as e:
        result['Message'] = str(e)
        
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('createAction').encode()).hexdigest(), methods=['POST'])
#5e358c3fa86341b6f7ebf1b5ac98c123bb34d38b
@admin_required
def createAction():
    ''' Funkcija dohvaća sve fakultete koji su registrirani. Čisto za potrebe CRUD.'''
    result = {
        'Result' : "ERROR",
        'Message' : "Neuspješno dodavanje zapisa!",
        'Record' : []
    }
    
    try:
        naziv = request.form["naziv"]
        ulica = request.form["ulica"]
        kucniBroj = request.form["kucniBroj"]
        postanskiBroj = request.form["postanskiBroj"]
        mjesto = request.form["mjesto"]
        kontaktEmail = request.form["kontaktEmail"]
        kontaktTelefon = request.form["kontaktTelefon"]
        logo = request.form["logo"]
        webStranica = request.form["webStranica"]
        visokoUciliste = request.form["visokoUciliste"]
        email = request.form["email"]
        lozinka = request.form["lozinka"]
    except (KeyError, TypeError):
        result["Message"] = "Pogrešni podaci!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')

    try:
        fakultet = baseSession.query(Fakultet).filter(Fakultet.email == email).first()
        visokoUciliste = baseSession.query(VisokoUciliste).filter(VisokoUciliste.idVisokogUcilista == visokoUciliste).first()
        if fakultet == None:
            fakultet = Fakultet()
            fakultet.naziv = naziv
            fakultet.ulica = ulica
            fakultet.kucniBroj = kucniBroj
            fakultet.postanskiBroj = postanskiBroj
            fakultet.mjesto = mjesto
            fakultet.kontaktEmail = kontaktEmail
            fakultet.kontaktTelefon = kontaktTelefon
            fakultet.logo = logo
            fakultet.webStranica = webStranica
            fakultet.visokoUciliste = visokoUciliste
            fakultet.email = email
            fakultet.lozinka = hashlib.sha512(lozinka.encode()).hexdigest()
            baseSession.add(fakultet)
            baseSession.commit()
        else:
            result["Message"] = "Već postoji fakultet sa upisanom email adresom!"
            return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        
        dodaniFakultet = baseSession.query(Fakultet).filter(Fakultet.email == email).first()
        if dodaniFakultet == None:
            return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        else:
            a = {"idFakulteta" : dodaniFakultet.idFakulteta, 
                "naziv" : dodaniFakultet.naziv, 
                "ulica" : dodaniFakultet.ulica, 
                "kucniBroj" : dodaniFakultet.kucniBroj, 
                "postanskiBroj" : dodaniFakultet.postanskiBroj, 
                "mjesto" : dodaniFakultet.mjesto, 
                "kontaktEmail" : dodaniFakultet.kontaktEmail, 
                "kontaktTelefon" : dodaniFakultet.kontaktTelefon, 
                "logo" : dodaniFakultet.logo, 
                "webStranica" : dodaniFakultet.webStranica, 
                "visokoUciliste" : dodaniFakultet.visokoUciliste_idVisokogUcilista, 
                "email" : dodaniFakultet.email,
                "lozinka" : dodaniFakultet.lozinka
            }
            result['Record'].append(a)
            result['Result'] = "OK"
            result['Message'] = "Successfull."
    except (BaseException):
        result["Message"] = "Pogreška s bazom!"
        baseSession.rollback()
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('updateAction').encode()).hexdigest(), methods=['POST'])
#37cdf6db410abda9c72152491e9feccf6c3cf8db
@admin_required
def updateAction():
    ''' Funkcija dohvaća sve fakultete koji su registrirani. Čisto za potrebe CRUD.'''
    result = {
        'Result' : "ERROR",
        'Message' : "Neuspješno dodavanje zapisa!",
        'Record' : []
    }
    
    try:
        naziv = request.form["naziv"]
        ulica = request.form["ulica"]
        kucniBroj = request.form["kucniBroj"]
        postanskiBroj = request.form["postanskiBroj"]
        mjesto = request.form["mjesto"]
        kontaktEmail = request.form["kontaktEmail"]
        kontaktTelefon = request.form["kontaktTelefon"]
        logo = request.form["logo"]
        webStranica = request.form["webStranica"]
        visokoUciliste = request.form["visokoUciliste"]
        email = request.form["email"]
        lozinka = request.form["lozinka"]
    except (KeyError, TypeError):
        result["Message"] = "Pogrešni podaci!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')

    try:
        fakultet = baseSession.query(Fakultet).filter(Fakultet.email == email).first()
        visokoUciliste = baseSession.query(VisokoUciliste).filter(VisokoUciliste.idVisokogUcilista == visokoUciliste).first()
        if fakultet != None:
            fakultet.naziv = naziv
            fakultet.ulica = ulica
            fakultet.kucniBroj = kucniBroj
            fakultet.postanskiBroj = postanskiBroj
            fakultet.mjesto = mjesto
            fakultet.kontaktEmail = kontaktEmail
            fakultet.kontaktTelefon = kontaktTelefon
            fakultet.logo = logo
            fakultet.webStranica = webStranica
            fakultet.visokoUciliste = visokoUciliste
            fakultet.email = email
            fakultet.lozinka = hashlib.sha512(lozinka.encode()).hexdigest()
            baseSession.add(fakultet)
            baseSession.commit()
        else:
            result["Message"] = "Pogreška s ažuriranjem podataka za fakultet!"
            return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        
        azuriraniFakultet = baseSession.query(Fakultet).filter(Fakultet.email == email).first()
        if azuriraniFakultet == None:
            return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        else:
            a = {"idFakulteta" : azuriraniFakultet.idFakulteta, 
                "naziv" : azuriraniFakultet.naziv, 
                "ulica" : azuriraniFakultet.ulica, 
                "kucniBroj" : azuriraniFakultet.kucniBroj, 
                "postanskiBroj" : azuriraniFakultet.postanskiBroj, 
                "mjesto" : azuriraniFakultet.mjesto, 
                "kontaktEmail" : azuriraniFakultet.kontaktEmail, 
                "kontaktTelefon" : azuriraniFakultet.kontaktTelefon, 
                "logo" : azuriraniFakultet.logo, 
                "webStranica" : azuriraniFakultet.webStranica, 
                "visokoUciliste" : azuriraniFakultet.visokoUciliste_idVisokogUcilista, 
                "email" : azuriraniFakultet.email,
                "lozinka" : azuriraniFakultet.lozinka
            }
            result['Record'].append(a)
            result['Result'] = "OK"
            result['Message'] = "Successfull."
    except (BaseException):
        result["Message"] = "Pogreška s bazom!"
        baseSession.rollback()
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('deleteAction').encode()).hexdigest(), methods=['POST'])
#58978999b05a1b8ea86d2723aa717982c47ece21
@admin_required
def deleteAction():
    ''' Funkcija dohvaća sve fakultete koji su registrirani. Čisto za potrebe CRUD.'''
    result = {
        'Result' : "ERROR",
        'Message' : "Neuspješno brisanje zapisa!",
        'Record' : []
    }
    
    try:
        idFakulteta = request.form["idFakulteta"]
    except (KeyError, TypeError):
        result["Message"] = "Pogrešni podaci!"
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
    
    try:
        baseSession.query(Fakultet).filter(Fakultet.idFakulteta == idFakulteta).delete()
        baseSession.commit()
        result["Result"] = "OK"
        result["Message"] = "Zapis uspješno obrisan."
    except (BaseException) :
        baseSession.rollback()
        result["Message"] = "Pogreška s bazom!"
    
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')


@app.route('/rest/'+hashlib.sha1(('dohvatiDnevnik').encode()).hexdigest(), methods=["GET",'POST'])
#9786583ec82eaf5bac6d070e104a6661a45033a1
@admin_required
def dohvatiDnevnik():
    ''' Funkcija dohvaća sve zapise u dnevniku'''
    try:
        dnevnik = baseSession.query(Dnevnik).order_by(Dnevnik.vrijeme.desc()).all()
        broj = baseSession.query(Dnevnik).count()
    except (BaseException):
        pass
    
    result = {
        'draw' : 1,
        'recordsTotal' : broj,
        'data' : []
    }
    for zapis in dnevnik:
        a = {
             "idZapisa" : zapis.idZapisa,
             "idLogiranogKorisnika" : zapis.idLogiranogKorisnika,
             "tipLogiranogKorisnika" : zapis.tipLogiranogKorisnika,
             "vrijeme" : zapis.vrijeme.isoformat(),
             "akcija" : zapis.akcija
        }
        result["data"].append(a)
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')