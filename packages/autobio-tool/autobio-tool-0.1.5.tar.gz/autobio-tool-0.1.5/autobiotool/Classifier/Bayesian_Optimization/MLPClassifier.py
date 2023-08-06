from sklearn.neural_network import MLPClassifier
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
def Classifier_cv( learning_rate_init, alpha, data, targets,optimize_type):
    estimator = MLPClassifier(
   
        learning_rate_init=learning_rate_init,
        alpha=alpha,
       
    )
    cval = cross_val_score(estimator, data, targets,
                           scoring=optimize_type, cv=5)
    return cval.mean()



def Best_Param(data, targets,optimize_type):
    def rfc_crossval(learning_rate_init, alpha):
        return Classifier_cv(
            
            learning_rate_init=max(min(learning_rate_init, 1e-4), 1e-7),
            alpha=max(min(alpha, 1e-4), 1e-7),
            data=data,
            targets=targets,
            optimize_type=optimize_type,
        )

    optimizer = BayesianOptimization(
        f=rfc_crossval,
        pbounds={
            
            "learning_rate_init": (1e-7, 1e-4),
            "alpha": (1e-7, 1e-4),
        },
       
        verbose=2
    )
    optimizer.maximize(n_iter=2)
    params=optimizer.max['params']
    modify_para=list(params.values())
    best_param={
                'learning_rate_init':int(modify_para[0]),
                'alpha':round(modify_para[1],3),
               }
    print(best_param)
    print(round(optimizer.max['target'],4))
    return best_param






