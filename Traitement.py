#!/bin/env python3 
import requests
import webbrowser
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import os
from config import *


class Traitement():
    def load(self,liste): 
        self.liste = liste     

    def run(self,traitement):
        indice=0
        if traitement=='Nuage':      
            self.cloud = []        
            for mot in self.liste:          
                cloud = WordCloud(stopwords = mots_exclus, max_words=nombre_mots,max_font_size=50).generate(mot)        
                save_dir = f"Cloud/{indice}.png"             
                cloud.to_file(save_dir)
                self.cloud.append(save_dir) 
                indice+=1
        elif traitement=='Image':     
            self.images=[]
            for img in self.liste:
                if img == ['PDF']:  
                    for numero in os.listdir(f'PDF'): 
                        self.images.append(f'PDF/{numero}')
                else:  
                    for i in img:
                        numero = i.split('.')[-1]
                        with open(f'HTML/{indice}.{numero}', 'wb') as f:
                            f.write(requests.get(i).content)
                        self.images.append(f"HTML/{indice}.{numero}") 
                        indice+=1



    def show(self,traitement):       
        base =  """ 
                <html>
                    <head>
                    </head>
                </html> 
                """       
                
        soup = BeautifulSoup(base, features="html.parser") 
        if traitement=='Nuage':
            for i in self.cloud:
                word = soup.new_tag("img", src=i)
                soup.head.append(word)
                soup.head.append(soup.new_tag('br'))
            with open("Nuage.html", "w") as f:
                f.truncate(0)
                f.write(str(soup))        
            webbrowser.open('Nuage.html')   
            print("Nuage de mot affiché")

        elif traitement=='Image':
            for i in self.images: 
                image = soup.new_tag("image", src=i, style="display:block")
                soup.head.append(image)        
                soup.head.append(soup.new_tag('br'))
            with open("Image.html", "w") as f: 
                f.write(str(soup))
            webbrowser.get(None).open('Image.html')
            print("Images de docs affichés")
