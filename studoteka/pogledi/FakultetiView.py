# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app, baseSession, session, forme

from flask import redirect, render_template, flash, url_for, Response, request
import json, hashlib
from studoteka.servisi import Fakulteti
from studoteka.forme import LoginForm, RegistrationForm
from studoteka.LoginSupport import login_required
from studoteka.dbKlase import VisokoUciliste, Fakultet, Poruka, Dnevnik
from flask_mail import Mail, Message

@app.route('/login', methods=['GET' ,'POST'])
def prijava():
    form = LoginForm(csrf_enabled = True)

    if request.method == 'POST':
        form.email = request.form['email']
        form.password = request.form['password']
        form.validate()

        if form.email == 'admin' and form.password == 'admin':
            session['user_data'] = {"email" : "admin"}
            return redirect('/admin')
        try:
            res = json.loads(Fakulteti.restPrijava(form.email, form.password))
            if res['status'] == True:
                return redirect('/app')
            else:
                flash('Neuspješna prijava! Pogrešan email ili lozinka ili korisnik ne postoji!')
        except ValueError:
            flash(('Neuspješna prijava! Pogrešan email ili lozinka ili korisnik ne postoji!').encode('utf-8'))
    return render_template('login.html', form = LoginForm(csrf_enabled = True))

@app.route("/logout")    
def odjava():
    Fakulteti.restOdjava()
    return redirect(url_for('index'))

@app.route('/profil', methods=['GET', 'POST'])
@login_required
def dohvatiProfil():
    listaUcilista = []
    for instance in baseSession.query(VisokoUciliste).order_by(VisokoUciliste.idVisokogUcilista):
        a = {"idVisokogUcilista" : instance.idVisokogUcilista, \
            "naziv" : instance.naziv
        }
        listaUcilista.append(a)
    return render_template('profil.html', popis=listaUcilista )


@app.route("/azurirajProfil", methods=['POST'])
@login_required
def azurirajProfil():
    result = {
        "status":"GREŠKA",
        "message" : "Pogreška kod ažuriranja podataka!"
    }
    azuriraj = False
    if (request.method == 'POST'):
        try:
            fak = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == session['user_data']['idFakulteta']).first()

            if session['user_data']['naziv'] != request.form['id_naziv']:
                fak.naziv = request.form['id_naziv']
                azuriraj = True
            if session['user_data']['ulica'] != request.form['id_ulica']:
                fak.ulica = request.form['id_ulica']
                azuriraj = True
            if session['user_data']['kucniBroj'] != request.form['id_kucniBroj']:
                fak.kucniBroj = request.form['id_kucniBroj']
                azuriraj = True
            if session['user_data']['mjesto'] != request.form['id_mjesto']:
                fak.mjesto = request.form['id_mjesto']
                azuriraj = True
            if session['user_data']['postanskiBroj'] != request.form['id_postanskiBroj']:
                fak.postanskiBroj = request.form['id_postanskiBroj']
                azuriraj = True
            if session['user_data']['kontaktEmail'] != request.form['id_kontaktEmail']:
                fak.kontaktEmail = request.form['id_kontaktEmail']
                azuriraj = True
            if session['user_data']['kontaktTelefon'] != request.form['id_kontaktTelefon']:
                fak.kontaktTelefon = request.form['id_kontaktTelefon']
                azuriraj = True
            if session['user_data']['webStranica'] != request.form['id_webStranica']:
                fak.webStranica = request.form['id_webStranica']
                azuriraj = True
            if session['user_data']['visokoUciliste'] != request.form['id_visokoUciliste']:
                fak.visokoUciliste_idVisokogUcilista = request.form['id_visokoUciliste']
                azuriraj = True
            if azuriraj:
                #fa.zadnjaIzmjena = datetime.datetime.now()
                baseSession.add(fak)
                baseSession.commit()
                #flash(("Podaci su uspješno ažurirani.").decode('utf-8'))
                
                fak = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == session['user_data']['idFakulteta']).first()
                a = {"idFakulteta" : fak.idFakulteta, \
                    "naziv" : fak.naziv, \
                    "ulica" : fak.ulica, \
                    "kucniBroj" : fak.kucniBroj, \
                    "postanskiBroj" : fak.postanskiBroj, \
                    "mjesto" : fak.mjesto, \
                    "kontaktEmail" : fak.kontaktEmail, \
                    "kontaktTelefon" : fak.kontaktTelefon, \
                    "logo" : fak.logo, \
                    "webStranica" : fak.webStranica, \
                    "visokoUciliste" : fak.visokoUciliste_idVisokogUcilista, \
                    "email" : fak.email
                }
                session.pop('user_data', None)
                session['user_data'] = dict(a)

                result["status"] = "OK"
                result["message"] = "Podaci su uspješno ažurirani."
                
                try:
                    dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Ažuriranje profila")
                    baseSession.add(dnevnik)
                    baseSession.commit()
                except (BaseException, KeyError):
                    baseSession.rollback()
                    pass
                
            else:
                result["status"] = "INFO"
                result["message"] = "Niste promjenili podatke."
        except ValueError as e:
            baseSession.rollback()
            result["message"] = "Korak ex."
            #flash(("Pogreška kod ažuriranja podataka!").decode('utf-8'))
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')

