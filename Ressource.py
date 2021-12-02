import PyPDF2
import requests
from bs4 import BeautifulSoup
import os
from abc import ABC, abstractmethod
from requests_html import HTMLSession


class Ressource:
    def __init__(self,lien):
        self.lien = lien
        self.type = self.setType(lien)
        self.text = self.setText(lien)

        
        
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
            # supprime les scripts et les éléments de styles
            for script in soup(["script", "style"]):
                script.extract()
            texte = soup.get_text()
            
            #Epure le texte pour enlever les espace et les retours à la ligne
            lines = (line.strip() for line in texte.splitlines())   
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            texte = '\n'.join(chunk for chunk in chunks if chunk)

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