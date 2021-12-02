from Ressource import Ressource





class Collecte:
    def __init__(self,urls):
        self.urls=urls
        self.result=[]


    def run(self):
        for urls in self.urls :            #### on effectue les opérations demandés grâce à Ressource
            self.result.append(Ressource(urls).setText())           ###### rajoute le texte trouver dans Ressource
            print("Ok ressource")    


    def content(self):
        return self.contentsText
