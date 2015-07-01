# -*- coding: utf8 -*-
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, DateTime, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from datetime import datetime


Base = declarative_base()

class Fakultet(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'fakultet'

	#	Schema
	idFakulteta = Column("idFakulteta", Integer, primary_key = True)
	naziv = Column("naziv", String(70))
	ulica = Column("ulica", String(50))
	kucniBroj = Column("kucniBroj", String(5))
	postanskiBroj = Column("postanskiBroj", Integer)
	mjesto = Column("mjesto", String(50))
	kontaktEmail = Column("kontaktEmail", String(50))
	kontaktTelefon = Column("kontaktTelefon", String(15))
	logo = Column("logo", String(100))
	webStranica = Column("webStranica", String(30))
	visokoUciliste_idVisokogUcilista = Column("visokoUciliste_idVisokogUcilista", Integer, ForeignKey('visokoUciliste.idVisokogUcilista'))
	email = Column("email", String(50))
	lozinka = Column("lozinka", String(256))
	aktiviran = Column("aktiviran", Boolean)
	blokiran = Column("blokiran", Boolean)
	aktivacijskiKod = Column("aktivacijskiKod", String(256))
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)
	
	#	Relations
	interesi = relationship("Interes", secondary="ponuda_interesa", backref = backref("fakulteti"))
	visokoUciliste = relationship("VisokoUciliste", backref = backref("fakulteti"))

class Ucenik(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'ucenik'

	#	Schema
	idUcenika = Column("idUcenika", Integer, primary_key = True)
	ime = Column("ime", String(20))
	prezime = Column("prezime", String(30))
	email = Column ("email", String(50))
	lozinka = Column("lozinka", String(256)) #-> sha512 ima 128
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)
	
	#	Relations
	interesi = relationship("Interes", secondary="je_zainteresiran", backref = backref("ucenici"))
	predlozeniFakulteti = relationship("Fakultet", secondary="pripada", backref=backref("potencijalniStudenti"))

class Interes(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'interes'

	#	Schema
	idInteresa = Column("idInteresa", Integer, primary_key=True)
	naziv = Column("naziv", String(30, collation='utf8'))
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)
	
	#	Relations
	
	
	#	Methods
	def __init__(self, naziv):
		self.idInteresa = id
		self.naziv = naziv
		self.zadnjaIzmjena = datetime.now()
	
	def ispisiPodatke(self):
		return "ID interesa: "+str(self.idInteresa)+"; Naziv: "+self.naziv+"; Zadnja izmjena: "+str(self.zadnjaIzmjena)
	

class TipVisokogUcilista(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'tipVisokogUcilista'
	
	#	Schema
	idtipVisokogUcilista = Column("idtipVisokogUcilista", Integer, primary_key=True)
	opis = Column("opis", String(45))
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)

	#	Relations
	visokaUcilista = relationship("VisokoUciliste", backref=backref("tipVisokogUcilista", cascade='all, delete-orphan', single_parent=True))

class StatusVisokogUcilista(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'statusVisokogUcilista'

	#	Schema
	idstatusVisokogUcilista = Column("idstatusVisokogUcilista", Integer, primary_key=True)
	opis = Column("opis", String(45))
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)

	#	Relations
	visokaUcilista = relationship("VisokoUciliste", backref=backref("statusVisokogUcilista", cascade='all, delete-orphan', single_parent=True))

class VisokoUciliste(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'visokoUciliste'
	
	#	Schema
	idVisokogUcilista = Column("idVisokogUcilista", Integer, primary_key=True)
	naziv = Column("naziv", String(80))
	tipVisokogUcilista_idtipVisokogUcilista = Column("tipVisokogUcilista_idtipVisokogUcilista", Integer, ForeignKey('tipVisokogUcilista.idtipVisokogUcilista'))
	statusVisokogUcilista_idstatusVisokogUcilista = Column("statusVisokogUcilista_idstatusVisokogUcilista", Integer, ForeignKey('statusVisokogUcilista.idstatusVisokogUcilista'))
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)
	
	#	Relations
	
	
	
class PonudaInteresa(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'ponuda_interesa'

	#	Schema
	fakultet_idFakulteta = Column("fakultet_idFakulteta", Integer, ForeignKey('fakultet.idFakulteta'), primary_key=True)
	interes_idInteresa = Column("interes_idInteresa", Integer, ForeignKey('interes.idInteresa'), primary_key=True)
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)
	
	#	Relations
	interes = relationship("Interes", backref=backref("ponudaInteresa", cascade='all, delete-orphan', single_parent=True))
	fakultet = relationship("Fakultet", backref=backref("ponudaInteresa", cascade='all, delete-orphan', single_parent=True))
	
	#	Metode
	
	

class JeZainteresiran(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'je_zainteresiran'

	#	Schema
	ucenik_idUcenika = Column("ucenik_idUcenika", Integer, ForeignKey('ucenik.idUcenika'), primary_key=True)
	interes_idInteresa = Column("interes_idInteresa", Integer, ForeignKey('interes.idInteresa'), primary_key=True)
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)
	
	#	Relations
	interes = relationship("Interes", backref=backref("jeZainteresiran", cascade='all, delete-orphan', single_parent=True))
	ucenik = relationship("Ucenik", backref=backref("jeZainteresiran", cascade='all, delete-orphan', single_parent=True))

	
class Pripada(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = 'pripada'

	#	Schema
	prioritet = Column("prioritet", Integer)
	postotak = Column("postotak", Float)
	brojHitova = Column("brojHitova", Integer)
	ucenik_idUcenika = Column("ucenik_idUcenika", Integer, ForeignKey('ucenik.idUcenika'), primary_key=True)
	fakultet_idFakulteta = Column ("fakultet_idFakulteta", Integer, ForeignKey('fakultet.idFakulteta'), primary_key=True)
	zadnjaIzmjena = Column("zadnjaIzmjena", TIMESTAMP)

	#	Realtions
	fakultet = relationship("Fakultet", backref=backref("pripada", cascade='all, delete-orphan', single_parent=True))
	ucenik = relationship("Ucenik", backref=backref("pripada", cascade='all, delete-orphan', single_parent=True))
	
class Poruka(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = "poruka"
	
	idPoruka = Column("idPoruka", Integer, primary_key=True)
	naslov = Column("naslov", String(45))
	tekst = Column("tekst", String(255))
	vrijeme = Column("vrijeme", DateTime)
	
class Dnevnik(Base):
	"""Klasa za rad sa bazom -> ORM"""
	__tablename__ = "dnevnik"
	
	idZapisa = Column("idZapisa", Integer, primary_key=True)
	vrijeme = Column("vrijeme", DateTime)
	idLogiranogKorisnika = Column("idLogiranogKorisnika", Integer)
	tipLogiranogKorisnika = Column("tipLogiranogKorisnika", String(10))
	akcija = Column("akcija", String(50))
	
	def __init__(self, korisnik, tip, akcija):
		self.vrijeme = datetime.now()
		self.idLogiranogKorisnika = korisnik
		self.tipLogiranogKorisnika = tip
		self.akcija = akcija