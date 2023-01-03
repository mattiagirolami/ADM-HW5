from collections import Counter
from statistics import mean

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd


## Functionality 1
def TOP_N(N,G_hero_net,edges_df):
    subnodes=set([el for el in edges_df.groupby('hero').count().sort_values(by=['comic'],ascending=False).head(N).index])
    return G_hero_net.subgraph(subnodes)

def number_of_nodes(graph_type,graph):
    if graph_type == 1 :
        print(f"The graph have " + str(graph.number_of_nodes()) +  " nodes")
        return
    elif graph_type == 2 :
        comic=0
        hero=0
        attr=nx.get_node_attributes(graph,'type')
        for k in graph.nodes:
            if (attr[k]=='comic'):
                comic+=1
            else:
                hero+=1
        print(f"The graph have " + str(comic) +  " nodes of type: COMIC")
        print(f"The graph have " + str(hero) +  " nodes of type: HERO")
        return 
    else:
        return ('Wrong type number')
    
def number_of_collaborations(graph_type,graph):
    if graph_type!=1:
        print('Valid only for type 1')
        return
    else:
        for node in graph:
            print( node + " has " + str(graph.degree(node)) + " collaborations.")
        return
    
def number_of_hero_in_each_comic(graph_type):
    if graph_type!=2:
        print('number_of_hero_in_each_comic: Valid only for type 2')

        return
    else:
        attr=nx.get_node_attributes(G_edges_net,'type')
        List_hero=[i for i in G_edges_net.nodes if attr[i]=='hero']
        tmp=0
        for hero in List_hero:
            if G_edges_net.degree(hero)==12651:
                print( hero + " has appeared in each comic")
                tmp+=1
        return tmp
    
def degree_distribution(graph):
    deg = [graph.degree(n) for n in graph.nodes()]
    deg_count = Counter(deg)
    return deg_count

def degree_mean(graph):
    deg = [graph.degree(n) for n in graph.nodes()]
    return mean(deg)

def nodes_hubs(graph):
    deg = [graph.degree(n) for n in graph.nodes()]
    percentile = np.percentile(deg, 95)

    return [n for n in graph.nodes() if graph.degree(n) > percentile]

def graph_density(graph):
    nodes_count = graph.number_of_nodes()
    max_edges = nodes_count * (nodes_count - 1) / 2
    edges_count = graph.number_of_edges()
    density = edges_count/ max_edges
    return density


## Functionality 2
damping_factor = 0.85

def compute_pagerank(graph, pagerank):
    for node in graph:
        rank = 1- damping_factor
        for neighbor in graph[node]:
            rank += damping_factor * pagerank[neighbor] / len(graph[neighbor])
            pagerank[node] = rank
    return pagerank

def page_rank_metric(graph):
    directed_graph = graph.to_directed()
    pagerank = {node: 1/len(directed_graph) for node in directed_graph}
    while True:
        prev_rank = pagerank.copy()
        pagerank = compute_pagerank(directed_graph, pagerank)
        if all(abs(prev_rank[node] - pagerank[node]) < 0.001 for node in pagerank):
            break
    return (pagerank)

def betweeness_metric(graph): #MAKE SURE TO CONSIDER ONLY A SUBGRAPH BECAUSE THIS ALGORITHM IN VERY SLOW
    betweeness = {n: 0 for n in graph.nodes()}
    for node in graph.nodes():
        for destin in graph.nodes():
            if destin!=node:
                paths = list(nx.all_shortest_paths(graph, node, destin))
                for key in paths:
                    for value in paths:
                        if key!=value:
                            for n in paths[(key, value)]:
                                betweeness[n] += 1 / len(paths[(key, value)])
    return betweeness

def closeness_metric(graph):
    closeness = {n: 0 for n in graph.nodes()}
    for node in graph.nodes():
        count=0
        for destin in graph.nodes():
            if destin!=node:
                count += len(list(nx.all_shortest_paths(graph, node, destin)))
        closeness[node]=(len(graph.nodes())-1)/count   
    return closeness

def degree_metric(graph):
    deg={n: 0 for n in graph.nodes()}
    for node in graph.nodes():
        deg[node]=graph.degree[node]/(len(graph.nodes())-1)
    return deg #IF YOU COMPARE IT WITH THE BUILT IN FUNCTION THERE IS A DIFFERENCE OF e-16 IN THE VALUES, BASICALLY ARE THE SAME





