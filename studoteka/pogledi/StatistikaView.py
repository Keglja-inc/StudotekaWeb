# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app
from flask import render_template

@app.route('/statistika')
def statistika():
    return render_template('statistika.html')