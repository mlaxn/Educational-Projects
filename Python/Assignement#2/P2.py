#+++++++++++++++++++++++++
# MILAN BISWAKARMA       +
# ID # 1001430854        +
# DATA MINING            +
# ASSIGNMENT 2           +
# NOVEMBER 23, 2018      +
#+++++++++++++++++++++++++
#Reference :
# Coding maniace
# kaggle.com
# youtube:
#  1) https://www.youtube.com/watch?v=lLbyEYjU55A&list=PL88fc_qdw6gfY1RgFVI0PTvKloBKmOC2Q&t=1201s&index=2
#  2) https://www.youtube.com/watch?v=hXNbFNCgPfY&index=3&list=PL88fc_qdw6gfY1RgFVI0PTvKloBKmOC2Q
#  3) https://www.youtube.com/watch?v=5xDE06RRMFk&index=14&list=PL88fc_qdw6gfY1RgFVI0PTvKloBKmOC2Q
#  4) https://www.youtube.com/watch?v=7gAZoK6kGhM&index=12&list=PL88fc_qdw6gfY1RgFVI0PTvKloBKmOC2Q&t=0s

import pandas as pd
import re
import numpy as np

from nltk.corpus import stopwords                               # for importing stopwords from nltk
from nltk.stem import SnowballStemmer                           # for stemmer
from sklearn.feature_extraction.text import TfidfVectorizer     # gives the tfidf of the words
from sklearn.pipeline import Pipeline                           # for pipelining the sequence of actions

from sklearn.model_selection import train_test_split            # for splitting the training and test data set
from sklearn.feature_selection import SelectKBest, chi2         # for selection of best words from the features
from sklearn.model_selection import cross_val_score             # for calculation of the cross valuation
from sklearn import metrics                                     # for calculation of the metrices in classification report

from sklearn.svm import LinearSVC                               # Linear Support Vector Machines
from sklearn.neighbors import KNeighborsClassifier              # k Nearest Neighbors
from sklearn.tree import DecisionTreeClassifier                 # Decision Tree
from sklearn.naive_bayes import GaussianNB                      # Naive Bayes Classification

from sklearn.externals import joblib                            # joblib helps to store and use the model as pickle file
import pickle
from nltk.tokenize import RegexpTokenizer                       #for tokenize

def tokenize(line):                                             # tokenize the line into words
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+""')
    return tokenizer.tokenize(line)

"""
Mode :: Train
Takes the input file and creates a classification model as pickel file
Also, prints the classification report, confusion matrix, and accuracy rete
"""

def train(filename):                                            # function for training mode
    #print("======== Train Mode =========")
    filename = filename.strip()                                 # strips the space from the begining of the filename
    data = pd.read_csv(filename)                                # reads and stores the .csv using panda

    stemmer = SnowballStemmer('english')                        # intializes the snowball stemmer
    words = stopwords.words("english")                          # stores the stopwords form stopwords library

    """ 
    The complex expression takes the text from the csv file, 
    1) converts them into lower case, 
    2) checks if not in the stop words list
    3) if not present split them
    4) then stemms the word 
    5) finally adds the filtered word in the new filtred data set
    """

    data['fitered'] = data['text'].apply(
        lambda x: " ".join([stemmer.stem(i) for i in re.sub("[^a-zA-Z]", " ", x).split() if i not in words]).lower())
    # print(data['filtered'])

    """ splits data set into test(25%) and training(75%) set """
    X_train, X_test, y_train, y_test = train_test_split(data['fitered'], data.label, test_size=0.25)

    """ 
    uses the pipepline function 
    1) takes the data set and create the vector with tfidf, 
    ngram takes to consequetive into consideration to create a bag of words
    2) from the bag of words, chi function selects k=1000 best features,
    3) finally, LinearSVC: the linear support vector does classification, where maximum number of iterations set to 300
    """
    pipeline = Pipeline([('vect', TfidfVectorizer(ngram_range=(1, 2))),
                         ('chi', SelectKBest(chi2, k=1000)),
                         ('clf', LinearSVC(max_iter = 300))])


    model = pipeline.fit(X_train, y_train)          # fits the model using the pipeline

    # store your trained model as pickle object using sklearn joblib
    joblib.dump(model, 'SVM.pkl')
    # load a pickle object
    trained_model = joblib.load('SVM.pkl')
    #print("Test set score: {:.3f}".format(trained_model.score(X_test, y_test)))

    # -------------------------------------------------------------

    # prints the table of the recall, f measure and accuracy
    # Classification Report(SVM)
    print("Classification Report:")
    y_expect = y_test
    y_pred = trained_model.predict(X_test)
    print(metrics.classification_report(y_expect, y_pred))      # calculate and prints the classification report

    #Confusion matrix (SVM)
    print("Confusion matrix:")
    prediction = trained_model.predict(X_test)
    print(pd.crosstab(y_test, prediction, rownames=['True'], colnames=['Predicted'], margins=True))
#-----------------------------------------------------------
"""
Mode :: Cross Validation
Takes the input file and uses the trained model prints 
- 10 fold cross validation and 
- average cross validation score
"""

def cross_val (filename):
   #print("========= Cross Valuation Mode =========")

   filename = filename.strip()                                      # strips the unneccessary space from the filename
   data = pd.read_csv(filename)                                     # read and store the csv file using panda

   trained_model = joblib.load('SVM.pkl')                           # loads the trained model

   scores = cross_val_score(trained_model, data.text, data.label, cv=10)    # calculates the cv = 10, cross validation score
   print()
   print("Cross-validation scores: {}".format(scores))
   print()
   print("Average cross-validation score: {:.2f}".format(scores.mean()))

#-----------------------------------------------------------
"""
Mode :: Precict
Uses the trained model to give the classfication for the desired test string
"""
def predict (filename):
    filename = filename.strip()                                     # strips the unneccessary space from the filename
    print("In prediction:",filename)                                # read and store the csv file using panda

    trained_model = joblib.load('SVM.pkl')                          # loads the trained model
    print(trained_model.predict([filename]))                        # prints classified class from the trained model

# trained_model = joblib.load('SVM.pkl')

# print(trained_model.predict(['Three years in a row now, you have voted against the Defense Authorization Act.']))
# print(trained_model.predict(['And as you know, nobody can reach the White House without the Hispanic vote.']))
# print(trained_model.predict(['Barack Obama did not vote for sanctions against Iran.' ]))
# print(trained_model.predict([ '65% of Texas voters casted a ballot for Donald Trump.']))

"""
Takes the command line input from the user
1) finds the desired mode from the command line and calls the respective function
2) splits the string using the key word input to get the desired pararameter, filename or test string
3) calls the respective function
4) quits when the "quit" is pressed

"""
while(True):
    command = input()

    if('train' in command):
        string = command
        filename = ''
        word = string.split("input")
        filename = word[1]
        #print("Word[1]:  ", word[1],"filename: ",filename)
        train(filename)

    if ('cross_val' in command):
        string = command
        filename = ''
        word = string.split("input")
        filename = word[1]
        # print("Word[1]:  ", word[1],"filename: ",filename)
        cross_val(filename)

    if ('predict' in command):
        string = command
        filename = ''
        word = string.split("input")
        filename = word[1]
        #print("filename:",filename)
        predict(filename)

    if (command == 'quit'):
        print("Exiting the Program....")
        exit()
