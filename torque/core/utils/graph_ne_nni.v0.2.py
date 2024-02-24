# http://matthiaseisen.com/articles/graphviz/
# http://graphviz.readthedocs.io/en/stable/manual.html#basic-usage
# designschool.canva.com/blog/100-color-combinations

import graphviz as gv

ne = 'edge1-dcu-glasnevin.nn.hea.net'
nnis = ['edge1-dcu.nn.hea.net', 'edge2-dcu.nn.hea.net']

ne = 'edge1-dcu-glasnevin'
nnis = ['edge1-dcu', 'edge2-dcu']


g1 = gv.Graph(format='svg',
        graph_attr={'bgcolor': 'transparent',
            'layout': 'neato'
        },
        edge_attr={'color': '#07575B',
            'len': '5',
            'penwidth': '10'
        },
        node_attr={'color': '#07575C',
            'fillcolor': '#C4DFE6',
            'fixedsize': 'true',
            'fontcolor': '#07575B',
            'fontname': 'nimbus',
            'fontsize': '14',
            'penwidth': '10',
            'shape': 'circle',
            'style': 'filled',
            'width': '2',
        }
)
g1.node(ne, fillcolor='#66A5AD')
for n in nnis:
    g1.node(n)
    g1.edge(ne, n)

#print(g1.source)
filename = g1.render(filename='ne_nnis')
print(filename)
