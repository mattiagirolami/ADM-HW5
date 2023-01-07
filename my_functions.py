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

#Functionality 5

def edge_to_remove(graph):
  G_dict = nx.edge_betweenness_centrality(graph)
  edge = ()

  # extract the edge with highest edge betweenness centrality score
  for key, value in sorted(G_dict.items(), key=lambda item: item[1], reverse = True):
      edge = key
      break

  return edge

def girvan_newman(graph):
	# find number of connected components
	sg = nx.connected_components(graph)
	sg_count = nx.number_connected_components(graph)

	while(sg_count == 1):
		graph.remove_edge(edge_to_remove(graph)[0], edge_to_remove(graph)[1])
		sg = nx.connected_components(graph)
		sg_count = nx.number_connected_components(graph)

	return sg

def label_propagation(graph):
    # make a deep copy of the graph to preserve the original
    graph = graph.copy()
    
    # assign a unique label to each node in the graph
    for i, node in enumerate(graph.nodes()):
        graph.nodes[node]['label'] = i
    
    # initialize a flag to indicate whether the labels have changed
    labels_changed = True
    
    while labels_changed:
        labels_changed = False
        
        # iterate over the nodes in the graph
        for node in graph.nodes():
            # get the labels of the node's neighbors
            neighbor_labels = [graph.nodes[neighbor]['label'] for neighbor in graph.neighbors(node)]
            
            # if the node has no neighbors, skip it
            if len(neighbor_labels) == 0:
                continue
            
            # get the most common label among the node's neighbors
            most_common_label = max(set(neighbor_labels), key=neighbor_labels.count)
            
            # if the most common label is not the node's current label, update the label
            if graph.nodes[node]['label'] != most_common_label:
                graph.nodes[node]['label'] = most_common_label
                labels_changed = True
    
    # group the nodes into communities based on their labels
    communities = {}
    for node, data in graph.nodes(data=True):
        label = data['label']
        if label not in communities:
            communities[label] = []
        communities[label].append(node)
    
    return list(communities.values())




