import os
import pandas as pd
from src.utils import *
from src.data_utils import *

path = os.getcwd() + '/project_data/' + 'paper_author.txt'
data = Hypergraph(path=path)
# path = 'save_graph/' + '15000th10threshold.txt'
# data = Updategraph(path=path)

query = Query()


Degree_difference = []
Max_degree = []
Avg_degree = []
MIN_distance = []
Avg_cluster_coef = []
Avg_jaccard = []
Hyper_jaccard = []
Adamic_adar = []

# Max_closeness = []
# Avg_closeness = []

# node_close = node_closeness(data)  # dict : node -> value
cluster_coefficient = cluster_coef(data)  # dict : node -> value

for i in range(len(query.query)):

    degs = []
    # clsness = []
    cls_coef = []
    for node in query.query[i]:
        try:
            # clsness.append(node_close[node])
            cls_coef.append(cluster_coefficient[node])

        except:
            # clsness.append(0)
            cls_coef.append(0)

        try:
            degs.append(data.degrees[node])
        except:
            degs.append(0)

    # Max_closeness.append(max(clsness))
    # Avg_closeness.append(np.average(clsness))
    Avg_cluster_coef.append(np.average(cls_coef))
    Max_degree.append(max(degs))
    Degree_difference.append(max(degs) - min(degs))
    Avg_degree.append(np.average(degs))

    min_dist = get_distance(Data_class=data, hyperedge=query.query[i])
    MIN_distance.append(min_dist)

    Hyper_jaccard.append(jaccard_hyper(Data_class=data, hyperedge=query.query[i]))
    Avg_jaccard.append(averaged_jaccard_similarity(Data_class=data, edge=query.query[i]))
    Adamic_adar.append(adamic_adar_query(data, query.query[i]))

    if i % 500 == 0:
        print(i, "th")


print(MIN_distance)