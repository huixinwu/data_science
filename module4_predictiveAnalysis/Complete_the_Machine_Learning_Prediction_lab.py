"""
module 4: predictive analysis (classification)
Hands on Lab: Complete the Machine Learning Prediction lab

"""
# Pandas is a software library written for the Python programming language for data manipulation and analysis.
import pandas as pd
# NumPy is a library for the Python programming language, adding support for large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical functions to operate on these arrays
import numpy as np
# Matplotlib is a plotting library for python and pyplot gives us a MatLab like plotting framework. We will use this in our plotter function to plot data.
import matplotlib.pyplot as plt
#Seaborn is a Python data visualization library based on matplotlib. It provides a high-level interface for drawing attractive and informative statistical graphics
import seaborn as sns
# Preprocessing allows us to standarsize our data
from sklearn import preprocessing
# Allows us to split our data into training and testing data
from sklearn.model_selection import train_test_split
# Allows us to test parameters of classification algorithms and find the best one
from sklearn.model_selection import GridSearchCV
# Logistic Regression classification algorithm
from sklearn.linear_model import LogisticRegression
# Support Vector Machine classification algorithm
from sklearn.svm import SVC
# Decision Tree classification algorithm
from sklearn.tree import DecisionTreeClassifier
# K Nearest Neighbors classification algorithm
from sklearn.neighbors import KNeighborsClassifier

def plot_confusion_matrix(y,y_predict):
    "this function plots the confusion matrix"
    from sklearn.metrics import confusion_matrix

    cm = confusion_matrix(y, y_predict)
    ax= plt.subplot()
    sns.heatmap(cm, annot=True, ax = ax); #annot=True to annotate cells
    ax.set_xlabel('Predicted labels')
    ax.set_ylabel('True labels')
    ax.set_title('Confusion Matrix'); 
    ax.xaxis.set_ticklabels(['did not land', 'land']); ax.yaxis.set_ticklabels(['did not land', 'landed']) 
    plt.show() 

import pandas as pd
import requests
import io

URL1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv"

response = requests.get(URL1)
text1 = io.BytesIO(response.content)
data = pd.read_csv(text1)
print(data.head())


URL2 = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_3.csv'

response = requests.get(URL2)
text2 = io.BytesIO(response.content)

X = pd.read_csv(text2)
print(X.head(100))

# task 1
Y = data['Class'].to_numpy()
print(Y)

# task 2
transform = preprocessing.StandardScaler()
X = transform.fit_transform(X)
print(X)

# task 3
from sklearn.model_selection import train_test_split

X_train, X_test, Y_train, Y_test = train_test_split(
    X, Y,
    test_size=0.2,
    random_state=2
)
Y_test.shape

# task 4
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

# Define the hyperparameter grid
parameters = {
    "C": [0.01, 0.1, 1],
    "penalty": ["l2"],   # l2 = Ridge, l1 = Lasso
    "solver": ["lbfgs"]
}

# Create Logistic Regression object
lr = LogisticRegression()

# Create GridSearchCV object with 10-fold cross-validation
logreg_cv = GridSearchCV(estimator=lr, param_grid=parameters, cv=10)

# Fit the GridSearchCV object to the training data
logreg_cv.fit(X_train, Y_train)

# Display the best parameters
print("Tuned hyperparameters (best parameters):", logreg_cv.best_params_)

# Display the best accuracy from cross-validation
print("Accuracy on validation data:", logreg_cv.best_score_)

# task 5
print("Test Accuracy:", logreg_cv.score(X_test, Y_test))

# task 6
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
import numpy as np

# Define parameters
parameters = {
    'kernel': ('linear', 'rbf', 'poly', 'sigmoid'),
    'C': np.logspace(-3, 3, 5),
    'gamma': np.logspace(-3, 3, 5)
}

# Create SVM model
svm = SVC()

# Create GridSearchCV object
svm_cv = GridSearchCV(estimator=svm, param_grid=parameters, cv=10)

# Fit model
svm_cv.fit(X_train, Y_train)

# Output results
print("Tuned hyperparameters (best parameters):", svm_cv.best_params_)
print("Accuracy:", svm_cv.best_score_)

# task 7
# Accuracy on test data
print("Test Accuracy:", svm_cv.score(X_test, Y_test))

# Predictions
yhat = svm_cv.predict(X_test)

# Confusion matrix
#plot_confusion_matrix(Y_test, yhat)

# task 8
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

# Define parameters
parameters = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_depth': [2*n for n in range(1, 10)],
    'max_features': ['auto', 'sqrt'],
    'min_samples_leaf': [1, 2, 4],
    'min_samples_split': [2, 5, 10]
}

# Create Decision Tree model
tree = DecisionTreeClassifier()

# Create GridSearchCV object
tree_cv = GridSearchCV(estimator=tree, param_grid=parameters, cv=10)

# Fit model
tree_cv.fit(X_train, Y_train)

# Output results
print("Tuned hyperparameters (best parameters):", tree_cv.best_params_)
print("Accuracy:", tree_cv.best_score_)

# task 9
print("Test Accuracy:", tree_cv.score(X_test, Y_test))
yhat = tree_cv.predict(X_test)
#plot_confusion_matrix(Y_test, yhat)

# task 10
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

# Define parameters
parameters = {
    'n_neighbors': [1,2,3,4,5,6,7,8,9,10],
    'algorithm': ['auto', 'ball_tree', 'kd_tree', 'brute'],
    'p': [1, 2]
}

# Create KNN model
KNN = KNeighborsClassifier()

# Create GridSearchCV object
knn_cv = GridSearchCV(estimator=KNN, param_grid=parameters, cv=10)

# Fit model
knn_cv.fit(X_train, Y_train)

# Output results
print("Tuned hyperparameters (best parameters):", knn_cv.best_params_)
print("Accuracy:", knn_cv.best_score_)

# task 11
yhat = knn_cv.predict(X_test)
#plot_confusion_matrix(Y_test, yhat)

# task 12
print("LogReg:", logreg_cv.score(X_test, Y_test))
print("SVM:", svm_cv.score(X_test, Y_test))
print("Decision Tree:", tree_cv.score(X_test, Y_test))
print("KNN:", knn_cv.score(X_test, Y_test))

print("Test Accuracy:", knn_cv.score(X_test, Y_test))

yhat = knn_cv.predict(X_test)
plot_confusion_matrix(Y_test, yhat)