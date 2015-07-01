# -*- coding: utf-8 -*-
'''
Created on 30. svi 2015.

@author: spicko
'''
from studoteka import app

from flask import render_template, request, Response
import urllib2, json
from pyquery import PyQuery
from lxml import etree, html
import requests, re

def dohvatiVijesti(self):
        page = requests.get('http://www.mojamatura.net/vijesti')
        tree = html.fromstring(page.text)

        naslovi = tree.xpath('//a[@class="PostHeader"]/text()')
        informacije = tree.xpath('//div[@class="art-PostHeaderIcons art-metadata-icons"]/text()')
        tekstovi = tree.xpath('//div[@class="art-article"]/text()')

        result = {
            "Status" : "OK",
            "Message" : "Podaci uspje�no dohva�eni",
            "Data" : []
        }

        d = PyQuery("<html></html>")
        d = PyQuery(etree.fromstring("<html></html>"))
        d = PyQuery(url='http://www.mojamatura.net/vijesti')
        d = PyQuery(url='http://www.mojamatura.net/vijesti', opener=lambda url: urllib2.urlopen(url).read())
        p = d("#art-main > div > div.art-Sheet-body > div > div > table").html()
        
        d1 = PyQuery(p)
        p1 = d1("div.art-Post-inner")

        for i in range(len(p1)):
            m = {}
            n = p1.eq(i).find("a.PostHeader").text()
            m["naslov"] = re.sub("<!--.*?-->", "", n)
            n = p1.eq(i).find("div.art-PostHeaderIcons art-metadata-icons").text()
            m["info"] = re.sub("<!--.*?-->", "", n)
            n = p1.eq(i).find("div.art-article").text()
            pattern = re.compile(r'<!--.*?-->')
            m["tekst"] = pattern.sub("", n)
            result["Data"].append(m)
        #p1 = p("div.PostHeader").html()
        
        # for i in range(len(naslovi)):
        #     v = {}
        #     v["naslov"] = naslovi[i]
        #     v["info"] = informacije[i]
        #     v["tekst"] = tekstovi[i]
        #     result["Data"].append(v)
        return Response(json.dumps(result), mimetype='application/json; charset=UTF-8')
        return str(result);
        return render_template('vijesti.html', sadrzaj=the_vijesti)