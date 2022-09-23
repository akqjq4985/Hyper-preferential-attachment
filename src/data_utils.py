import os
from networkx import clustering
import pickle
class Hypergraph():

    def __init__(self, path):
        self.data = {}
        pub = 1
        with open(path, 'r') as f:
            while 1:
                line = f.readline()
                line = line.split(' ')

                if line == ['']:
                    break
                for idx, author in enumerate(line):
                    line[idx] = line[idx].replace('\n', '')
                    line[idx] = int(line[idx])

                if line[1] == 137958:
                    continue

                self.data[pub] = line
                pub += 1

        self.nodes = self.nodes()
        self.edges = self.hyper_edges()
        self.degrees = self.hyper_degrees()
        self.nbd_edgelist = self.hyper_neighbor_edge()
        self.neighbors = self.neighbors()


    def nodes(self):
        node = set()
        for edge in self.data.values():
            for _node in edge:
                node.add(_node)
                if _node == 34157:
                    print(_node)
        return node

    def hyper_edges(self):
        edges = dict()
        for idx, edge in enumerate(self.data.values()):
            edges[idx] = edge
        return edges

    def neighbors(self):
        neighbor_dict = dict()
        for node in self.nodes:
            for edge_idx in self.nbd_edgelist[node]:
                edge = self.edges[edge_idx]
                for i, node_ in enumerate(edge):
                    if node not in neighbor_dict.keys():
                        neighbor_dict[node]=set()
                    neighbor_dict[node].add(node_)

        for node, neighbors in neighbor_dict.items():
            if len(neighbors) > 1:
                neighbors.remove(node)
                neighbor_dict[node] = neighbors
        return neighbor_dict


    def hyper_degrees(self):
        degrees = dict()
        for edge in self.edges.values():
            for node in edge:
                if node not in degrees.keys():
                    degrees[node] = 1
                else:
                    degrees[node] += 1
        return degrees

    def hyper_neighbor_edge(self):
        nbd_edgelist = dict()
        for idx, edge in self.edges.items():
            for node in edge:
                if node not in nbd_edgelist.keys():
                    nbd_edgelist[node] = []
                    nbd_edgelist[node].append(idx)
                else:
                    nbd_edgelist[node].append(idx)
        return nbd_edgelist

    def cluster_coef(self):
        c = clustering(self)
        return c

    def add_edge(self, edge):
        idx = len(self.edges) + 1
        self.edges.update({idx: edge})

        for node in edge:
            self.degrees[node] += 1


        for i in range(len(edge)):
            for j in range(i+1, len(edge)):
                self.neighbors[edge[i]].add(edge[j])
                self.neighbors[edge[j]].add(edge[i])

    def get_authors_publication(self):
        aut_pub = dict()
        for aut_list in self.data.values():
            for aut in aut_list:
                if aut not in aut_pub.keys():
                    aut_pub[aut] = 0
                aut_pub[aut] += 1

        return aut_pub


class Query():

    def __init__(self):
        path1 = os.getcwd() + '/project_data/' + 'query_public.txt'
        path2 = os.getcwd() + '/project_data/' + 'answer_public.txt'

        self.query = []
        self.answer = []

        with open(path1, 'r') as f:
            while 1:
                line = f.readline()
                line = line.split(' ')

                if line == ['']:
                    break

                for idx, author in enumerate(line):
                    line[idx] = line[idx].replace('\n', '')
                    line[idx] = int(line[idx])

                if line == [34479]:
                    continue

                self.query.append(line)

        with open(path2, 'r') as f:
            while 1:
                line = f.readline()

                if line == '':
                    break
                if 'True' in line:
                    self.answer.append(True)
                else:
                    self.answer.append(False)



class Updategraph():

    def __init__(self, path):
        self.data = {}
        pub = 1
        with open(path, 'rb') as f:

            self.data = pickle.load(f)

        self.nodes = self.nodes()
        self.edges = self.hyper_edges()
        self.degrees = self.hyper_degrees()
        self.nbd_edgelist = self.hyper_neighbor_edge()
        self.neighbors = self.neighbors()


    def nodes(self):
        node = set()
        for edge in self.data:
            for _node in edge:
                node.add(_node)
                if _node == 34157:
                    print(_node)
        return node

    def hyper_edges(self):
        edges = dict()
        for idx, edge in enumerate(self.data):
            edges[idx] = edge
        return edges

    def neighbors(self):
        neighbor_dict = dict()
        for node in self.nodes:
            for edge_idx in self.nbd_edgelist[node]:
                edge = self.edges[edge_idx]
                for i, node_ in enumerate(edge):
                    if node not in neighbor_dict.keys():
                        neighbor_dict[node]=set()
                    neighbor_dict[node].add(node_)

        for node, neighbors in neighbor_dict.items():
            if len(neighbors) > 1:
                neighbors.remove(node)
                neighbor_dict[node] = neighbors
        return neighbor_dict


    def hyper_degrees(self):
        degrees = dict()
        for edge in self.edges.values():
            for node in edge:
                if node not in degrees.keys():
                    degrees[node] = 1
                else:
                    degrees[node] += 1
        return degrees

    def hyper_neighbor_edge(self):
        nbd_edgelist = dict()
        for idx, edge in self.edges.items():
            for node in edge:
                if node not in nbd_edgelist.keys():
                    nbd_edgelist[node] = []
                    nbd_edgelist[node].append(idx)
                else:
                    nbd_edgelist[node].append(idx)
        return nbd_edgelist

    def cluster_coef(self):
        c = clustering(self)
        return c

    def add_edge(self, edge):
        idx = len(self.edges) + 1
        self.edges.update({idx: edge})

        for node in edge:
            self.degrees[node] += 1


        for i in range(len(edge)):
            for j in range(i+1, len(edge)):
                self.neighbors[edge[i]].add(edge[j])
                self.neighbors[edge[j]].add(edge[i])

    def get_authors_publication(self):
        aut_pub = dict()
        for aut_list in self.data:
            for aut in aut_list:
                if aut not in aut_pub.keys():
                    aut_pub[aut] = 0
                aut_pub[aut] += 1

        return aut_pub