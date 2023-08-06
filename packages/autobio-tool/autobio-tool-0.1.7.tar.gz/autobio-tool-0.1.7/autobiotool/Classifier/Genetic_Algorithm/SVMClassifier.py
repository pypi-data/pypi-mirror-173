# -*- coding: utf-8 -*-

import geatpy as ea 
import numpy as np
import geatpy as ea
from sklearn import svm
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from multiprocessing.dummy import Pool as ThreadPool
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
            C = Vars[i, 0]
            G = Vars[i, 1]
            svc = svm.SVC(C=C, kernel='rbf', gamma=G).fit(self.data, self.dataTarget) 
            scores = cross_val_score(svc, self.data, self.dataTarget, scoring=self.optimize_type,cv=5) 
            pop.ObjV[i] = scores.mean() 
        pool = ThreadPool(2) 
        pool.map(subAimFunc, list(range(pop.sizes)))
   




def Best_Param(datas,data_targets,optimize_type):


    problem = MyProblem(datas,data_targets,optimize_type) 


    Encoding = 'RI'       
    NIND = 2             
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) 
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


    best_param={'C':BestIndi.Phen[0][0],
                'gamma':BestIndi.Phen[0][1],
                'cache_size':3000,
               }
    return best_param