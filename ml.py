from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from pandas import DataFrame
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
#from xgboost import XGBClassifier
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn import preprocessing
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def splitData(X:DataFrame,Y:DataFrame):
    return train_test_split(X,Y,train_size=0.7,random_state=42)

def trainSupervisedModels(dataset:DataFrame):
    #Split features and label :
    Y = dataset.label.copy()
    X = dataset.copy()
    X = X.drop(columns=['label'])
    X = preprocessing.scale(X)                          #Scale features

    #Scale features :
    models = [
          ('RF', RandomForestClassifier(n_estimators=100,criterion='gini',max_depth=10,min_samples_split=2)),
          ('KNN', KNeighborsClassifier()),
          ('SVM', SVC()),
          ('GNB', GaussianNB()),
         # ('XGB', XGBClassifier())
        ]

    results = []

    scoring = ['accuracy', 'precision_weighted', 'recall_weighted', 'f1_weighted', 'roc_auc']
    for name, model in models:
        result = {}
        result['name'] = name;
        result['model'] = model.fit(X, Y.values.tolist());
        kfold = model_selection.KFold(n_splits=5, shuffle=True, random_state=42)
        cv_results = model_selection.cross_validate(model, X, Y.values.tolist(), cv=kfold, scoring=scoring)
        result['metrics'] = {}
        for s in scoring:
            result['metrics'][s] = np.mean(cv_results['test_' + s])
        full_results = pd.DataFrame(cv_results)
        full_results['model'] = name
        result['full_results'] = full_results.copy()
        results.append(result)

    return results

def supervisedModelComparison(results):
    final = pd.concat([res['full_results'] for res in results], ignore_index=True)
    bootstraps = []
    for model in list(set(final.model.values)):
        model_df = final.loc[final.model == model]
        bootstrap = model_df.sample(n=30, replace=True)
        bootstraps.append(bootstrap)
    bootstrap_df = pd.concat(bootstraps, ignore_index=True)
    results_long = pd.melt(bootstrap_df,id_vars=['model'],var_name='metrics', value_name='values')
    time_metrics = ['fit_time','score_time'] # fit time metrics
    ## PERFORMANCE METRICS
    results_long_nofit = results_long.loc[~results_long['metrics'].isin(time_metrics)] # get df without fit data
    results_long_nofit = results_long_nofit.sort_values(by='values')
    ## TIME METRICS
    results_long_fit = results_long.loc[results_long['metrics'].isin(time_metrics)] # df with fit data
    results_long_fit = results_long_fit.sort_values(by='values')
    plt.figure(figsize=(20, 12))
    sns.set(font_scale=2.5)
    g = sns.boxplot(x="model", y="values", hue="metrics", data=results_long_nofit, palette="Set3")
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.title('Comparison of Model by Classification Metric')
    plt.savefig('./benchmark_models_performance.png',dpi=300)
    metrics = list(set(results_long_nofit.metrics.values))
    bootstrap_df.groupby(['model'])[metrics].agg([np.std, np.mean])