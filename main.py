import os
from src.data_utils import *
from src.utils import *
import numpy as np
from model import *
import time


if __name__ == "__main__":
    path = os.getcwd() + '/project_data/' + 'paper_author.txt'
    data = Hypergraph(path=path)
    query = Query()

    for i in range(10):
        start =time.time()
        hyper_PA(data, update_iter=500, rejection_type='adamic_adar', threshold=10)
        print("-----PA---", time.time() - start)
        print("-------------")

        start = time.time()
        accuracy, precision, recall, f1_score = evaluate(data, query, predict_method='neighbor', criterion=0.7)
        print("---Metric--- Commone", time.time() - start)
        print(accuracy, precision, recall, f1_score)