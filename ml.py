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

def different_models(dataset:DataFrame):
    Y = dataset.label.copy()
    X = dataset.copy()
    X = X.drop(columns=['label'])
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Prepare cross-validation (cv)
    cv = KFold(n_splits = 5, random_state = None)
    
    # Classifiers
    names = ["Logistic Regression", "Logistic Regression with Polynomial Hypotheses",
    "Linear SVM", "RBF SVM", "Neural Net", "Decision Tree","Random Forest"]

    classifiers = [
        LogisticRegression(solver='lbfgs', max_iter=1000),
        make_pipeline(PolynomialFeatures(3), LogisticRegression(solver='lbfgs', max_iter=1000)),
        SVC(kernel="linear", C=0.025,max_iter=1000 ),
        SVC(gamma=2, C=1,max_iter=1000),
        MLPClassifier(alpha=1,max_iter=1000),
        DecisionTreeClassifier(),
        RandomForestClassifier(n_estimators=100)
    ]
    
    models = []
    trained_classifiers = []
    for name, clf in zip(names, classifiers):
        scores = []
        for train_indices, test_indices in cv.split(X):
            clf.fit(X[train_indices], Y[train_indices].ravel())
            scores.append( clf.score(X_test, y_test.ravel()) )
        
        min_score = min(scores)
        max_score = max(scores)
        avg_score = sum(scores) / len(scores)
        
        trained_classifiers.append(clf)
        models.append((name, min_score, max_score, avg_score)) 
    
    fin_models = DataFrame(models, columns = ['Name', 'Min Score', 'Max Score', 'Mean Score'])

    return (fin_models.sort_values(['Mean Score']))