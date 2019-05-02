import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(fromV, toV):
    df = pd.DataFrame({'from': fromV, 'to': toV})

    # Build your graph
    G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph())
    graphs = list(nx.connected_component_subgraphs(G))
    for g in graphs:
        pos = nx.spring_layout(g)

    # Plot it
        nx.draw(g, pos, with_labels=True)
        plt.show()
