import  csv
from numpy import *
import numpy as np
import csv
import random
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_curve,auc,precision_recall_curve
def ReadCsv(fileName):
    SaveList=[]
    csv_reader = csv.reader(open(fileName))
    for row in csv_reader:
        SaveList.append(list(map(float,row)))
    return SaveList
def SaveCsv(data, fileName):
    with open(fileName, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    return

def loadmodel(modelname):

    if modelname=='RandomForestClassifier':

        model = joblib.load('./model/RandomForestClassifier.auto')

    return model

def shuffle(data, targets):
    data = np.array(data)
    targets = np.array(targets)
    permutation = np.random.permutation(targets.shape[0])
    data = data[permutation, :]
    targets = targets[permutation]
    return data, targets