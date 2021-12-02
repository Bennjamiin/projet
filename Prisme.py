from Traitement import Traitement
from Collecte import Collecte



class Prisme:
    def __init__(self,traitement):
        self.traitement = traitement
        self.aTraiter = list()
        

    def run(self,fichier):
        if self.type=='Nuage':
            file=open(fichier,'r')
            urls=[i.strip() for i in file.readlines()]
            une_collecte = Collecte(urls)
            une_collecte.run()
            self.aTraiter = une_collecte.content()
            un_traitement=Traitement()
            un_traitement.charge(self.aTraiter)
            self.un_traitement.run()
            self.un_traitement=un_traitement
        
        elif self.type=='Image':
            pass
      

    def show(self):
        if self.traitement=='Nuage':
            self.un_traitement.show()
        elif self.traitement=='Image':
            pass
        else:
             print("mauvais traitement enregistré")




        