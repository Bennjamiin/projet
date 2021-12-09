#!/bin/env python3 
import os
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from pdfminer.high_level import extract_text
from requests_html import HTMLSession
from urllib.parse import urljoin
import pathlib
from wordcloud import WordCloud
import fitz
import io
from PIL import Image
import PyPDF2
import shutil



class Ressource():
    def __init__(self,url):
        self.url = url
        self.type=self.setType(url)
        self.request = requests.get(self.url)

 

    def setType(self,url):                     ########OK
        r = requests.get(url)
        content_type = r.headers.get('content-type')
        
        if 'application/pdf' in content_type:
            ext = 'PDF'
            namePDF = url.split("/")
            namePDF = namePDF[2]
            with open(namePDF+'.pdf', 'wb') as f:
                f.write(r.content)
            
        elif 'text/html' in content_type:
            ext = 'HTML'
            
        else:
            ext = ''
            print('Unknown type: {}'.format(content_type))

        return ext


    def text(self):
        if os.path.exists('Cloud'):
            shutil.rmtree('Cloud')        
        pathlib.Path('Cloud').mkdir(parents=False, exist_ok=True) #Création du fichier image, ou l'on va stocker les nuages de mots

        if self.type == 'HTML':       ###### OK
            r = requests.get(self.url)
            raw_html = r.text
            html_page = BeautifulSoup(raw_html, features="html.parser")
            for s in html_page.select('script'):
                s.extract()
            for s in html_page.select('style'):
                s.extract()
            return html_page.get_text()

        elif self.type == 'PDF':               ####### OK
            pdf = BytesIO(self.request.content)
            self.texte=extract_text(pdf)
            return self.texte

    def image(self):
        if not os.path.exists('image'):
            os.makedirs('image')
        if os.path.exists('image\PDF'):
            shutil.rmtree('image\PDF')
        if not os.path.exists('image\PDF'):
            os.makedirs('image\PDF')
        if os.path.exists('image\HTML'):
            shutil.rmtree('image\HTML')
        if not os.path.exists('image\HTML'):
            os.makedirs('image\HTML')        

        if self.type == "HTML" :            ######OK
            self.img_urls = []
            session = HTMLSession()
            r = session.get(self.url)
            soup = BeautifulSoup(r.html.html, "html.parser")
            for img in soup.find_all("img"):
                img_url = img.attrs.get("src") or img.attrs.get("data-src") or img.attrs.get("data-original")
                if not img_url:
                    continue
                img_url = urljoin(self.url, img_url)
                try:
                    pos = img_url.index("?")
                    img_url = img_url[:pos]
                except ValueError:
                    pass
                self.img_urls.append(img_url)
            session.close()
            return self.img_urls


        if self.type == "PDF":                         
            if not os.path.exists('Docs_pdf'):
                os.makedirs('Docs_pdf')
            self.img_urls = ['PDF']
            path = os.getcwd() #obtient le chemin du fichier
            file_path = os.path.join(path,os.path.basename(self.url))  #Fichier ou l'on va telecharge le pdf tout en conservant son nom
            self.nom = os.path.basename(self.url) #on conserve le nom du PDF telechargé
            with open(file_path, 'wb') as f:  #telecharge le fichier pdf
                f.write(self.request.content)
            doc = fitz.open(self.nom)
            for pages in range(len(doc)):  #On récupère toutes les images dans le dossier image/PDF
                page = doc[pages]
                for imageindex, img in enumerate(page.getImageList(),start = 1):
                    xref = img[0]
                    baseimage = doc.extractImage(xref)
                    ib = baseimage["image"]
                    image = Image.open(io.BytesIO(ib))
                    image.save(open(f"image/PDF/image{pages+1}_{imageindex}.png", "wb"))
            return self.img_urls  #Renvoie ['PDF'] qui sera utile pour le traitement des images du PDF par la suite
                