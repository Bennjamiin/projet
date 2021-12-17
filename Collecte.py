#!/bin/env python3
from Ressource import Ressource
import os
import shutil

class Collecte():               
    def __init__(self, urls):    
        self.urls = urls
        self.result=[]

    def run(self,traitement):     
        num_pag=1
        if traitement=='Image':
            if os.path.exists('PDF'):
                shutil.rmtree('PDF')
            if not os.path.exists('PDF'):
                os.makedirs('PDF')
            if os.path.exists('HTML'):
                shutil.rmtree('HTML')
            if not os.path.exists('HTML'):
                os.makedirs('HTML')      
        for url in self.urls:
            if traitement=='Nuage':          
                self.mots = []
                texte = Ressource(url)
                texte.text()
                self.mots.append(texte)
                for i in self.mots:
                    self.result.append(i.text())
            elif traitement=='Image':
                self.image = []
                images = Ressource(url)        
                images.image(num_pag)
                self.image.append(images)       
                for i in self.image:
                    self.result.append(i.img)
            num_pag+=1
            

    def content(self): 
        return self.result
