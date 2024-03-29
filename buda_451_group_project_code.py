# -*- coding: utf-8 -*-
"""BUDA 451 Group Project Code.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/144US_-7CRaC3k9pe_mdSFeL6b52cIfns

## Importing Spotify Dataset:
"""

import pandas as pd

rawdata = pd.read_csv("https://raw.githubusercontent.com/taggartshea/BUDA451/main/BUDA451%20Spotify%20Data.csv",  header=0)
rawdata

processingdata = rawdata.drop(labels = ['Unnamed: 0', 'song_title', 'artist', 'duration_ms'], axis = 1)
cleandata = processingdata.drop_duplicates()
cleandata

cleandatashuffled = cleandata.sample(frac = 1)
cleandatashuffled

rawdata.isnull().sum()

df = rawdata['artist'].nunique()
df

pd.set_option('display.max_rows', None)
df = rawdata["artist"].value_counts()
df

pd.set_option('display.max_rows', None)
df2 = rawdata["song_title"].value_counts()
df2

textdata = rawdata.drop(labels = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'Unnamed: 0', 'duration_ms'], axis=1)
textdata

"""## Splitting data into training and test datasets:"""

x_cols = ["acousticness", "danceability", "energy", "instrumentalness", "key", "liveness", "loudness", "mode", "speechiness", "tempo", "time_signature",
          "valence"]

import pandas as pd
from sklearn.model_selection import train_test_split

training_data = cleandatashuffled.sample(frac=0.8, random_state=25)
testing_data = cleandatashuffled.drop(training_data.index)

print(f"No. of training examples: {training_data.shape[0]}")
print(f"No. of testing examples: {testing_data.shape[0]}")

# train data
X_train = training_data[x_cols].values
y_train = training_data['target'].values

# test data
X_test = testing_data[x_cols].values
y_test = testing_data['target'].values

print(f'num train records: {len(X_train)}')
print(f'num train records: {len(X_test)}')

"""## Model 1: Decision Tree"""

from sklearn import tree

clf = tree.DecisionTreeClassifier(criterion='entropy', max_depth=5)
clf.fit(X_train, y_train)
y_pred_tree = clf.predict(X_test)

import pydotplus
from IPython.display import Image

