# -*- coding: utf-8 -*-

import geatpy as ea 
import numpy as np
import geatpy as ea
from sklearn import svm
from sklearn import preprocessing
from sklearn.model_selection import cross_val_score
from multiprocessing.dummy import Pool as ThreadPool
class MyProblem(ea.Problem): # 继承Problem父类
    def __init__(self,datas,data_targets,optimize_type):
        name = 'MyProblem' # 初始化name（函数名称，可以随意设置）
        M = 1 # 初始化M（目标维数）
        maxormins = [-1] # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = 2 # 初始化Dim（决策变量维数）
        varTypes = [0, 0] # 初始化varTypes（决策变量的类型，元素为0表示对应的变量是连续的；1表示是离散的）
        lb = [2**(-8)] * Dim # 决策变量下界
        ub = [2**8] * Dim # 决策变量上界
        lbin = [1] * Dim # 决策变量下边界（0表示不包含该变量的下边界，1表示包含）
        ubin = [1] * Dim # 决策变量上边界（0表示不包含该变量的上边界，1表示包含）
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, M, maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        # 目标函数计算中用到的一些数据
        
        self.data = datas # 训练集的特征数据（归一化）
        self.dataTarget = data_targets
        self.optimize_type = optimize_type
    
    def aimFunc(self, pop): # 目标函数，采用多线程加速计算
        Vars = pop.Phen # 得到决策变量矩阵
        pop.ObjV = np.zeros((pop.sizes, 1)) # 初始化种群个体目标函数值列向量
        def subAimFunc(i):
            C = Vars[i, 0]
            G = Vars[i, 1]
            svc = svm.SVC(C=C, kernel='rbf', gamma=G).fit(self.data, self.dataTarget) # 创建分类器对象并用训练集的数据拟合分类器模型
            scores = cross_val_score(svc, self.data, self.dataTarget, scoring=self.optimize_type,cv=5) # 计算交叉验证的得分
            pop.ObjV[i] = scores.mean() # 把交叉验证的平均得分作为目标函数值
        pool = ThreadPool(2) # 设置池的大小
        pool.map(subAimFunc, list(range(pop.sizes)))
    
    def test(self, C, G): # 代入优化后的C、Gamma对测试集进行检验
        # 读取测试集数据
        fp = open('iris_test.data')
        datas = []
        data_targets = []
        for line in fp.readlines():
            line_data = line.strip('\n').split(',')
            data = []
            for i in line_data[0:4]:
                data.append(float(i))
            datas.append(data)
            data_targets.append(line_data[4])
        fp.close()
        data_test = preprocessing.scale(np.array(datas)) # 测试集的特征数据（归一化）
        dataTarget_test = np.array(data_targets) # 测试集的标签数据
        svc = svm.SVC(C=C, kernel='rbf', gamma=G).fit(self.data, self.dataTarget) # 创建分类器对象并用训练集的数据拟合分类器模型
        dataTarget_predict = svc.predict(data_test) # 采用训练好的分类器对象对测试集数据进行预测
        print("测试集数据分类正确率 = %s%%"%(len(np.where(dataTarget_predict == dataTarget_test)[0]) / len(dataTarget_test) * 100))




def Best_Param(datas,data_targets,optimize_type):


    """===============================实例化问题对象==========================="""
    problem = MyProblem(datas,data_targets,optimize_type) # 生成问题对象


    """=================================种群设置==============================="""
    Encoding = 'RI'       # 编码方式
    NIND = 2             # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_DE_rand_1_bin_templet(problem, population) # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 10 # 最大进化代数
    myAlgorithm.trappedValue = 1e-6 # “进化停滞”判断阈值
    myAlgorithm.maxTrappedCount = 10 # 进化停滞计数器最大上限值，如果连续maxTrappedCount代被判定进化陷入停滞，则终止进化
    myAlgorithm.logTras = 1  # 设置每隔多少代记录日志，若设置成0则表示不记录日志
    myAlgorithm.verbose = True  # 设置是否打印输出日志信息
    myAlgorithm.drawing = 1  # 设置绘图方式（0：不绘图；1：绘制结果图；2：绘制目标空间过程动画；3：绘制决策空间过程动画）
    """===========================调用算法模板进行种群进化======================="""
    [BestIndi, population] = myAlgorithm.run()  # 执行算法模板，得到最优个体以及最后一代种群
    BestIndi.save()  # 把最优个体的信息保存到文件中
    """==================================输出结果============================="""
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