from stack import *

class Regex(object):
    def __init__(self, Expresion):
        self.expresion = Expresion
        self.Alfabeto = set()
        self.__generar_alfabeto()

    def __generar_alfabeto(self):
        # Obtener elementos que no son operadores
        # ni parentesis
        for element in self.expresion:
            if not (element in '()*| ε + ? ^'):
                self.Alfabeto.add(element)
    
    def get_alfabeto(self):
        return self.Alfabeto

    def obtenerPrecedente(self, letra):
        if letra == '(':
            return 1
        elif letra == '|':
            return 2
        elif letra == '.':
            return 3
        elif letra == '?':
            return 4
        elif letra == '*':
            return 4
        elif letra == '+':
            return 4
        elif letra == '^':
            return 5
        else:
            return 6

    def get_expresion(self):
        return self.expresion

    def validar_expresion_regular(self):

        if not self.expresion.strip():
            return "Error: La expresión está vacía."


        balance = 0
        subexpresiones = []
        pila_indices_apertura = []
        for i, char in enumerate(self.expresion):
            if char == "(":
                balance += 1
                pila_indices_apertura.append(i)
            elif char == ")":
                balance -= 1
                if balance < 0:
                    return "Error: Los paréntesis están desbalanceados."
                indice_apertura = pila_indices_apertura.pop()
                subexpresion = self.expresion[indice_apertura+1:i]
                subexpresiones.append(subexpresion)
        if balance != 0:
            return "Error: Los paréntesis están desbalanceados."

        if '' in subexpresiones:
            return "Error: La expresión esta vacia."
        for subexpresion in subexpresiones:
            if subexpresion.isspace():
                return "Error: La expresión esta vacia."

        i = 0
        longitud = len(self.expresion)
        while i < longitud:
            caracter_actual = self.expresion[i]
            if caracter_actual == '(':
                balance = 1
                i += 1
                while i < longitud and balance > 0:
                    caracter_actual = self.expresion[i]
                    if caracter_actual == '(':
                        balance += 1
                    elif caracter_actual == ')':
                        balance -= 1
                    i += 1
                if balance != 0:
                    return "Error: Los paréntesis en la subexpresión están desbalanceados."
            elif caracter_actual in '*+?':
                if i == 0 or self.expresion[i-1] in '?':
                    return "Error: El operador está al principio de la expresión o después de otro operador."
            elif caracter_actual == '|':
                if i == 0 or i == longitud - 1 or self.expresion[i-1] == '|' or self.expresion[i+1] == '|' or self.expresion[i+1] == '?' or self.expresion[i+1] == '*' or self.expresion[i+1] == '+':
                    return "Error: El operador | está en la posición incorrecta o seguido de otro operador."
            i += 1

        return True

    def get_postfix(self):

        res = ""
        operadores = ['|', '?', '+', '*', '^']
        binarios = ['^', '|']

        for element in range(len(self.expresion)):
            c1 = self.expresion[element]
            if (element + 1) < len(self.expresion):
                c2 = self.expresion[element + 1]
                res += c1

                if (c1 != '(') and (c2 != ')') and (c2 not in operadores) and (c1 not in binarios):
                    res += '.'

        res += self.expresion[len(self.expresion) - 1]

        postfix = ''

        stack = Stack()

        for c in res:
            if c == '(':
                stack.push(c)
            elif c == ')':
                while stack.peek() !='(':
                    postfix += stack.pop()

                stack.pop()
            else:
                while stack.size() > 0:
                    peekedchar = stack.peek()
                    peekedCharPrecedence = self.obtenerPrecedente(peekedchar)
                    currentCharPrecedence = self.obtenerPrecedente(c)

                    if peekedCharPrecedence >= currentCharPrecedence:
                        postfix += stack.pop()
                    else:
                        break
                stack.push(c)


        while stack.size() > 0:
            postfix += stack.pop()

        postfix = postfix.replace('?', 'ε|')

        return postfix
