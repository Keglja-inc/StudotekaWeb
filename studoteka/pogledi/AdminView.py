# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app, baseSession
from studoteka.LoginSupport import admin_required
from flask import render_template
from flask.globals import request
from werkzeug.utils import redirect
from studoteka.dbKlase import Poruka
from _datetime import datetime

@app.route('/admin')
@admin_required
def admin():
    return render_template("admin_index.html")

@app.route('/adminFakulteti')
@admin_required
def adminFakulteti():
    return render_template("admin_fakulteti.html")

@app.route('/adminObavijesti', methods=["GET", "POST"])
@admin_required
def adminObavijesti():
    if request.method == "GET":
        return render_template("admin_objave.html")
    elif request.method == "POST":
        try:
            poruka = Poruka()
            poruka.naslov = request.form["naslov"]
            poruka.tekst = request.form["tekst"]
            poruka.vrijeme = datetime.now()
            baseSession.add(poruka)
            baseSession.commit()
            return render_template("admin_objave.html")
        except(BaseException):
            redirect("/adminObavijesti")
    else:
        redirect("/")

@app.route('/adminDnevnik', methods=["GET", "POST"])
@admin_required
def adminDnevnik():
    return render_template("admin_dnevnik.html")