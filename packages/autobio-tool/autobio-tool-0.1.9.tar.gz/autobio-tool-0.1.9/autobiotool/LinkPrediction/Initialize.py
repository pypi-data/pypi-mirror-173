#coding=UTF-8
'''
Created on 2016年11月19日

@author: ZWT
'''
import numpy as np
import time

def Data_Shape(Data):
    List_A = []
    List_B = []
    for row in range(Data.shape[0]):
        List_A.append(Data[row][0])
        List_B.append(Data[row][1])
    List_A = list(set(List_A))
    List_B = list(set(List_B))
    length_A = len(List_A)
    length_B = len(List_B)
 
    MaxNodeNum =  int(max(max(List_A),max(List_B)))+1
    
    return MaxNodeNum
def MatrixAdjacency(MaxNodeNum,Data):
    MatrixAdjacency = np.zeros([MaxNodeNum,MaxNodeNum])
    for col in range(Data.shape[0]):
        i = int(Data[col][0])
        j = int(Data[col][1])
        MatrixAdjacency[i,j] = 1
        MatrixAdjacency[j,i] = 1
    return MatrixAdjacency
def spones(Array):
    for index in range(len(Array)):
        if Array[index] != 0:
            Array[index] = 1
    return Array

def Init(NetFile):
  
    NetData = np.loadtxt(NetFile)
    MaxNodeNum = Data_Shape(NetData)
    MatrixAdjacency_Net = MatrixAdjacency(MaxNodeNum, NetData)
    return MatrixAdjacency_Net,MaxNodeNum
    
def Divide(NetFile,MatrixAdjacency_Net,MaxNodeNum,NetName):
    
    DivideTime_Start = time.clock()
    DivideNum = 0.9
    NetData = np.loadtxt(NetFile)
    permutation = np.random.permutation(NetData.shape[0])
    NetData = NetData[permutation, :]
    TestData = NetData[int(len(NetData)*DivideNum):]
    
    MatrixAdjacency_Train=MatrixAdjacency_Net
    MatrixAdjacency_Test=np.zeros((len(MatrixAdjacency_Net),len(MatrixAdjacency_Net[0])))
    for i in TestData:
            a=int(i[0])
            b=int(i[1])
            MatrixAdjacency_Train[a,b]=0
            MatrixAdjacency_Train[b,a]=0
            MatrixAdjacency_Test[a,b]=1
            MatrixAdjacency_Test[b,a]=1


    
    

   

    DivideTime_End = time.clock()
    
    return MatrixAdjacency_Train,MatrixAdjacency_Test
    
def Init2(Test_File,Train_File):
    print ("DataShape......")
    TrainData = np.loadtxt(Train_File)
    MaxNodeNumTrain = Data_Shape(TrainData)
    TestData = np.loadtxt(Test_File)
    MaxNodeNumTest = Data_Shape(TestData)
    MaxNodeNum = max(MaxNodeNumTrain,MaxNodeNumTest)
    
    MatrixAdjacency_Train = MatrixAdjacency(MaxNodeNum, TrainData)
    MatrixAdjacency_Test = MatrixAdjacency(MaxNodeNum, TestData)
    
    return MatrixAdjacency_Train,MatrixAdjacency_Test,MaxNodeNum


