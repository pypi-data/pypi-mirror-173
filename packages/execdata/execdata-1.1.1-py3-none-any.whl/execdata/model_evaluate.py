'''
Date         : 2022-10-25 17:21:52
Author       : BDFD,bdfd2005@gmail.com
Github       : https://github.com/bdfd
LastEditTime : 2022-10-26 12:21:58
LastEditors  : BDFD
Description  : 
FilePath     : \execdata\model_evaluate.py
Copyright (c) 2022 by BDFD, All Rights Reserved. 
'''
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
# from xgboost import XGBClassifier


def model_evaluate(X_train, X_test, y_train, y_test):
    train_scores = []
    test_scores = []

    classifiers = {
        "LogisticRegression" : LogisticRegression(),
        "KNeighbors" : KNeighborsClassifier(),
        "SVC" : SVC(),
        "DecisionTree" : DecisionTreeClassifier(),
        "RandomForest" : RandomForestClassifier(),
        # "XGBoost" : XGBClassifier()
    }

    models = ['LogisticRegression', 'KNeighbors', 'SVC', 'DecisionTree', 'RandomForest']

    for key, classifier in classifiers.items():
        classifier.fit(X_train, y_train)
        train_score = classifier.score(X_train, y_train)
        train_scores.append(train_score)
        test_score = classifier.score(X_test, y_test)
        test_scores.append(test_score)

    print(f'model list is {models}')
    for n in range(5):
        print(f'for model {models[n]} with the train_score:{train_scores[n]} and test_score:{test_scores[n]} ')

    return train_scores, test_scores, models