from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split , KFold
from sklearn import metrics
from pandas import DataFrame
from sklearn.preprocessing import PolynomialFeatures
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
#from xgboost import XGBClassifier
from sklearn import model_selection
from sklearn.utils import class_weight
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np
import pandas as pd


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

def trainModels(dataset:DataFrame):
    Y = dataset.label.copy()
    X = dataset.copy()
    X = X.drop(columns=['label'])
    x_train, x_test, y_train, y_test = splitData(X,Y)

    models = [
          ('LogReg', LogisticRegression(),{}),
          ('RF', RandomForestClassifier(n_estimators=100,criterion='gini',max_depth=10,min_samples_split=2),{}),
          ('KNN', KNeighborsClassifier(),{}),
          ('SVM', SVC(),{}),
          ('GNB', GaussianNB(),{}),
         # ('XGB', XGBClassifier())
        ]

    scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted', 'roc_auc']
    target_names = ['BOT', 'HUMAN']
    for name, model, metrics in models:
        kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=42)
        cv_results = model_selection.cross_validate(model, x_train, y_train, cv=kfold, scoring=scoring)
        clf = model.fit(x_train, y_train)
        y_pred = clf.predict(x_test)
        print(name)
        metrics = classification_report(y_test, y_pred, target_names=target_names)
        print(metrics)

    return models