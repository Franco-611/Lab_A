class AF(object):
    def __init__(self, regex):
        if regex != None:
            self.alfabeto = regex.get_alfabeto()
            self.Regex = regex
            self.expresion = ''
        self.estados = set()
        self.transiciones = {}
        self.inicio = set()
        self.aceptacion = set()
        self.name = ''
    
    def e_closure(self, states):
        stack = []
        res = set()
        # Ingresar todos los estados iniciales en stack y en resultados.
        for state in states:
            stack.append(state)
            res.add(state)

        while(len(stack) > 0):
            t = stack.pop()
            # Obtener todos los estados a los que se llega con E.
            reached = [x[0] for x in self.transiciones[t] if x[1] == 'E']
            # Agregar los estados al resultado.
            for u in reached:
                if not(u in res):
                    res.add(u)
                    stack.append(u)
        return res

    def move(self, estados, simbolo):
        result = set()

        # Obtener todos los estados a los cuales se puede mover de estado con simbolo
        for estado in estados:
            for element in self.transiciones[estado]:
                if simbolo == element[1]:
                    result.add(element[0])
                    
        return result
