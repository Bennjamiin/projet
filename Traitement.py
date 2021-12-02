import requests
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import pathlib


class Traitement:

    def charge(self,fichiers):
        self.fichiers=fichiers
        
    
    def run(self):
        for text in self.aTraiter :
            r = text.split()
            self.conclusion += len(r)
            


    def show(self):
        print(self.conclusion)