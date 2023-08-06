from catboost import CatBoostClassifier
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
def Classifier_cv(n_estimators, learning_rate, iterations,data, targets,optimize_type):
    estimator = CatBoostClassifier(
        n_estimators=n_estimators,
        learning_rate=round(learning_rate,3),
        iterations=iterations,

      
      
    )
    cval = cross_val_score(estimator, data, targets,
                           scoring=optimize_type, cv=5)
    return cval.mean()



def Best_Param(data, targets,optimize_type):
    def rfc_crossval(n_estimators, learning_rate,iterations):
        return Classifier_cv(
            n_estimators=int(n_estimators),
            learning_rate=max(min(learning_rate, 0.3), 1e-8),
            iterations=int(iterations),
            data=data,
            targets=targets,
            optimize_type=optimize_type,
        )

    optimizer = BayesianOptimization(
        f=rfc_crossval,
        pbounds={
            "n_estimators": (10, 999),
            "learning_rate": (0, 0.3),
            "iterations": (100, 9999),
           
        },
       
        verbose=2
    )
    optimizer.maximize(n_iter=2)
    params=optimizer.max['params']
    modify_para=list(params.values())
    best_param={
                
                'n_estimators':int(modify_para[0]),
                'learning_rate':round(modify_para[1],3),
                'iterations':int(modify_para[2]),         
               }
    print(best_param)
    print(round(optimizer.max['target'],4))
    return best_param

