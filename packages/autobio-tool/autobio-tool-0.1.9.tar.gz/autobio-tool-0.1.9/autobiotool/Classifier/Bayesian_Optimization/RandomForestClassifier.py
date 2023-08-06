from sklearn.ensemble import RandomForestClassifier
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
def Classifier_cv(n_estimators, min_samples_split, max_features, data, targets,optimize_type):
    estimator = RandomForestClassifier(
        n_estimators=n_estimators,
        min_samples_split=min_samples_split,
        max_features=max_features,
        n_jobs=-1,
    )
    cval = cross_val_score(estimator, data, targets,
                           scoring=optimize_type, cv=5)
    return cval.mean()



def Best_Param(data, targets,optimize_type):
    def rfc_crossval(n_estimators, min_samples_split, max_features):
        return Classifier_cv(
            n_estimators=int(n_estimators),
            min_samples_split=int(min_samples_split),
            max_features=max(min(max_features, 0.999), 1e-3),
            data=data,
            targets=targets,
            optimize_type=optimize_type,
        )

    optimizer = BayesianOptimization(
        f=rfc_crossval,
        pbounds={
            "n_estimators": (10, 999),
            "min_samples_split": (2, 100),
            "max_features": (0.1, 1.0),
        },
       
        verbose=2
    )
    optimizer.maximize(n_iter=2)
    params=optimizer.max['params']
    modify_para=list(params.values())
    best_param={
                
                'n_estimators':int(modify_para[0]),
                'min_samples_split':int(modify_para[1]),
                'max_features':round(modify_para[2],3),
                'n_jobs':-1,
               }
    print(best_param)
    print(round(optimizer.max['target'],4))
    return best_param






