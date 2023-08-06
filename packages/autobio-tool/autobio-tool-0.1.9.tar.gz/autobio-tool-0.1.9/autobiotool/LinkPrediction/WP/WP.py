import numpy as np

def is_invertible(a):

     return a.shape[0] == a.shape[1] and np.linalg.matrix_rank(a) == a.shape[0]

def C_(A,alpha,p):
  
    
 
    AAT=A@A.conj().T  
     
    Matrix_EYE = np.eye(A.shape[0])
    Temp = (1/alpha) *Matrix_EYE + AAT
    if  is_invertible(Temp):
        INV_Temp = np.linalg.inv(Temp)
    else:
        Temp[Temp == 0]=1e-12
        
        INV_Temp = np.linalg.inv(Temp)   

    C=AAT@INV_Temp    
    
    
    S=C@A
    
    Num=int(np.sum(A==1)/2*p)
    


    
    S_=[]
    
    for i in S:
        
        S_.extend(i)
    

    
    S_sort=np.sort(S_)
    
    Key=S_sort[-Num]
    
    S[S>=Key]=1
    S[S<Key]=0
    
    
    return S



def C(A,alpha):
  
    
 
    AAT=A@A.conj().T  
     
    Matrix_EYE = np.eye(A.shape[0])
    Temp = (1/alpha) *Matrix_EYE + AAT
    if  is_invertible(Temp):
        INV_Temp = np.linalg.inv(Temp)
    else:
        Temp[Temp == 0]=1e-12
        
        INV_Temp = np.linalg.inv(Temp)   

    C=AAT@INV_Temp    
    
    
    S=C@A
    
    return S




def LRTM(A,alpha,beta):
    maxiter=30
    m=len(A)
    n=len(A[0])
    
    
    A=np.array(A)
    W1 = np.random.rand(m,m)
    W2 = np.random.rand(n,n)
    k=1
    
 
    
    
    
    
   
   
    
    AAT=A@A.conj().T  
    ATA=A.conj().T@A
    
    
    
    
    for i in range(maxiter):
        
       
        W1=W1*AAT/((W1@A+A@W2)@A.conj().T+alpha*W1)
        W2=W2*ATA/(A.conj().T@(W1@A+A@W2)+beta*W2)
        
        
       
        W1[W1 == 0]=1e-12
        W2[W2 == 0]=1e-12
       

        
    
    
    S=W1@A+A@W2
    
    return S