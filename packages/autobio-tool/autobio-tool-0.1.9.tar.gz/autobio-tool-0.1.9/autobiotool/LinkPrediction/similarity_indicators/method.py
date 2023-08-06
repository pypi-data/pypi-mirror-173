import similarity_indicators.CommonNeighbor
import similarity_indicators.Salton
import similarity_indicators.Jaccard
import similarity_indicators.Sorenson
import similarity_indicators.HPI
import similarity_indicators.HDI
import similarity_indicators.LHN_I
import similarity_indicators.PA
import similarity_indicators.AA
import similarity_indicators.RA
import similarity_indicators.RWR
def LPmethod(MatrixAdjacency_Train,Method):
    
    
    if Method == 0:
        
        print ('----------Cn----------')
        Matrix_similarity = similarity_indicators.CommonNeighbor.Cn(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 1:
        print ('----------Salton----------')
        Matrix_similarity = similarity_indicators.Salton.Salton(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 2:
        print ('----------Jaccard----------')
        Matrix_similarity = similarity_indicators.Jaccard.Jaccavrd(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 3:
        print ('----------Sorenson----------')
        Matrix_similarity = similarity_indicators.Sorenson.Sorenson(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 4:
        print ('----------HPI----------')
        Matrix_similarity = similarity_indicators.HPI.HPI(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 5:
        print ('----------HDI----------')
        Matrix_similarity = similarity_indicators.HDI.HDI(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 6:
        print ('----------LHN-1----------')
        Matrix_similarity = similarity_indicators.LHN_I.LHN_I(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 7:
        print ('----------PA----------')
        Matrix_similarity = similarity_indicators.PA.PA(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 8:
        print ('----------AA----------')
        Matrix_similarity = similarity_indicators.AA.AA(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 9:
        print ('----------RA----------')
        Matrix_similarity = similarity_indicators.RA.RA(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 10:
       
        print( '----------LP----------')
        Matrix_similarity = similarity_indicators.LP.LP(MatrixAdjacency_Train)
        #valuation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 11:
        print ('----------Katz----------')
        Matrix_similarity = similarity_indicators.Katz.Katz(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 12:
        
        print ('----------ACT----------')
        Matrix_similarity = similarity_indicators.ACT.ACT(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 13:
        print ('----------Cos----------')
        Matrix_similarity = similarity_indicators.Cos.Cos(MatrixAdjacency_Train)
        #Evaluation_Indicators.AUC.Calculation_AUC(MatrixAdjacency_Train, MatrixAdjacency_Test, Matrix_similarity, MaxNodeNum)
    elif Method == 14:
        print ('----------RWR----------')
        Matrix_similarity = similarity_indicators.RWR.RWR(MatrixAdjacency_Train)
        
    
    else:
        print ("Method Error!")
            
            
    return Matrix_similarity