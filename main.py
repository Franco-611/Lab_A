from Regex import *
from AFN import *

Expresion = input('Ingrese la expresion regular: ')

# Generar AFN
regex = Regex(Expresion)

mensaje = regex.validar_expresion_regular()

if ( mensaje != True):
    print('La expresion regular no es valida')
    print(mensaje)
    exit()

print('La expresion regular es valida')
afn = AFN(regex)
afn.dibujar()

print(afn)



