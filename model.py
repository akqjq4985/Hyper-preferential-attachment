import numpy as np
import random
from src.utils import *
from matplotlib import pyplot as plt


def hyper_PA(Data_class, update_iter=1000, mu=3, rejection_type='jaccard', threshold = 0):
    def calculate_prob(degrees):
        prob = dict()
        deg_sum = np.sum([deg for deg in degrees.values()])
        for node, degree in degrees.items():
            prob[node] = degree / deg_sum
        return prob

    if rejection_type is None:
        similarity_measure = no_similarity
    elif rejection_type == 'jaccard':
        similarity_measure = radius_jaccard
    elif rejection_type == 'adamic_adar':
        similarity_measure = adamic_adar
    random.seed(70)
    # time_sequence = list(np.random.poisson(mu, update_iter))
    degree_dist = [len(edge) for edge in Data_class.edges.values()]
    max_length = max(degree_dist)
    degree_dist = plt.hist(degree_dist, bins=max(degree_dist))[0]
    degree_dist = degree_dist/sum(degree_dist)
    time_sequence = list(random.choices(list(range(1, max_length+1)), weights=list(degree_dist), k=update_iter))

    ## select m node
    for iteration, num_add_node in enumerate(time_sequence):
        if num_add_node == 0:
            num_add_node += 1
        elif num_add_node > 5:
            num_add_node = 5

        node_choices = random.choices(list(Data_class.nodes), k=1)
        p = calculate_prob(Data_class.degrees)

        for node1 in node_choices:
            i=0
            
            while 1:
                    
                new_edge = [node1] + list(random.choices(list(p.keys()), weights=list(p.values()), k=num_add_node))

                edge_similarity = similarity_measure(Data_class, new_edge)
                # print(new_edge)
                if (new_edge not in Data_class.edges.values()) & (edge_similarity > threshold):
                    Data_class.add_edge(new_edge)
                    break
                i+=1
                if i>20:
                    break
            ## in addition to adding edge, other self feature should be updated.
            ## have to restrict the maximum length of hyper edges
            ## 2-hop
        if iteration%10== 0:
            print(iteration, "th iteration")




def hyper_PA2(Data_class, update_iter=1000, mu=3, rejection_type = 'jaccard', threshold = 0):
    def calculate_prob(degrees):
        prob = dict()
        deg_sum = np.sum([deg for deg in degrees.values()])
        for node, degree in degrees.items():
            prob[node] = degree / deg_sum
        return prob

    if rejection_type is None:
        similarity_measure = no_similarity
    elif rejection_type == 'jaccard':
        similarity_measure = radius_jaccard
    elif rejection_type == 'adamic_adar':
        similarity_measure = adamic_adar

    time_sequence = list(np.random.poisson(mu, update_iter))

    ## select m node
    for iteration, num_add_node in enumerate(time_sequence):
        if num_add_node == 0:
            num_add_node += 1
        elif num_add_node > 5:
            num_add_node = 6
        node_choices = random.choices(list(Data_class.nodes), k=1)
        neighbor = Data_class.neighbors[node_choices[0]]
        neighbor = neighbor | set(node_choices)

        professor_degree = max([Data_class.degrees[nb] for nb in neighbor])
        professor = [nb for nb in neighbor if Data_class.degrees[nb]==professor_degree][0]




        p = calculate_prob(Data_class.degrees)

        for node1 in node_choices:
            while 1:

                new_edge = [node1] + list(random.choices(list(p.keys()), weights=list(p.values()), k=num_add_node))

                edge_similarity = similarity_measure(Data_class, new_edge)
                # print(edge_similarity)
                # print(new_edge)
                if (new_edge not in Data_class.edges.values()) & (edge_similarity > threshold):

                    Data_class.add_edge(new_edge)
                    break

            ## in addition to adding edge, other self feature should be updated.
            ## have to restrict the maximum length of hyper edges
            ## 2-hop
        if iteration%1000 == 0:
            print(iteration, "th iteration")

def predict(Graph, edge, method='common_edge', criterion = 0.3):

    if method == 'common_edge':
        for edge_ in Graph.edges.values():

            jaccard = len(set(edge)&set(edge_))/len(set(edge)|set(edge_))
            if jaccard >= criterion:
                pred = True
                break
            else:
                pred = False

    elif method =='neighbor':
        cnt = 0
        for i in range(len(edge)):
            for j in range(i+1, len(edge)):
                try:
                    edge[j] in Graph.neighbors[edge[i]]
                    cnt += 1
                except:
                    continue

        if cnt >= len(edge)-1:
            pred = True
        else:
            pred = False

    return pred

def evaluate(Graph, Query, predict_method='common_edge', criterion=0.3):

    tp = tn = fp = fn = 0

    for i in range(len(Query.query)):

        pred = predict(Graph, Query.query[i], method=predict_method, criterion=criterion)

        if (Query.answer[i] == True) & (pred == True):
            tp += 1
        elif (Query.answer[i] == True) & (pred == False):
            fn += 1
        elif (Query.answer[i] == False) & (pred == True):
            fp += 1
        elif (Query.answer[i] == False) & (pred == False):
            tn += 1

    accuracy = (tp+tn) / (len(Query.query))
    precision = tp / (tp+fp)
    recall = tp / (tp+tn)
    f1 = 2*precision*recall/(precision+recall)
    return accuracy, precision, recall, f1


