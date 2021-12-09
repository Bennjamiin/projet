#!/bin/env python3 

urls = ['https://math.univ-angers.fr/','http://dominique.frin.free.fr/terminales/coursTS_integration.pdf']  

  
#Paramètres nuage de mots
'''
mots_exclus= list()
with open("stopword.txt", encoding ="utf_8_sig") as f:
    for line in f:
        mots_exclus.append(line.strip())
f.close()
'''
mots_exclus = ['de'] 
navigateurpath = None
nombre_mots = 100 
