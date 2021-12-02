from src.ressource import Ressource

class Collecte():

    def __init__(self, array):
        self.array = array
        self.result = []

    def run(self):
        for i in self.array:
            self.result.append(Ressource(i).text())
    
    def content(self):
        return self.result

    def runimg(self):
        for i in self.array:
            self.result.append(Ressource(i).image())