@app.route('/registracija', methods=['GET', 'POST'])
def registracija():
    form = RegistrationForm(csrf_enabled = True)
    if request.method == 'POST':
        res = json.loads(Fakulteti.provjeriDostupnostEmaila(request.form['email'], False))
        if res['status'] == True:
            try:
                aKod = hashlib.sha224((request.form['email']+"o/6sfasSASD!#54!)w").encode()).hexdigest()
                noviFakultet = Fakultet(email=request.form['email'], lozinka = hashlib.sha512((request.form['password']).encode()).hexdigest(), \
                     aktiviran = False, blokiran = False, aktivacijskiKod=aKod)
                baseSession.add(noviFakultet)
                mail = Mail()
                msg = Message()
                msg.sender = ('Keglja inc. - StuFacJoint', 'AiRPTim@gmail.com')
                msg.subject = "Dobrodošli na StuFacJoint"
                msg.recipients = [request.form['email']]
                msg.body = 'Poveznica za aktivaciju: ' + url_for('index', _external=True) + 'rest/9f5a0e9de8ed801c983bf3019ca40c54f08b4a03/' + aKod
                msg.html = '''
                    <html>
                        <head>
                            <title> Potvrda elektroničke pošte </title>
                        </head>
                        <body>
                            <h1> Dobrodošli na StuFacJoint </h1>
                            <p> Kako bi koristili usluge molimo Vas da potvrdite adresu elektroničke pošte. </p>
                            <p> Aktivaciju možete izvršiti klikom na <a href='%s'>AKTIVIRAJ StuFacJoint</a> </p>
                        </body>
                    </html>
                ''' % (url_for('index', _external=True) + 'rest/9f5a0e9de8ed801c983bf3019ca40c54f08b4a03/' + aKod)
                mail.send(msg)

                baseSession.commit()
                return redirect('/login')
            except ValueError:
                baseSession.rollback()
                flash(("Greška kod registracije!").decode('utf-8'))
        else:
            flash((res['message']).decode('utf-8'))
    return render_template('registracija.html', form = form)

    
@app.route('/promjena lozinke', methods=['GET'])
@login_required
def promjenaLozinke():
    forma = forme.PromjenaLozinke()
    return render_template('promjenaLozinke.html', form= forma)


@app.route('/promjeniLozinku', methods=["POST"])
#9f5a0e9de8ed801c983bf3019ca40c54f08b4a03
@login_required
def promjeniLozinku():
    result={
        "status" : False,
        "message" : "Neuspješna promjena lozinke!"
    }
    
    fakultet = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == session["user_data"]["idFakulteta"]).first()
    if fakultet != None:
        if fakultet.lozinka == hashlib.sha512((request.form['trenutnaLozinka']).encode()).hexdigest():
            fakultet.lozinka = hashlib.sha512((request.form['novaLozinka']).encode()).hexdigest()
            baseSession.add(fakultet)
            baseSession.commit()
            result["status"] = True
            result["message"] = "Lozinka uspješno promjenjena!"
            
            try:
                dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Promjena lozinke")
                baseSession.add(dnevnik)
                baseSession.commit()
            except (BaseException, KeyError):
                baseSession.rollback()
                pass
            
        else:
            result["message"] += " Pogrešna lozinka!"
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8') 


@app.route('/promjena e-maila', methods=['GET'])
@login_required
def promjenaEmaila():
    forma = forme.PromjenaEmaila()
    return render_template('promjenaEmaila.html', form= forma)
    
@app.route('/promjeniEmail', methods=['POST'])
@login_required
def promjeniEmail():
    result={
        "status" : False,
        "message" : "Neuspješna promjena emaila!"
    }
    
    fakultet = baseSession.query(Fakultet).filter(Fakultet.idFakulteta == session["user_data"]["idFakulteta"]).first()
    if fakultet != None:
        res = json.loads(Fakulteti.provjeriDostupnostEmaila(request.form['noviEmail'], False))
        if res["status"] == True:
            if fakultet.lozinka == hashlib.sha512((request.form['trenutnaLozinka']).encode()).hexdigest():
                fakultet.email = request.form['noviEmail']
                baseSession.add(fakultet)
                baseSession.commit()
                result["status"] = True
                result["message"] = "Email uspješno promjenjen!"
                
                try:
                    dnevnik = Dnevnik(session["user_data"]["idFakulteta"], "Fakultet", "Promjena emaila")
                    baseSession.add(dnevnik)
                    baseSession.commit()
                except (BaseException, KeyError):
                    baseSession.rollback()
                    pass
                
            else:
                result["message"] += " Pogrešna lozinka!"
        else:
            result["message"] += res["message"]
    return Response(json.dumps(result), mimetype='application/json; charset=UTF-8') 

@app.route('/pocetna', methods=['GET'])
def pocetna():
    try:
        poruke = baseSession.query(Poruka).order_by(Poruka.vrijeme.desc())
    except (BaseException):
        pass

    return render_template("objave.html", poruke = poruke)