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
            if not (element in '()*| E'):
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
        return postfix
