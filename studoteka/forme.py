# -*- coding: utf-8 -*-
from wtforms import Form, BooleanField, TextField, PasswordField, validators
from flask_wtf import RecaptchaField

class RegistrationForm(Form):
    
    email = TextField('Email adresa', [
        validators.Required(),
        validators.Length(min=6, max=35),
        validators.EqualTo('repeated', message='Upisane email adrese nisu jednake!')
    ])
    repeated = TextField('Ponovljena email adresa', [
        validators.Required(),
        validators.Length(min=6, max=35)
    ])
    
    password = PasswordField('Lozinka', [
        validators.Required(),
        validators.Length(min=6),
        validators.EqualTo('confirm', message='Upisane lozinke nisu jednake!')
    ])
    confirm = PasswordField('Ponovljena lozinka', [
        validators.Required()
    ])

    recaptcha = RecaptchaField()

class LoginForm(Form):
    email = TextField('Email Adresa', [
        validators.Length(min=6, max=35)
    ])
    password = PasswordField('Lozinka', [
        validators.Required()
    ])
    recaptcha = RecaptchaField()

class Profil(Form):
    """Forma za uredivanje profila fakulteta"""
    naziv = TextField("Naziv")
    ulica = TextField("Ulica")
    kucniBroj = TextField("Kucni broj")
    postanskiBroj = TextField("Poštanski broj")
    mjesto = TextField("Mjesto")
    kontaktEmail = TextField("Kontakt email adresa")
    kontaktTelefon = TextField("Kontakt telefon")
    logo = TextField("Logo fakulteta")
    webStranica = TextField("Adresa web stranice")
    visokoUciliste = TextField("Visoko učilište")
        
class PromjenaLozinke(Form):
    """Froma za promjenu lozinke"""
    trenutnaLozinka = PasswordField("Trenutna lozinka",[
        validators.Required(),
        validators.length(min=6, max=30, message="Lozinka mora imati između 6 i 30 znakova")
    ])
    novaLozinka = PasswordField("Nova lozinka",[
        validators.Required(),
        validators.length(min=6, max=30, message="Lozinka mora imati između 6 i 30 znakova")
    ])
    ponovljenaLozinka = PasswordField("Ponovljena lozinka",[
        validators.Required(),
        validators.length(min=6, max=30, message="Lozinka mora imati između 6 i 30 znakova"),
        validators.equal_to(novaLozinka, message="Lozinke se ne podudaraju")
    ])

class PromjenaEmaila(Form):
    """Forma za promjenu emaila"""
    trenutnaLozinka = PasswordField("Trenutna lozinka",[
        validators.Required(),
        validators.length(min=6, max=30, message="Lozinka mora imati između 6 i 30 znakova")
    ])
    noviEmail = TextField("Novi email")