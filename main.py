from Regex import *
from AFN import *

Expresion = input('Ingrese la expresion regular: ')

# Generar AFN
regex = Regex(Expresion)

if not regex.validar_expresion_regular():
    print('La expresion regular no es valida')
    exit()

print('La expresion regular es valida')
afn = AFN(regex)
afn.dibujar()

print(afn)



