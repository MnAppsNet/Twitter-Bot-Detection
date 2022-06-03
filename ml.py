from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pandas import DataFrame

def splitData(X:DataFrame,Y:DataFrame):
    return train_test_split(X,Y,train_size=0.7,random_state=42)

def randomForest(dataset:DataFrame):
    Y = dataset.label.copy()
    X = dataset.drop('label');
    X_train, X_test, y_train, y_test = splitData(X,Y)
    