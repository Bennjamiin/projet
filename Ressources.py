import PyPDF2
import requests
from bs4 import BeautifulSoup
import re


class Prisme:

    def __init__(self,traitement):
        self.traitement=traitement
        self.aTraiter = list()
        self.run("listeURLS.txt"


    def run(self,fichier):
        with open(fichier, encoding ="utf_8_sig") as f:
            urls = list()
            for ligne in f :
                urls.append(ligne)

        une_collecte = Collecte(urls)
        une_collecte.run()
        self.aTraiter = une_collecte.content()
        

    def show(self):
        pass


        

class Collecte:
    def __init__(self,listURL):
        self.liste=listURL
        self.contentsText=list()
        print("Ok start collecte")


    def run(self):
        for url in self.liste :
            ressource = Ressource(url)
            self.contentsText.append(ressource.text)
            print("Ok ressource")


    def content(self):
        return self.contentsText



'''
class Traitement():
'''




















class Ressource:
    def __init__(self,lien):
        self.lien = lien
        self.type = self.setType(lien)
        self.text = self.setText(lien)
        self.setImages()
        
        


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


    def setImages (self):

        site = 'https://www.geeksforgeeks.org/how-to-extract-images-from-pdf-in-python/'

        response = requests.get(site)

        soup = BeautifulSoup(response.text, 'html.parser')
        img_tags = soup.find_all('img')

        urls = [img['src'] for img in img_tags]

        for url in urls:
            filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
            if not filename:
                 '''print("Regex didn't match with the url: {}".format(url))'''
                 continue
            with open(filename.group(1), 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative 
                    # if it is provide the base url which also happens 
                    # to be the site variable atm. 
                    url = '{}{}'.format(site, url)
                response = requests.get(url)
                f.write(response.content)

      
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



    
