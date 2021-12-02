import PyPDF2
import requests
from bs4 import BeautifulSoup
import re
import os
from abc import ABC, abstractmethod



class Prisme:
    def __init__(self,traitement):
        self.traitement = traitement
        self.aTraiter = list()       ####liste des urls a traiter
        self.un_traitement = self.traitement()
        self.run("listeURLS.txt")
        



    def run(self,fichier):
        with open(fichier, encoding ="utf_8_sig") as f:
            urls = list()   #### création de la liste des urls
            for ligne in f :
                urls.append(ligne)    #### implémentations des urls dans la liste

        une_collecte = Collecte(urls)     ##### On commence par utiliser Collecte pour entrer la liste des urls
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
        os.rmdir('images')   ####    supprime répertoire vide
        os.mkdir('images')    #####   crée le répertoire 'images'
        print("Ok start collecte")   #####  démarrage


    def run(self):
        for url in self.liste :   ##### pour les différents lien transmit
            ressource = Ressource(url)           #### on effectue les opérations demandés grâce à Ressource
            self.contentsText.append(ressource.text)           ###### rajoute le texte trouver dans Ressource
            print("Ok ressource")           


    def content(self):
        return self.contentsText






class TraitementTrivial:
    def __init__(self):
        self.aTraiter = list()
        self.conclusion = 0
        
    
    def run(self):
        for text in self.aTraiter :
            r = text.split()   #####sépare tous les mots dans une seul liste
            self.conclusion += len(r)    ####compte combien d'élément (de mots) dans la liste pour connaître le nombre de mots totals
            


    def show(self):
        print(self.conclusion)         ##### renvoi le nombre de mot trouver précèdement






class Ressource:
    def __init__(self,lien):
        self.lien = lien
        self.type = self.setType(lien)
        self.text = self.setText(lien)
        self.setImages(lien)
        
        


    def setText(self,lien):
        texte = ""
        if (self.type == 'pdf'):         #### si le doc est un pdf
            namePDF = lien.split("/")       #### on enlève les "/"
            namePDF = namePDF[2]            #### on ne garde que la 2ème partie de l'url, celle avec le nom du PDF 
            pdfFileObject = open(namePDF+'.pdf', 'rb')          #### permet d'ouvrir le dossier via la création de notre nom de pdf
            pdfReader = PyPDF2.PdfFileReader(pdfFileObject)         #####  permet d'effectuer toutes les manipulations relier à la lecture du doc
            count = pdfReader.numPages              ### on compte le nombre de pages
            for i in range(count):          ### on boucle sur le nombre de pages
                page = pdfReader.getPage(i)
                texte += page.extractText()             ### on "relie" les pages entre elles pour ne faire qu'une seule page


                              
        elif (self.type == 'html') :            #### si le doc est un html
            html = requests.get(lien).text              ##### on donne la valeur du lien à la variable 'html'
            soup = BeautifulSoup(html, features="html.parser")      #####on donne à la variable 'soup' les caractéritiques de html
             # kill all script and style elements
            for script in soup(["script", "style"]):        #### on boucle sur le script du html
                script.extract()         #### on extrait le texte de html
            texte = soup.get_text()          #### on donne à la variable texte la valeur de tout le texte du html
            #Epure le texte pour enlever les espace et les retours à la ligne
            lines = (line.strip() for line in texte.splitlines())           #### On enlève les retours à la ligne
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))          ### on enlève les espaces
            texte = '\n'.join(chunk for chunk in chunks if chunk)                #### On réécrit le texte sans saut de lignes ni espaces

        return texte


    def setImages (self,url):

        '''site = 'https://www.geeksforgeeks.org/how-to-extract-images-from-pdf-in-python/'''

        r = requests.get(url)                  #### à l'aide du package 'requests' je donne à la variable r l'url
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        images = soup.findAll('img')              ##### j'utilise le package findAll pour trouver tous les doc images et les mettre dans une liste

        # initial count is zero
        count = 0
 
        # print total images found in URL
        print(f"Total {len(images)} Image Found!")   
 
        # checking if images is not zero
        if len(images) != 0:
            for i, image in enumerate(images):
                
                try:
                    # In image tag ,searching for "data-srcset"
                    image_link = image["data-srcset"]
                except:
                    try:
                        # In image tag ,searching for "data-src"
                        image_link = image["data-src"]
                    except:
                        try:
                            # In image tag ,searching for "data-fallback-src"
                            image_link = image["data-fallback-src"]
                        except:
                            try:
                                # In image tag ,searching for "src"
                                image_link = image["src"]
                                print(image_link)
 
                            # if no Source URL found
                            except:
                                pass
 
                try:
                    filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', image_link)
                    if not filename:
                        '''print("Regex didn't match with the url: {}".format(image_link))'''
                        continue
                    with open(filename.group(1), 'wb') as f:
                        print(image_link)
                        if 'http' not in image_link:
                            image_link = '{}{}'.format(url, image_link)
                        r = requests.get(image_link).content
                        f.write(r)
                        
 
                    count += 1
                except:
                    print("pas ok")
                    pass
 
            if count == len(images):
                print("All Images Downloaded!")
             
            else:
                print(f"Total {count} Images Downloaded Out of {len(images)}")

      
    def setType(self,url):
        r = requests.get(url)      #### à l'aide du package 'requests' je donne à la variable r l'url
        content_type = r.headers.get('content-type')        ####on extrait le type dans l'url
        
        if 'application/pdf' in content_type:           #### si on a écrit application/pdf dans le type
            ext = 'pdf'             ### on donne à la variable ext le mot pdf
            
            
            namePDF = url.split("/")        #### on supprime les '/' de l'url
            namePDF = namePDF[2]             #### on ne garde que la 2ème partie de l'url, celle avec le nom du PDF
            with open(namePDF+'.pdf', 'wb') as f:           #### on ouvre le doc avec le nom du PDF trouvé précèdement
                f.write(r.content)                   #### on écrit dans f le texte contenue dans le PDF ouvert
            
        elif 'text/html' in content_type:                ###sinon si on voit écrit html
            ext = 'html'                ### on attribut la valeur 'html' à la variable ext
            
        else:
            ext = ''            ###sinon on ne retourne rien
            print('Unknown type: {}'.format(content_type))             ### on écrit type inconnue avec le nom du nom format mystère

        return ext          #### on retourne la valeur de ext



    
