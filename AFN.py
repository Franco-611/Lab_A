from AF import *
from time import perf_counter

class AFN(AF):
    def __init__(self, regex):
        super().__init__(regex)
        self.stack = []
        self.count = 0
        self.__Thompson()
        self.name = 'AFN'

    def __Thompson(self):
        postfix = self.Regex.get_postfix()
        # Stack made of postfix elements
        for element in postfix:
            self.stack.append(element)

        # Crear AFN con Thompson
        initial, acceptance = self.__crear_AFN()
        self.inicio.add(initial)
        self.aceptacion.add(acceptance)
    
    def __crear_AFN(self):
        if len(self.stack) != 0:
            first = self.stack.pop()
            if first in self.alfabeto or first == 'ε':
                # Se crea un elemento unitario si solo se encuentra un elemento del alfabeto.
                return self.__unidad(first)
            if self.__is_binary(first):
                # Si se encuentra un operador binario, se obtienen las transiciones, recursivamente,
                # para los dos elementos siguientes del stack.
                op1 = self.__crear_AFN()
                op2 = self.__crear_AFN()
                if first == '.':
                    return self.__concat(op2, op1)
                if first == '|':
                    return self.__hamburguesa(op2, op1)
            else:
                # Si se encuentra un Kleene solo se necesita un operador, creado recursivamente.
                op1 = self.__crear_AFN()
                return self.__barco(op1)

    def simular(self, string):
        acu = []
        s = self.e_closure(self.inicio)
        acu.append(('ε', s))
        start = perf_counter()
        if len(string) > 0:
            string = iter(string)
            c = next(string)
            try:
                while True:
                    s = self.e_closure(self.move(s, c))
                    acu.append((c, s))
                    c = next(string)
            except: StopIteration
        end = perf_counter()
        diff = end - start

        if s.intersection(self.aceptacion) != set():
            return True, acu, diff
        
        return False, acu, diff

    def __barco(self, op1):
        # Se crea el estado inicial del barco
        self.count += 1
        initial = self.count
        self.estados.add(initial)
        
        # Se crea la transición al estado inicial del diagrama de transición del argumento.
        transition = (op1[0], 'ε')
        self.transiciones[initial] = [(transition)]

        # Se crea una transición del estado final del argumento a su estado inicial.
        transition = (op1[0], 'ε')
        self.transiciones[op1[1]].append(transition)
        
        # Se crea el estado final del barco.
        self.count += 1
        final = self.count
        self.estados.add(final)
        self.transiciones[final] = []

        # Se añade una transición del estado inicial al final con epsilon.
        transition = (final, 'ε')
        self.transiciones[initial].append(transition)

        # Se crea una transición del estado final del argumento al estado final del barco con epsilon.
        transition = (final, 'ε')
        self.transiciones[op1[1]].append(transition)

        return (initial, final)

    def __hamburguesa(self, op1, op2):
        # Se crea un estado inicial para la hamburguesa.
        self.count += 1
        initial = self.count
        self.estados.add(initial)

        # Se crea una transición para cada una de las dos partes de la hamburguesa
        # Estos son los estados iniciales de los dos operandos del OR.
        transition = (op1[0], 'ε')
        self.transiciones[initial] = [(transition)]
        transition = (op2[0], 'ε')
        self.transiciones[initial].append(transition)

        # Se crea un estado final de la hamburguesa.
        self.count += 1
        final = self.count
        self.estados.add(final)

        self.transiciones[final] = []

        # Se crea una transición del estado final de un componente del OR al final de la hamburguesa.
        transition = (final, 'ε')
        self.transiciones[op1[1]].append(transition)

        # Se crea una transición del estado final del componente restante del OR al final de la hamburguesa.
        transition = (final, 'ε')
        self.transiciones[op2[1]].append(transition)

        return (initial, final)

    def __concat(self, op1, op2):
        # Se obtienen el estado inicial de la primera transición y el final de la segunda.
        initial = op1[0]
        final = op2[1]

        # Se crea una transición entre estos estados con ε
        # Tiene la forma: estado_incial_1 - ε - > estado_inicial_2
        transition = (op2[0], 'ε')

        # Se agrega la transición
        self.transiciones[op1[1]].append(transition)

        # Se devuelve el estado inicial y final de la concatenación.
        return (initial, final)

    def __unidad(self, symbol):
        # Crear dos nuevos estados para crear la transición con el símbolo.
        # La forma es: state_1 - symbol - > state_2
        self.count += 1
        state_1 = self.count
        self.estados.add(state_1)
        self.count += 1
        state_2 = self.count
        self.estados.add(state_2)

        # Se crea una nueva transición con los estados y el símbolo y se agrega a las transiciones del AFN.
        transition = (state_2, symbol)
        self.transiciones[state_1] = [transition]
        self.transiciones[state_2] = []

        # Se retorna el estado inicial y el final de la transición
        return (state_1, state_2)

    def __is_binary(self, element):
        # Se determina si la operación es binaria o no.
        if element in '.|':
            return True
        return False

    def __str__(self):
        res = f'---------------- {self.name} ----------------\n'
        res += 'Estado inicial: ' + str(self.inicio) + '\n'
        res += 'Estado de aceptación: ' + str(self.aceptacion) + '\n'
        res += 'Estados: ' + str(self.estados) + '\n'
        res += 'Símbolos: ' + str(self.alfabeto) + '\n'
        res += 'Transiciones:\n'
        for key in self.transiciones:
            for elements in self.transiciones[key]:
                res += str(key) + ' - (' + str(elements[1]) + ') - > ' + str(elements[0]) + '\n'
        return res