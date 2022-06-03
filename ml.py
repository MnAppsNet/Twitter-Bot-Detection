from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from pandas import DataFrame

def splitData(X:DataFrame,Y:DataFrame):
    return train_test_split(X,Y,train_size=0.7,random_state=42)

def randomForest(dataset:DataFrame):
    estimators = 100
    criterion = 'gini'
    max_depth = 10
    min_samples_split = 2
    Y = dataset.label.copy()
    X = dataset.copy()
    X = X.drop(columns=['label'])
    x_train, x_test, y_train, y_test = splitData(X,Y)
    model = RandomForestClassifier(estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, random_state=42)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    return model, {
        'accuracy':metrics.accuracy_score(y_test,y_pred),
        'precision':metrics.precision_score(y_test,y_pred),
        'recall':metrics.recall_score(y_test,y_pred),
        'f1':metrics.f1_score(y_test,y_pred)
    }