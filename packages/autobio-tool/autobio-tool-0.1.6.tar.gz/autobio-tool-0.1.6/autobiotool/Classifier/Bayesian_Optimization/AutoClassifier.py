import AdaBoostClassifier,CatBoostClassifier,KNeighborsClassifier,LightGBMClassifier,MLPClassifier,RandomForestClassifier,SVMClassifier,XGBClassifier
from sklearn.ensemble import AdaBoostClassifier as AdaBoost
from catboost import CatBoostClassifier as CatBoost
from catboost import  Pool
from sklearn.neighbors import KNeighborsClassifier as KNeighbors
from lightgbm import LGBMClassifier as LGBM
from sklearn.neural_network import MLPClassifier as MLP
from sklearn.ensemble import RandomForestClassifier as RandomForest
from sklearn.svm import SVC 
from  xgboost import XGBClassifier as XGB

from sklearn.model_selection import StratifiedKFold
import joblib
PATH='./AutoClassifierModel'
def k_fold_Bagging(data, targets,best_param,Flag,k):
    try:
        os.mkdir(PATH+'/'+Flag)
    except:
        pass
    cv = StratifiedKFold(n_splits=k)
    NUM=0
    for train, test in cv.split(data, targets):

        if Flag=='ada':
            model = AdaBoost(**best_param)
        if Flag=='cat':
            model = CatBoost(**best_param)
        if Flag=='knn':
            model = KNeighbors(**best_param) 
        if Flag=='gbm':
            model = LGBM(**best_param)
        if Flag=='mlp':
            model = MLP(**best_param)
        if Flag=='rf':
            model = RandomForest(**best_param)
        if Flag=='svm':
            model = SVC(**best_param)
        if Flag=='xg':
            model = XGB(**best_param)


        x_train=data[train]
        x_test = data[test]
        y_train=targets[train]
        y_test=targets[test]

        model.fit(x_train, y_train)

        if Flag=='ada':
            joblib.dump(model, PATH+'/'+Flag+'/'+str(NUM)+'.auto')
        if Flag=='cat':
         
            model.save_model(PATH+'/'+Flag+'/'+str(NUM)+'.auto')
        if Flag=='knn':
            joblib.dump(model, PATH+'/'+Flag+'/'+str(NUM)+'.auto')
        if Flag=='gbm':
            joblib.dump(model, PATH+'/'+Flag+'/'+str(NUM)+'.auto')
        if Flag=='mlp':
            joblib.dump(model, PATH+'/'+Flag+'/'+str(NUM)+'.auto')
        if Flag=='rf':
            joblib.dump(model, PATH+'/'+Flag+'/'+str(NUM)+'.auto')
        if Flag=='svm':
            joblib.dump(model, PATH+'/'+Flag+'/'+str(NUM)+'.auto')
        if Flag=='xg':
            
            model.save_model(PATH+'/'+Flag+'/'+str(NUM)+'.auto')


        joblib.dump(model, PATH+'/'+Flag+'/'+str(NUM)+'.auto')


    
def Stack_Ensembling(data, targets,k):

    Ensemble=[]
    List=['ada','cat','knn','gbm','mlp','rf','svm','xg']

    for Flag in List:
        part=[]
        for NUM in range(k):
            if Flag=='ada':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='cat':
                model=CatBoost
                model.load_model(PATH+'/'+Flag+'/'+str(NUM)+'.auto')
            if Flag=='knn':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='gbm':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='mlp':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='rf':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='svm':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='xg':
                model = XGB
                model.load_model(PATH+'/'+Flag+'/'+str(NUM)+'.auto')
   
            prob=model.predict_proba(data)[:, 1]
            part.append(prob)

        Ensemble.append(part)


        feature=[]
        for kk in range(len(targets)):
            part=[]
            for ii in Ensemble:

                for jj in ii:
                    part.append(jj[kk])

        
            feature.append(part)

        
    x_train, x_val, y_train, y_val = train_test_split(feature, targets, test_size=0.2)
    train_pool = Pool(x_train,y_train)
    val_pool = Pool(x_val, y_val)

    model  = CatBoostClassifier(task_type='CPU',use_best_model=True,loss_function='MultiClass',custom_loss=['Recall', 'Accuracy'],eval_metric='Accuracy')

    model.fit(train_pool, eval_set=val_pool,use_best_model=True, silent=False,plot=False)

    model.save_model(PATH+'/Stack_Ensembling/cat.auto')




def fit(data, targets,optimize_type,k):

    try:
        os.mkdir(PATH)
    except:
        pass
    adaboost_best_param=AdaBoostClassifier.Best_Param(data, targets,optimize_type)
    catboost_best_param=CatBoostClassifier.Best_Param(data, targets,optimize_type)
    KNN_best_param=KNeighborsClassifier.Best_Param(data, targets,optimize_type)
    lightGBM_best_param=LightGBMClassifier.Best_Param(data, targets,optimize_type)
    MLP_best_param=MLPClassifier.Best_Param(data, targets,optimize_type)
    RF_best_param=RandomForestClassifier.Best_Param(data, targets,optimize_type)
    SVM_best_param=SVMClassifier.Best_Param(data, targets,optimize_type)
    xgboost_best_param=XGBClassifier.Best_Param(data, targets,optimize_type)

    k_fold_Bagging(data, targets,adaboost_best_param,'ada',k)
    k_fold_Bagging(data, targets,catboost_best_param,'cat',k)
    k_fold_Bagging(data, targets,KNN_best_param,'knn',k)
    k_fold_Bagging(data, targets,lightGBM_best_param,'gbm',k)
    k_fold_Bagging(data, targets,MLP_best_param,'mlp',k)
    k_fold_Bagging(data, targets,RF_best_param,'rf',k)
    k_fold_Bagging(data, targets,SVM_best_param,'svm',k)
    k_fold_Bagging(data, targets,xgboost_best_param,'xg',k)

    Stack_Ensembling(data, targets,k)

def predict_proba(data):

    Ensemble=[]
    List=['ada','cat','knn','gbm','mlp','rf','svm','xg']

    for Flag in List:
        part=[]
        for NUM in range(k):
            if Flag=='ada':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='cat':
                model=CatBoost
                model.load_model(PATH+'/'+Flag+'/'+str(NUM)+'.auto')
            if Flag=='knn':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='gbm':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='mlp':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='rf':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='svm':
                model = joblib.load(PATH+'/'+Flag+'/'+str(NUM)+'.auto') 
            if Flag=='xg':
                model = XGB
                model.load_model(PATH+'/'+Flag+'/'+str(NUM)+'.auto')
   
            prob=model.predict_proba(data)[:, 1]
            part.append(prob)

        Ensemble.append(part)


        feature=[]
        for kk in range(len(data)):
            part=[]
            for ii in Ensemble:

                for jj in ii:
                    part.append(jj[kk])

        
            feature.append(part)


        model = CatBoost()
        model.load_model(PATH+'/'+Flag+'/'+str(NUM)+'.auto')
        prob = model.predict_proba(feature)

        return prob