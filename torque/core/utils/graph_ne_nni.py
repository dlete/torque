# http://matthiaseisen.com/articles/graphviz/
# http://graphviz.readthedocs.io/en/stable/manual.html#basic-usage
# designschool.canva.com/blog/100-color-combinations

def graph_ne_nni(ne, nnis):
    '''
    Input:
        ne (str) is a fqdn
        nnis (list) is a list of fqdn
    Output:
        a graph
    '''

    import graphviz as gv
    g1 = gv.Graph(format='svg',
        graph_attr={'bgcolor': 'transparent',
                'layout': 'dot',
                'nodesep': '4',
                'splines': 'false'
            },
            edge_attr={'color': '#07575B',
                'len': '5',
                'minlen': '6',
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
    #filename = g1.render(filename='ne_nnis')
    #fname = "../static/nnis_" + ne
    #filename = g1.render(filename=ne)
    #filename = g1.render(filename=fname)
    #filename = g1.render(filename="../static/nnis_" + ne)  # /workspace/pjt_torque/static
    #filename = g1.render(filename="static/nnis_" + ne)     # /workspace/pjt_torque/torque/static
    filename = g1.render(filename="core/static/nnis_" + ne) # /workspace/pjt_torque/torque/core/static
    #print(filename)

'''
# mark
ne = 'edge1-dcu-glasnevin'
nnis = ['edge1-dcu', 'edge2-dcu']
graph_ne_nni(ne, nnis)

ne = 'core1-blanch'
nnis = ['core1-dcu', 'core1-pw', 'core2-blanch', 'dist2-itb', 'edge1-blanch']
graph_ne_nni(ne, nnis)
'''
