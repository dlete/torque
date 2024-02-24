# http://matthiaseisen.com/articles/graphviz/
# https://graphviz.readthedocs.io/en/stable/

from graphviz import Digraph

ne = 'edge1-dcu-glasnevin.nn.hea.net'
nnis = ['edge1-dcu.nn.hea.net', 'edge2-dcu.nn.hea.net']


print("This is the Ne")
print(ne)
print("\nand these are its NNI neighbors")
for n in nnis:
    print(n)


dot = Digraph(comment='ne and its nnis', node_attr={'shape': 'egg'})
dot.node(ne, ne)
for n in nnis:
    dot.node(n, n)
    dot.edge(ne, n)
dot.format = 'svg'
dot.render('ne_nnis.gv', view=False)


dot = Digraph(comment='The Round Table')

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

dot.render('round-table.gv', view=False)
