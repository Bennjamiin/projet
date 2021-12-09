#!/bin/env python3 
import pathlib
import requests
import webbrowser
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import os
from config import *





class Traitement():
    def load(self,fichiers): 
        self.fichiers = fichiers

    def run(self,traitement):
        if traitement=='Nuage':        #####OK
            self.cloud = []        
            k=0 
            for i in self.fichiers:          
                cloud = WordCloud(stopwords = mots_exclus, max_words=nombre_mots,max_font_size=50).generate(i)        
                save_dir = f"Cloud/{k}.png"             
                cloud.to_file(save_dir)
                self.cloud.append(save_dir) 
                k+=1
        elif traitement=='Image':
            self.images=[]
            k=0
            for url in self.fichiers:
                if url == ['PDF']:  ## si c'est un fichier PDF
                    for filename in os.listdir(f'{os.getcwd()}/image/PDF'): #on ajoute a la liste self.images le chemin et nom des images enregistré dans image/PDF
                        self.images.append(f'{os.getcwd()}/image/PDF/{filename}')


                else:   ##fichier HTML On télécharge les images dans le fichier image/HTML
                    for i in url:
                        file_ext = i.split('.')[-1]
                        with open(f'image/HTML/{k}.{file_ext}', 'wb') as f:
                            f.write(requests.get(i).content)

                        self.images.append(f"image/HTML/{k}.{file_ext}") #on ajoute a la liste self.images le chemin et nom des différentes images
                        k+=1



    def show(self,traitement):              ###### OK
        base = """ 
                <html>
                    <head>
        
                    </head>
                </html> 
                """       
                
        soup = BeautifulSoup(base, features="html.parser") 
        if traitement=='Nuage':
            for i in self.cloud:
                word = soup.new_tag("img", src=i, style="display:block")
                soup.head.append(word)        
                soup.head.append(soup.new_tag('br'))
            with open("nuages.html", "w") as f:
                f.truncate(0)
                f.write(str(soup))        
            webbrowser.open('nuages.html')   

        elif traitement=='Image':
            for i in self.images: 
                image = soup.new_tag("image", src=i, style="display:block")
                soup.head.append(image)        
                soup.head.append(soup.new_tag('br'))
            with open("Image.html", "w") as f: 
                f.truncate(0)
                f.write(str(soup))
            webbrowser.get(navigateurpath).open('Image.html')


                
                


