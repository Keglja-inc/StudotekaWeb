# -*- coding: utf-8 -*-
from flask import Flask, session, redirect, render_template
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap

from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker

#APP CONFIGURATION
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RTS"ds"sda"sadsa'
#Recaptcha
RECAPTCHA_PUBLIC_KEY = '6LdREQITAAAAABSU6avnFZwC1nql88kAEfAGp6iR'
RECAPTCHA_PRIVATE_KEY = '6LdREQITAAAAAGHV1nZZ1zZh7lDPs5v4uVUxVd98'

#Mail
mail_config = {
    'MAIL_SERVER' : 'smtp.gmail.com',
    'MAIL_PORT' : 465,
    'MAIL_USE_TLS' : False,
    'MAIL_USE_SSL' : True,
    'MAIL_USERNAME' : 'airptim@gmail.com',
    'MAIL_PASSWORD' : 'funkcionalnost4'
}

#DATAbaseSession
engine = create_engine('mysql://remoteuser:remotepass753@46.101.185.15/studotekadb?charset=utf8', echo = False)
Session = sessionmaker(bind=engine)
baseSession = Session();
# --------DATAbaseSession

login_manager = LoginManager()
app = Flask(__name__)
Bootstrap(app)
login_manager.init_app(app)
app.config.update(mail_config)
mail = Mail(app)
app.config.from_object(__name__)

from studoteka.pogledi import FakultetiView, AdminView, InteresiView, StatistikaView, TestView
from studoteka.servisi import Fakulteti, PodaciFakulteti, PodaciInteresi, Ucenici, Admin, PodaciUcenici, Statistika
from studoteka.LoginSupport import login_required

@app.route('/')
def index():
    if 'user_data' in session:
        return redirect('app')
    else:
        return redirect('login')


@app.route('/app')
def aplikacija():
    return render_template("navigacija.html")

