#178244
from autobiotool.utils import *
from Classifier.Genetic_Algorithm.SVMClassifier import *
from sklearn.metrics import roc_curve, auc
import sklearn
random.seed(123)
data = ReadCsv('feature.csv')
targets = ReadCsv('labels.csv')
targets = [int(i[0]) for i in targets]
data, targets=shuffle(data, targets)
# cls = autosklearn.classification.AutoSklearnClassifier( time_left_for_this_task=720, per_run_time_limit=190, ml_memory_limit=10000)
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(data, targets, random_state=1)
y_train=[[i] for i in y_train]



from autogluon.tabular import TabularDataset, TabularPredictor



label = 256  # specifies which column do we want to predict

save_path = 'ag_models/'  # where to save trained models

Train=np.hstack((X_train,y_train))

train_data = pd.DataFrame(Train)
X_test = pd.DataFrame(X_test)





#predictor = TabularPredictor(label=label, path=save_path).fit(train_data)

#print(X_test.head())

predictor = TabularPredictor.load(save_path)  # Unnecessary, we reload predictor just to demonstrate how to load previously-trained predictor from file
y_prob = predictor.predict_proba(X_test)
y_prob=[i[1] for i in y_prob.values.tolist()]

fpr, tpr, thresholds = roc_curve(y_test, y_prob)
roc_auc = auc(fpr, tpr)
print(roc_auc)