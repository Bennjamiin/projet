#!/bin/env python3 

urls =[]
with open("liste_urls.txt",encoding="utf_8_sig") as f:
    for ligne in f:
        urls.append(ligne.strip())
    f.close
  

mots_exclus= list()
with open("stopword.txt", encoding ="utf_8_sig") as f:
    for ligne in f:
        mots_exclus.append(ligne.strip())
f.close()


f = open('liste_urls.txt', 'r')
text=f.readlines()
NumberOfLine = len(text)
nombre_mots = 50 
max_mots=int(nombre_mots % NumberOfLine)
