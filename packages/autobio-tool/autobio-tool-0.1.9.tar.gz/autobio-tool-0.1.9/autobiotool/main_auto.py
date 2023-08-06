from utils import *
from Classifier.Auto import AutoClassifier
data = ReadCsv('feature.csv')
targets = ReadCsv('labels.csv')
targets = [int(i[0]) for i in targets]
data, targets=shuffle(data, targets)

cv = StratifiedKFold(n_splits=5)
aucs=[]
for train, test in cv.split(data, targets):

      
        model = AutoClassifier.fit(data[train], targets[train])
        Testdata=pd.DataFrame(data[test])
        y_prob = model.predict_proba(Testdata)
        y_prob = [i[1] for i in y_prob.values.tolist()]
      
        fpr, tpr, thresholds = roc_curve(targets[test], y_prob)
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
roc_auc=np.mean(aucs) 
print("AUC=",roc_auc)
