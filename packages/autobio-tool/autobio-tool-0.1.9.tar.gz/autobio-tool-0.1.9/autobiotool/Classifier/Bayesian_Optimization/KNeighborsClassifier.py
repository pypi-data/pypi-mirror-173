from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve,auc,precision_recall_curve,accuracy_score
import numpy as np
from bayes_opt import BayesianOptimization
from bayes_opt.util import Colours
import random
random.seed(123)
def Classifier_cv(n_neighbors, p,  data, targets,optimize_type):
    estimator = KNeighborsClassifier(
        n_neighbors=n_neighbors,
        p=p,

    
    )
    cval = cross_val_score(estimator, data, targets,
                           scoring=optimize_type, cv=5)
    return cval.mean()



def Best_Param(data, targets,optimize_type):
    def rfc_crossval(n_neighbors, p):
        return Classifier_cv(
            n_neighbors=int(n_neighbors),
            p=int(p),
        
            data=data,
            targets=targets,
            optimize_type=optimize_type,
        )

    optimizer = BayesianOptimization(
        f=rfc_crossval,
        pbounds={
            "n_neighbors": (2, 10),
            "p": (1, 4),
          
        },
       
        verbose=2
    )
    optimizer.maximize(n_iter=2)
    params=optimizer.max['params']
    modify_para=list(params.values())
    best_param={
                
                'n_neighbors':int(modify_para[0]),
                'p':int(modify_para[1]),
                'n_jobs':-1,
               }
    print(best_param)
    print(round(optimizer.max['target'],4))
    return best_param






