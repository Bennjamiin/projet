from src.traitement import Traitement
from src.collecte import Collecte

class Prisme():

    def __init__(self, type):
        self.type = type
    

    def run(self, path):
        if self.type == "Nuage":

            file = open(path, 'r')

            url = [i.strip() for i in file.readlines()]

            cl = Collecte(url)
            cl.run()

            tr = Traitement()
            tr.load(cl.content())
            tr.run()

            self._tr = tr

        if self.type == "Image":
            
            file = open(path, 'r')

            url = [i.strip() for i in file.readlines()]

            cl = Collecte(url)
            cl.runimg()

            tr = Traitement()
            tr.load(cl.content())
            tr.runimg()

            self._tr = tr


    def show(self):
        if self.type == "Nuage":
            return self._tr.show()
        elif self.type == "Image":
            return self._tr.showimg()
        