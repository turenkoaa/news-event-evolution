import community
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(fromV, toV):
    df = pd.DataFrame({'from': fromV, 'to': toV})

    # Build your graph
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())
    graphs = list(nx.weakly_connected_component_subgraphs(G))
    print("Number of Stories: " + str(len(graphs)))

    for g in graphs:
        pos = nx.spring_layout(g)

    # Plot it
        nx.draw(g, pos, with_labels=True)
        plt.show()


def draw_graph3(fromV, toV):

    df = pd.DataFrame({'from': fromV, 'to': toV})

    # Build your graph
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())
    pos = nx.spring_layout(G)
    graphs = list(nx.weakly_connected_component_subgraphs(G))
    print("Number of Stories: " + str(len(graphs)))

    # for g in graphs:
        # pos = nx.spring_layout(g)

    # Plot it
    nx.draw(G, pos, with_labels=True)
    plt.show()



def draw_graph2(fromV, toV):
    df = pd.DataFrame({'from': fromV, 'to': toV})
    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())

    partition = community.best_partition(G)
    labels = {}
    for node in G.nodes():
        labels[node] = node  # news[node]['documentId']

    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)
    count = 0.
    for com in set(partition.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition.keys()
                      if partition[nodes] == com]
        nx.draw_networkx_nodes(G, pos, list_nodes, labels=labels, node_size=20,
                               node_color=str(count / size))

    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.show()



def draw_graph1(fromV, toV, ids, classes):
    df = pd.DataFrame({'from': fromV, 'to': toV})
    carac = pd.DataFrame({'ID': ids, 'classes': classes})

    G = nx.from_pandas_edgelist(df, source='from', target='to', create_using=nx.DiGraph())
    G.nodes()
    carac = carac.set_index('ID')
    carac = carac.reindex(G.nodes())

    nx.draw(G, with_labels=True, node_color=carac['classes'])

    # graphs = list(nx.weakly_connected_component_subgraphs(G))
    # for g in graphs:
    #     pos = nx.spring_layout(g)
    #
    # # Plot it
    #     nx.draw(g, pos, with_labels=True)

    plt.show()