from Regex import *
from AFN import *

Expresion = input('Ingrese la expresion regular: ')

# Generar AFN
regex = Regex(Expresion)
afn = AFN(regex)
afn.dibujar()

print(afn)



