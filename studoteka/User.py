# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, userId, naziv, active = True):
        self.id = userId
        self.naziv = naziv
        self.active = active

    def is_active(self):
        #check db if user is active
        return self.active
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True