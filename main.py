from Regex import *
from AFN import *

Expresion = input('Ingrese la expresion regular: ')

# Generar AFN
regex = Regex(Expresion)
afn = AFN(regex)

print(afn)



