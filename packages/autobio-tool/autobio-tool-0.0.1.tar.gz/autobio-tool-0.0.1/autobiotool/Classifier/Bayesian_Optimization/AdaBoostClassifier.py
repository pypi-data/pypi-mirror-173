from sklearn.ensemble import AdaBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import roc_curve,auc,precision_recall_curve,accuracy_score
import joblib
import numpy as np
from bayes_opt import BayesianOptimization
from bayes_opt.util import Colours
random.seed(123)

def Classifier_cv(n_estimators, learning_rate, data, targets,optimize_type):
    estimator = AdaBoostClassifier(
        n_estimators=n_estimators,
        learning_rate=learning_rate,
      
        n_jobs=-1,
    )
    cval = cross_val_score(estimator, data, targets,
                           scoring=optimize_type, cv=5)
    return cval.mean()



def Best_Param(data, targets,optimize_type):
    def rfc_crossval(n_estimators, learning_rate):
        return Classifier_cv(
            n_estimators=int(n_estimators),
            
            learning_rate=learning_rate,
            data=data,
            targets=targets,
            optimize_type=optimize_type,
        )

    optimizer = BayesianOptimization(
        f=rfc_crossval,
        pbounds={
            "n_estimators": (10, 300),
            "learning_rate":(0,1.0),
        },
       
        verbose=2
    )
    optimizer.maximize(n_iter=30)
    params=optimizer.max['params']
    modify_para=list(params.values())
    best_param={
                'n_estimators':int(modify_para[0]),
                'learning_rate':round(modify_para[1],3),
                'n_jobs':-1,
               }
    print(best_param)
    print(round(optimizer.max['target'],4))
    return best_param





