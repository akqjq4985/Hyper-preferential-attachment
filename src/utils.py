import numpy as np
import networkx as nx
from itertools import permutations


def no_similarity(Data_class, edge):
    return 1

def radius_jaccard(Data_class, hyperedge):
    
    intersect = set(Data_class.neighbors[hyperedge[0]])
    unionset = set()
    for node in hyperedge:
        node_set = get_radius_neighbors(Data_class, set(), node, 1, 3)
        intersect = set(node_set).intersection(intersect)
        unionset = set(node_set).union(unionset)

    return float(len(intersect))/len(unionset)

def averaged_jaccard_similarity(Data_class, edge):
    jaccard_list = []
    edge_length = len(edge)

    for i in range(edge_length):
        for j in range(i + 1, edge_length):
            try:
                jcd = jaccard(Data_class.neighbors[edge[i]], Data_class.neighbors[edge[j]])
            except:
                jcd = 0
            jaccard_list.append(jcd)

    return np.mean(jaccard_list)


def jaccard(node1, node2):
    s1 = set(node1)
    s2 = set(node2)
    return len(s1 & s2) / len(s1 | s2)


def get_radius_neighbors(Data_class, neighbors, nodeID, iter, max_iter):
    if (iter > max_iter):
        return neighbors
    old_neighbors = neighbors
    new_neighbors = set(Data_class.neighbors[nodeID])
    difference = [x for x in new_neighbors if x not in old_neighbors]
    if not difference:
        return neighbors
    neighbors = old_neighbors.union(new_neighbors)
    for node in difference:
        neighbors = get_radius_neighbors(Data_class, neighbors, node, iter + 1, max_iter)
    return neighbors


def adamic_adar(Data_class, hyperedge):
    # 반지름 5로 늘리기 - union

    for node in hyperedge:
        neighbors = get_radius_neighbors(Data_class, set(), node, 1, 3)
        if (node == hyperedge[0]):
            common_neighbors = neighbors

        else:
            common_neighbors = neighbors.intersection(common_neighbors)

    # 공통 이웃들의 degree에 log씌우고 1에서 나눠서 다 더하기
    Adamic_adar = 0
    for node in common_neighbors:
        if (Data_class.degrees[node] != 1):
            Adamic_adar += 1.0 / np.log(Data_class.degrees[node])
    return Adamic_adar


def adamic_adar_query(Data_class, hyperedge):
    # 공통 이웃들의 degree에 log씌우고 1에서 나눠서 다 더하기
    Adamic_adar = 0
    for node in hyperedge:
        try:
            if (Data_class.degrees[node] != 1):
                Adamic_adar += 1.0 / np.log(Data_class.degrees[node])
        except:
            continue

    return Adamic_adar


def jaccard_hyper(Data_class, hyperedge):
    try:
        intersect = set(Data_class.neighbors[hyperedge[0]])
        unionset = set()
        for node in hyperedge:
            intersect = set(Data_class.neighbors[node]).intersection(intersect)
            unionset = set(Data_class.neighbors[node]).union(unionset)
    except:
        return 0

    return float(len(intersect)) / len(unionset)


def get_distance(Data_class, hyperedge):
    min_distance = 10
    for i in range(len(hyperedge) - 1):

        for j in range(i + 1, len(hyperedge)):
            try:
                set1 = Data_class.neighbors[hyperedge[i]]
            except:
                return 7

            if hyperedge[j] in set1:
                return 1

            try:
                set2 = Data_class.neighbors[hyperedge[j]]
            except:
                return 7

            difference = set1.intersection(set2)
            if not difference:
                min_distance = 2
                continue

            set1 = get_radius_neighbors(Data_class, set(), hyperedge[i], 1, 2)
            difference = set1.intersection(set2)
            if not difference:
                if min_distance > 3:
                    min_distance = 3
                continue
            set2 = get_radius_neighbors(Data_class, set(), hyperedge[i], 1, 2)
            difference = set1.intersection(set2)
            if not difference:
                if min_distance > 4:
                    min_distance = 4
                continue
            set1 = get_radius_neighbors(Data_class, set(), hyperedge[i], 1, 3)
            difference = set1.intersection(set2)
            if not difference:
                if min_distance > 5:
                    min_distance = 5
                continue
            set2 = get_radius_neighbors(Data_class, set(), hyperedge[i], 1, 3)
            difference = set1.intersection(set2)
            if not difference:
                if min_distance > 6:
                    min_distance = 6
                continue
            else:
                min_distance = 7
                continue

    return min_distance


def cluster_coef(Data_class):
    G = nx.Graph()
    edges = Data_class.edges
    for item in edges.values():
        if len(item) > 1:
            edge = permutations(item, 2)
            G.add_edges_from(edge)
    cluster_nodes = nx.clustering(G)
    return cluster_nodes


def node_closeness(Data_class):
    G = nx.Graph()
    edges = Data_class.edges
    for item in edges.values():
        if len(item) > 1:
            edge = permutations(item, 2)
            G.add_edges_from(edge)
    cluster_nodes = nx.closeness_centrality(G)
    return cluster_nodes