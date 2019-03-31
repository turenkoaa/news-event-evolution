import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(fromV, toV):
    df = pd.DataFrame({'from': fromV, 'to': toV})

    # Build your graph
    G = nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.DiGraph())

    # Plot it
    nx.draw(G, with_labels=True)
    plt.show()
