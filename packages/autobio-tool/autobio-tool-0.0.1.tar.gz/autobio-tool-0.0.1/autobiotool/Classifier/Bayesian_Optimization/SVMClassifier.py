from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve,auc,precision_recall_curve,accuracy_score
import joblib
import numpy as np
from sklearn.svm import SVC
from bayes_opt import BayesianOptimization
from bayes_opt.util import Colours
random.seed(123)
def rfc_cv(C,gamma, data, targets,optimize_type):
    estimator = SVC(
        C=C,
        gamma=gamma
    )
    cval = cross_val_score(estimator, data, targets,
                           scoring=optimize_type, cv=5)
    return cval.mean()



def Best_Param(data, targets,optimize_type):
    def rfc_crossval(C,gamma):
        return rfc_cv(
            C=C,
            gamma=gamma,
            data=data,
            targets=targets,
            optimize_type=optimize_type,
        )

    optimizer = BayesianOptimization(
        f=rfc_crossval,
        pbounds={
            "C": (0, 100),
            "gamma": (1e-8, 0.99999),
            
        },
        random_state=1234,
        verbose=2
    )
    optimizer.maximize(n_iter=30)
    params=optimizer.max['params']
    modify_para=list(params.values())
    best_param={'C':modify_para[0],
                'gamma':modify_para[1],
                'cache_size':3000,
               }
    print(best_param)
    print(round(optimizer.max['target'],4))
    return best_param




