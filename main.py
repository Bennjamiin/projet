#!/bin/env python3
from Prisme import *
from Ressource import *

u1="https://www.lespommesdeterre.com/histoire/"

u2="http://dominique.frin.free.fr/terminales/coursTS_integration.pdf"
U=[u1,u1]





"""
ressource=Ressource(u1)

print(ressource.setText(u1))  ###fonctionne



print(ressource.setImages(u1))  ###fonctionne


print(ressource.setType(u1))    ###fonctionne

"""


"""
ressource=Ressource(u2)         
"""


"""
print(ressource.setText(u2))      #####fonctionne
"""


"""
print(ressource.setType(u2))  ###fonctionne 
"""

"""
print(ressource.setImages(u2))     ### ne fonctionne pas , peut être pas à faire ???
"""


collect=Collecte.run(U)




"""
un_prisme = Prisme('Nuage')


un_prisme.run(U)

un_prisme.show()
"""

###      """