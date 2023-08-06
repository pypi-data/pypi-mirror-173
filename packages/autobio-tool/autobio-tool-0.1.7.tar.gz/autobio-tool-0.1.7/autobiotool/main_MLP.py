#177497
from utils import *
from Classifier.Genetic_Algorithm.MLPClassifier import *
random.seed(123)
data = ReadCsv('feature.csv')
targets = ReadCsv('labels.csv')
targets = [int(i[0]) for i in targets]
data, targets=shuffle(data, targets)
optimize_type=['accuracy','f1','precision','recall','roc_auc']
best_param=Best_Param(data, targets,optimize_type[4])
model = MLPClassifier(**best_param)

roc_auc = cross_val_score(model, data, targets,scoring='roc_auc', cv=5)
print("AUC=",roc_auc.mean())
