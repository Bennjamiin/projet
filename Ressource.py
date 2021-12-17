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
from pathlib import Path



class Ressource():
    def __init__(self,url):
        self.url = url
        self.type=self.setType(url)
        self.request = requests.get(self.url)

 

    def setType(self,url):                    
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
        pathlib.Path('Cloud').mkdir(parents=False, exist_ok=True) 


        if self.type == 'HTML':       
            HTML = requests.get(self.url).text
            soup = BeautifulSoup(HTML, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            texte = soup.get_text()
            lines = (line.strip() for line in texte.splitlines())   
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            texte = ' '.join(chunk for chunk in chunks if chunk)
            texte = texte.split("'")
            texte = ' '.join(texte)
            return texte

        elif self.type == 'PDF':               
            PDF = BytesIO(self.request.content)
            return extract_text(PDF)

    def image(self,num_pag):
        if self.type == "HTML" :           
            self.img = []
            pathlib.Path('HTML') 
            session = HTMLSession()
            r = requests.get(self.url)                
            soup = BeautifulSoup(r.text, 'html.parser')
            images = soup.findAll('img')              
            count = 0
            if len(images) != 0:
                for i, image in enumerate(images):
                    try:
                        image_link = image["data-srcset"]
                    except:
                        try:
                            image_link = image["data-src"]
                        except:
                            try:
                                image_link = image["data-fallback-src"]
                            except:
                                try:
                                    image_link = image["src"]
                                except:
                                    pass
                    try:
                        filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', image_link)
                        if not filename:
                            continue
                        with open(filename.group(1), 'wb') as f:
                            if 'http' not in image_link:
                                image_link = f"{num_pag}_{count}".format(url, image_link)
                            r = requests.get(image_link).content
                    except:
                        pass
                    image_link=urljoin(self.url,image_link)
                    self.img.append(image_link)
                    session.close()
                    count+=1
                print("Images télécharger depuis le HTML :", count)
                return self.img


        if self.type == "PDF":    
            self.img = ['PDF']
            typ="PDF"
            path=os.getcwd()
            file_path = os.path.join(os.getcwd(),os.path.basename(self.url))
            titre = os.path.basename(self.url) 
            with open(file_path, 'wb') as f:  
                f.write(self.request.content)
            texte = fitz.open(titre)
            count=0
            for p in range(len(texte)):  
                for imageindex, img in enumerate(texte[p].getImageList(),start = 1):
                    image = Image.open(io.BytesIO(texte.extractImage(img[0])["image"]))
                    image.save(open(f"PDF/{typ}_{num_pag}_{count}.png", "wb"))
                    count+=1
            print("Images télécharger depuis le PDF :", count)
            return self.img
