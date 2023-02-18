import pydot

# Definir el grafo del AFN utilizando la sintaxis de Graphviz
afn = pydot.Dot(graph_type='digraph')
afn.set_rankdir('LR')  # Establecer la dirección de la grafica
qI = pydot.Node('qI', shape='point')
q0 = pydot.Node('q0', shape='circle')
q1 = pydot.Node('q1', shape='circle')
q2 = pydot.Node('q2', shape='doublecircle')
afn.add_node(qI)
afn.add_node(q0)
afn.add_node(q1)
afn.add_node(q2)
afn.add_edge(pydot.Edge(qI, q0))
afn.add_edge(pydot.Edge(q0, q1))
afn.add_edge(pydot.Edge(q1, q2, label='a'))
afn.add_edge(pydot.Edge(q1, q1, label='b', constraint='false'))
afn.add_edge(pydot.Edge(q1, q2, label='c'))

# Generar la imagen del grafo del AFN
afn.write_png('afn.png')