dot_data = tree.export_graphviz(clf, feature_names=x_cols, class_names=['0','1'], filled=True,
                                out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
Image(graph.create_png())

testY = cleandata['target']
testX = cleandata.drop(['target'],axis=1)

predY = clf.predict(testX)
predictions = pd.concat([testY,pd.Series(predY,name='Predicted Class')], axis=1)
predictions

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


print('Accuracy on test data is %.2f' % (accuracy_score(y_test, y_pred_tree)))
print('Precision on test data is %.2f' % precision_score(y_test, y_pred_tree) )
print('Recall on test data is %.2f' % recall_score(y_test, y_pred_tree) )
print('F1_score on test data is %.2f' % f1_score(y_test, y_pred_tree) )

from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(clf, X_test, y_test)

"""## Model 2: Logistic Regression"""

import sklearn.linear_model
log_reg = sklearn.linear_model.LogisticRegression(fit_intercept=True, C=20)

log_reg.fit(X_train, y_train)

y_pred = log_reg.predict(X_test)

print('Accuracy on test data is %.2f' % (accuracy_score(y_test, y_pred)))
print('Precision on test data is %.2f' % precision_score(y_test, y_pred) )
print('Recall on test data is %.2f' % recall_score(y_test, y_pred) )
print('F1_score on test data is %.2f' % f1_score(y_test, y_pred) )

import matplotlib.pyplot as plt


coefs = pd.DataFrame(
   log_reg.coef_.ravel(),
   columns=['coefficients'], index=x_cols
)

coefs.plot(kind='barh', figsize=(9, 7))
plt.title('Logistic regression model')
plt.axvline(x=0, color='0.5')
plt.subplots_adjust(left=.1)
plt.grid( color='0.95')

from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(log_reg, X_test, y_test)

"""## Model 3: SVM"""

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


clf_svm = SVC(C=30, kernel='rbf')
clf_svm.fit(X_train, y_train)
y_pred_SVM = clf_svm.predict(X_test)

print('Accuracy on test data is %.2f' % (accuracy_score(y_test, y_pred_SVM)))
print('Precision on test data is %.2f' % precision_score(y_test, y_pred_SVM) )
print('Recall on test data is %.2f' % recall_score(y_test, y_pred_SVM) )
print('F1_score on test data is %.2f' % f1_score(y_test, y_pred_SVM) )

from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(clf_svm, X_test, y_test)

"""## Model 4: Ensemble Methods

### Bagging:
"""

from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier

bag_clf = BaggingClassifier(
    DecisionTreeClassifier(criterion='entropy', max_depth=8),
    n_estimators=500,
    max_samples=100, bootstrap=True, random_state=42)

bag_clf.fit(X_train, y_train)
y_pred_bag = bag_clf.predict(X_test)

print('Accuracy on test data is %.2f' % (accuracy_score(y_test, y_pred_bag)))
print('Precision on test data is %.2f' % (precision_score(y_test, y_pred_bag)))
print('Recall on test data is %.2f' % (recall_score(y_test, y_pred_bag)))
print('F1_score on test data is %.2f' % (f1_score(y_test, y_pred_bag)))

from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(bag_clf, X_test, y_test)

"""### Random Forests:"""

from sklearn.ensemble import RandomForestClassifier

rnd_clf = RandomForestClassifier(max_leaf_nodes=5,
                                 n_estimators=500,
                                 max_samples=100,
                                 random_state=42)
rnd_clf.fit(X_train, y_train)
y_pred_rf = rnd_clf.predict(X_test)

print('Accuracy on test data is %.2f' % (accuracy_score(y_test, y_pred_rf)))
print('Precision on test data is %.2f' % (precision_score(y_test, y_pred_rf)))
print('Recall on test data is %.2f' % (recall_score(y_test, y_pred_rf)))
print('F1_score on test data is %.2f' % (f1_score(y_test, y_pred_rf)))

from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(rnd_clf, X_test, y_test)

"""### AdaBoost:"""

from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

ada_clf = AdaBoostClassifier(
    DecisionTreeClassifier(criterion='entropy', max_depth=5), n_estimators=500,
    algorithm="SAMME.R", learning_rate=0.5, random_state=42)
ada_clf.fit(X_train, y_train)
y_pred_ada = ada_clf.predict(X_test)

print('Accuracy on test data is %.2f' % (accuracy_score(y_test, y_pred_ada)))
print('Precision on test data is %.2f' % (precision_score(y_test, y_pred_ada)))
print('Recall on test data is %.2f' % (recall_score(y_test, y_pred_ada)))
print('F1_score on test data is %.2f' % (f1_score(y_test, y_pred_ada)))

from sklearn.metrics import ConfusionMatrixDisplay

ConfusionMatrixDisplay.from_estimator(ada_clf, X_test, y_test)

"""## Investigating Text Models:"""

# Commented out IPython magic to ensure Python compatibility.
!pip install -U NLTK
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfTransformer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy.random import random

# %matplotlib inline

training_data = textdata.sample(frac=0.8, random_state=25)
testing_data = textdata.drop(training_data.index)

x_cols = ["artist", "song_title"]

# train data
text_train = training_data['artist']
y_train = training_data['target']

# test data
text_test = testing_data['artist']
y_test = testing_data['target']

from sklearn.feature_extraction.text import TfidfVectorizer
# train data

tfidfVec = TfidfVectorizer(min_df=5,
                           tokenizer=nltk.word_tokenize,
                           max_features=3000)

X_train = tfidfVec.fit_transform(text_train)
X_test = tfidfVec.transform(text_test)

maxdepths = [2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50]

for depth in maxdepths:
    clf_tree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=depth)
    clf_tree.fit(X_train, y_train)
    y_pred_tree = clf_tree.predict(X_test)
    print('Accuracy on test data is %.2f' % (accuracy_score(y_test, y_pred_tree)))

text_train = training_data['song_title']
y_train = training_data['target']

# test data
text_test = testing_data['song_title']
y_test = testing_data['target']

from sklearn.feature_extraction.text import TfidfVectorizer
# train data

tfidfVec = TfidfVectorizer(min_df=5,
                           tokenizer=nltk.word_tokenize,
                           max_features=3000)

X_train = tfidfVec.fit_transform(text_train)
X_test = tfidfVec.transform(text_test)

maxdepths = [2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50]

for depth in maxdepths:
    clf_tree = tree.DecisionTreeClassifier(criterion='entropy', max_depth=depth)
    clf_tree.fit(X_train, y_train)
    y_pred_tree = clf_tree.predict(X_test)
    print('Accuracy on test data is %.2f' % (accuracy_score(y_test, y_pred_tree)))

from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

reguList = [0.1, 0.5, 1.0,  5, 10, 20, 50, 100]
for regu in reguList:
    clf_svm = SVC(C=regu, kernel='rbf')
    clf_svm.fit(X_train, y_train)
    Y_predTest = clf_svm.predict(X_test)
    print('Accuracy on test data is %.2f' % (accuracy_score(y_test, Y_predTest)))