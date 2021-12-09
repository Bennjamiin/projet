#!/bin/env python3 
from Ressource import Ressource


class Collecte():  
    def __init__(self, urls):
        self.urls = urls
        self.ressources = []

    def run(self,traitement,urls):
        for url in self.urls:
            if traitement=='Nuage':           #### A CHANGER
                self.textes = []
                texte = Ressource(url)
                texte.text()
                self.textes.append(texte)
                for i in self.textes:
                    self.ressources.append(i.text())
            elif traitement=='Image':
                self.images = []
                imge = Ressource(url)        
                imge.image()
                self.images.append(imge)       
                for i in self.images:
                    self.ressources.append(i.img_urls)
            

    def content(self): 
        return self.ressources
