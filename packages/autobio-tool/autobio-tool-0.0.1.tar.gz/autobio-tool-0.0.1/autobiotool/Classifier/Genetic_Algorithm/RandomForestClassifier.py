# -*- coding: utf-8 -*-
from sklearn.ensemble import RandomForestClassifier
import geatpy as ea 
import numpy as np
import geatpy as ea
from sklearn import svm
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from multiprocessing.dummy import Pool as ThreadPool
import random
random.seed(123)
class MyProblem(ea.Problem): 
    def __init__(self,datas,data_targets,optimize_type):
        name = 'MyProblem' 
        
        M = 1
        maxormins = [-1] 
        Dim = 2 
        varTypes = [0, 0] 
        lb = [2**(-8)] * Dim 
        ub = [2**8] * Dim
        lbin = [1] * Dim 
        ubin = [1] * Dim       
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
     
        
        self.data = datas 
        self.dataTarget = data_targets
        self.optimize_type = optimize_type
    
    def aimFunc(self, pop): 
        Vars = pop.Phen 
        pop.ObjV = np.zeros((pop.sizes, 1)) 
        def subAimFunc(i):
            n_estimators = Vars[i, 0]
            min_samples_split = Vars[i, 1]
            max_features = Vars[i, 2]


            model = RandomForestClassifier(
                                n_estimators=int(n_estimators),
                                min_samples_split=int(min_samples_split),
                                max_features=max_features,
                                n_jobs=-1,
                            )
            model.fit(self.data, self.dataTarget) 
            scores = cross_val_score(model, self.data, self.dataTarget, scoring=self.optimize_type,cv=5) 
            pop.ObjV[i] = scores.mean() 
        pool = ThreadPool(2) 
        pool.map(subAimFunc, list(range(pop.sizes)))
   




def Best_Param(datas,data_targets,optimize_type):


    problem = MyProblem(datas,data_targets,optimize_type) 


    Encoding = 'RI'       
    NIND = 2    

    n_estimators = [10,999] 
    min_samples_split = [2,100] 
    max_features = [0.1,1.0] 

    b1 = [1, 1] 
    b2 = [1, 1] 
    b3 = [1, 1]
    

  
    ranges=np.vstack([ n_estimators, min_samples_split, max_features]).T
  
    borders=np.vstack([b1, b2, b3]).T
    varTypes = np.array([0, 0, 0]) 



    Field = ea.crtfld(Encoding, varTypes, ranges, borders) 
    population = ea.Population(Encoding, Field, NIND) 
    
    myAlgorithm = ea.soea_DE_rand_1_bin_templet(problem, population) 
    myAlgorithm.MAXGEN = 10 
    myAlgorithm.trappedValue = 1e-6 
    myAlgorithm.maxTrappedCount = 10 
    myAlgorithm.logTras = 1  
    myAlgorithm.verbose = True  
    myAlgorithm.drawing = 1  

    [BestIndi, population] = myAlgorithm.run()  
    BestIndi.save()  
 
    print('Timed：%f s' % myAlgorithm.passTime)
    
    if BestIndi.sizes != 0:
        print('The optimal objective function value is:%s' % BestIndi.ObjV[0][0])
        print('The optimal parameter value is:')
        for i in range(BestIndi.Phen.shape[1]):
            print(BestIndi.Phen[0, i])
    else:
        print('No feasible solution was found.')


    best_param={'n_estimators':int(BestIndi.Phen[0][0]),
                'min_samples_split':int(BestIndi.Phen[0][1]),
                'max_features':BestIndi.Phen[0][2],
                'n_jobs':-1,
                
               }
    return best_param