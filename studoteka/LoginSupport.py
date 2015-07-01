# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import session
from flask import flash, redirect, Response
from functools import wraps
import json

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'user_data' in session:
            return test(*args, **kwargs)
        else:
            flash (('Trebate se prijaviti u sustav.').encode().decode('utf-8'))
            return redirect('/login')
    return wrap

def potrebnaPrijava(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'user_data' in session:
            return test(*args, **kwargs)
        else:
            result = {
                "status" : False,
                "message" : "Resurs je dostupan samo za prijavljene korisnike"
            }
            return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
            
    return wrap

def admin_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'user_data' in session:
            if session["user_data"]["email"] == "admin":
                return test(*args, **kwargs)
        else:
            flash (('Trebate se prijaviti u sustav.').encode().decode('utf-8'))
            return redirect('/login')
    return wrap