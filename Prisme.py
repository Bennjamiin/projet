#!/bin/env python3 
from Collecte import *
from Traitement import *





class Prisme():
    def __init__(self,traitement):
        self.traitement = traitement

    def run(self,urls):        
        collecte = Collecte(urls)
        self.Tr = Traitement()
        self.Tr.load(collecte.content())
        collecte.run(self.traitement, urls)
        self.Tr.run(self.traitement)
  
        
    def show(self):
        return self.Tr.show(self.traitement)
