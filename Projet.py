#!/bin/env python3
import PyPDF2
import requests
from bs4 import BeautifulSoup

import re
import os
from abc import ABC, abstractmethod


import fitz   



class Prisme:
    def __init__(self,traitement):
        self.traitement = traitement
        self.aTraiter = list()
        self.un_traitement = self.traitement()
        self.run("listeURLS.txt")
        

    def run(self,fichier):
        with open(fichier, encoding ="utf_8_sig") as f:
            urls = list()
            for ligne in f :
                urls.append(ligne)
                
        une_collecte = Collecte(urls)
        une_collecte.run()
        self.aTraiter = une_collecte.content()
        self.un_traitement.aTraiter = self.aTraiter
        self.un_traitement.run()
      

    def show(self):
        self.un_traitement.show()




        

class Collecte:
    def __init__(self,listURL):
        self.liste=listURL
        self.contentsText=list()
        os.rmdir('images')
        os.mkdir('images')


    def run(self):
        for url in self.liste :
            ressource = Ressource(url)
            self.contentsText.append(ressource.text)


    def content(self):
        return self.contentsText






class TraitementTrivial:
    def __init__(self):
        self.aTraiter = list()
        self.conclusion = 0
        
    
    def run(self):
        for text in self.aTraiter :
            r = text.split()
            self.conclusion += len(r)
            


    def show(self):
        print(self.conclusion)









class Ressource:
    def __init__(self,lien):
        self.lien = lien
        self.type = self.setType(lien)
        self.text = self.setText(lien)
        if self.type == 'pdf' :
            self.setImagesPdf(lien)
        elif self.type == 'html':
            self.setImagesHtml(lien)
        
        


    def setText(self,lien):
        
        texte = ""
        
        if (self.type == 'pdf'):
            namePDF = lien.split("/")
            namePDF = namePDF[2]
            pdfFileObject = open(namePDF+'.pdf', 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
            count = pdfReader.numPages
            for i in range(count):
                page = pdfReader.getPage(i)
                texte += page.extractText()


                              
        elif (self.type == 'html') :
            html = requests.get(lien).text
            soup = BeautifulSoup(html, features="html.parser")
            
            for script in soup(["script", "style"]):
                script.extract()
            texte = soup.get_text()
            
            #Epure le texte pour enlever les espace et les retours à la ligne
            lines = (line.strip() for line in texte.splitlines())   
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            texte = '\n'.join(chunk for chunk in chunks if chunk)

        return texte


    def setImagesHtml (self,url):

        r = requests.get(url)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        images = soup.findAll('img')

        count = 0
 
        if len(images) != 0:
            # On va chercher un lien dans les données récupérées
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

                                #on corrige les liens pour supprimer les "?...." à la suite des .jpg,.png ou .gif et on rajoute .jpg s'il n'y a pas .jpg,.png ou.gif                              
                                image_link = image_link.split("/")
                                surplus = image_link[-1]
                                surplus = surplus.split("?")
                                surplus = surplus[0].split(".")
                                if len(surplus) == 1 :
                                    surplus.append("jpg")
                                    surplus = ".".join(surplus)
                                    image_link[-1] = surplus[0]
                                else :
                                    surplus = ".".join(surplus)
                                image_link[-1] = surplus
                                liaison = "/"
                                image_link = liaison.join(image_link)
 
                            # si on de trouve pas de source URL
                            except:
                                pass
 
                try:
                    #On télécharge l'image grace au lien
                    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', image_link)
                    if not filename:
                        print("Regex didn't match with the url: {}".format(image_link))
                        continue
                    with open(filename.group(1), 'wb') as f:
                        if 'http' not in image_link:
                            image_link = '{}{}'.format(url, image_link)
                        r = requests.get(image_link).content
                        f.write(r)
                        
 
                    count += 1
                except:
                    pass
 
            '''if count == len(images):
                print("All Images Downloaded!")
             
            else:
                print(f"Total {count} Images Downloaded Out of {len(images)}")
                '''


    def setImagesPdf (self,url):
        namePDF = url.split("/")
        namePDF = namePDF[2]
        doc = fitz.open(namePDF+".pdf")
        for i in range(len(doc)):
            for img in doc.get_page_images(i):
                xref = img[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:      
                    pix.save("p%s-%s.png" % (i, xref))
                else:               
                    pix1 = fitz.Pixmap(fitz.csRGB, pix)
                    pix1.save("p%s-%s.png" % (i, xref))
                    pix1 = None
                pix = None

      
    def setType(self,url):
        r = requests.get(url)
        content_type = r.headers.get('content-type')
        
        if 'application/pdf' in content_type:
            ext = 'pdf'
            
            
            namePDF = url.split("/")
            namePDF = namePDF[2]
            with open(namePDF+'.pdf', 'wb') as f:
                f.write(r.content)
            
        elif 'text/html' in content_type:
            ext = 'html'
            
        else:
            ext = ''
            print('Unknown type: {}'.format(content_type))

        return ext



    
