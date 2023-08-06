from  xgboost import XGBClassifier
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
def Classifier_cv(n_estimators, gamma, subsample,colsample_bytree, data, targets,optimize_type):
    estimator = XGBClassifier(
        n_estimators=n_estimators,
        gamma=round(gamma,3),
        subsample=round(subsample,3),
        colsample_bytree=round(colsample_bytree,3),
        use_label_encoder=False,
        eval_metric=['logloss','auc','error'],
      
      
    )
    cval = cross_val_score(estimator, data, targets,
                           scoring=optimize_type, cv=5)
    return cval.mean()



def Best_Param(data, targets,optimize_type):
    def rfc_crossval(n_estimators, gamma, subsample,colsample_bytree):
        return Classifier_cv(
            n_estimators=int(n_estimators),
            gamma=max(min(gamma, 0.2), 1e-2),
            subsample=max(min(subsample, 0.9), 0.6),
            colsample_bytree=max(min(colsample_bytree, 0.9), 0.6),
           
            data=data,
            targets=targets,
            optimize_type=optimize_type,
        )

    optimizer = BayesianOptimization(
        f=rfc_crossval,
        pbounds={
            "n_estimators": (10, 999),
            "gamma": (0.01, 0.2),
            "subsample": (0.6, 0.9),
            "colsample_bytree": (0.6, 0.9),
           
        },
       
        verbose=2
    )
    optimizer.maximize(n_iter=2)
    params=optimizer.max['params']
    modify_para=list(params.values())
    best_param={
                
                'n_estimators':int(modify_para[0]),
                'gamma':round(modify_para[1],3),
                'subsample':round(modify_para[2],3),
                'colsample_bytree':round(modify_para[3],3),  
                'use_label_encoder':False,
                'eval_metric':['logloss','auc','error'],          
               }
    print(best_param)
    print(round(optimizer.max['target'],4))
    return best_param






