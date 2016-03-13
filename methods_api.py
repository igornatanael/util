#coding: utf-8
from bs4 import BeautifulSoup
import sys, os
import glob
import re
if len(sys.argv) != 2:
    print 'usage: python parse_estilos.py estilos.html'
    sys.exit()


html = sys.argv[1]
soup = BeautifulSoup(open(html), "html.parser")
try:
    categ = soup.findAll("label")
    print categ[-1].get_text() + "\n"
    divs = soup.findAll("div", { "class" : "hp-api-specification hp-collapsible public hp-collapsed" })
    met = soup.findAll("span", {"class":"method hp-api-method"})
    uri = soup.findAll("span", {"class":"uri"})
    desc = soup.findAll("description")
    print re.sub(r"\s+", " ", desc[0].get_text()) + "\n \n"
    if len(uri) == len(met):
        for i in range(len(uri)):
            print met[i].get_text(), uri[i].get_text()+ "\n"
            print re.sub(r"\s+", " ", desc[i+1].get_text())+ "\n \n"
except Exception as e:
    print e, "exeption"

