# -*- coding: utf-8 -*-
"""
Network analysis

Using the edgelist of support conversations, run a basic analysis of the group
"""

import pandas as pd
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

edges = pd.read_csv(r"edgelist.csv", index_col=False)

edgeList = list()
for q in range(0, len(edges["0"])):
    edgeList.append((edges["0"][q], edges["1"][q], {"weight": edges["2"][q]}))

g = nx.Graph()
g.add_edges_from(edgeList)

#assign node weights to every node
nodeIter = iter(g.nodes)
summDict = dict()
avgDict = dict()
numDict = dict()
while(True):
    try:
        this = next(nodeIter)
        summ = 0
        count = 0
        edges = iter(g.edges(this, data = True))
        while(True):
            try:
                thisEdge = next(edges)
                summ += (int(str(thisEdge[2].values())[-3:-2]))
                count += 1
            except: break
        numDict.update({this:count})
        summDict.update({this: summ})
        avg = summ / count
        avgDict.update({this: avg})
    except: break
nx.set_node_attributes(g, summDict, 'sumRelations')
nx.set_node_attributes(g, avgDict, 'avgRelations')
nx.set_node_attributes(g, numDict, 'numRelations')
# print(nx.get_node_attributes(g, 'sumRelations'))
# print()
# print(nx.get_node_attributes(g, 'avgRelations'))
# print()
# print(nx.get_node_attributes(g, 'numRelations'))


print(sorted([(value,key) for (key,value) in numDict.items()]))
print()
print(sorted([(value,key) for (key,value) in avgDict.items()]))


# #boxplots
# plt.boxplot(np.array(list(avgDict.values())))
# plt.title('Distribution of Average Quality of Supports')


#nx.draw(g, with_labels = True, node_color = '#DDA0DD', edge_color = '#8aacb8')
#MACRO ANALYSIS -------------------------------------
#Assortativity
print("The assortativity of the graph: " + str(nx.degree_assortativity_coefficient(g)))
#Average Clustering
print("The average clustering coefficient: " + str(nx.average_clustering(g)))
#Density
print("The Density of our Graph: " + str(nx.density(g)))
#Number of Nodes
print("The Number of Nodes: " + str(len(g.nodes)))
#Number of Edges
print("The Number of Edges: " + str(len(g.edges)))

#MICRO ANALYSIS -------------------------------------
#degree centrality
print("The top 5 nodes by degree centrality:")
deg = pd.DataFrame(dict(nx.degree_centrality(g)).items())
print(deg.sort_values(by = [1], ascending= False).head(5)) 
#betweenness centrality
print("The top 5 nodes by betweenness centrality:")
bet = pd.DataFrame(dict(nx.betweenness_centrality(g)).items())
print(bet.sort_values(by = [1], ascending= False).head(5))

#boxplot
plt.boxplot(np.array(bet.sort_values(by = [1], ascending= False)[1]))
plt.title('Distribution of Betweenness')


#Bottom of each list
#degree centrality
print("The bottom 5 nodes by degree centrality:")
deg = pd.DataFrame(dict(nx.degree_centrality(g)).items())
print(deg.sort_values(by = [1], ascending= False).tail(5)) 
#betweenness centrality
print("The bottom 5 nodes by betweenness centrality:")
bet = pd.DataFrame(dict(nx.betweenness_centrality(g)).items())
print(bet.sort_values(by = [1], ascending= False).tail(5))
