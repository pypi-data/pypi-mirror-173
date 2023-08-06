from datetime import time
from autobiotool.utils import *
import sklearn
from autogluon.tabular import  TabularPredictor
random.seed(123)

def fit(data, targets):
    
    label=len(data[0])
    save_path = './model/auto/' 
    y_train=[[i] for i in targets]
    Train=np.hstack((data,y_train))
    train_data = pd.DataFrame(Train)
    model = TabularPredictor(label=label, path=save_path).fit(train_data)
    
    return model

