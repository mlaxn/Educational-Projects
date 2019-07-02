#+++++++++++++++++++++++++
# MILAN BISWAKARMA       +
# DATA MINING            +
# ASSIGNMENT 1           +
# NOVEMBER 2, 2018       +
#+++++++++++++++++++++++++

import os
import re                                           #for tokinization
import math                                         #for log calc
import nltk                                         #for nltk download
from nltk.tokenize import RegexpTokenizer           #for tokenize
from nltk.corpus import stopwords                   #for stopwords downlaod
from nltk.stem.porter import PorterStemmer          #for stemmer

#stemmer function to stem the vector
stemmer = PorterStemmer()

#tokenize function for line and word
def tokenize(line):                                 # tokenize the line into words
    list =[]                                        # list intialization
    tokenizer = RegexpTokenizer(r'[a-zA-Z]+')       # tokenizer defination for the list
    stop_list = stopwords.words("english")          # store the list in the stop_list
    tokens = tokenizer.tokenize(line)               # stores the tokens in the list
    for word in tokens:
        if word not in stop_list:
           list.append(stemmer.stem(word))          # appends the stremmed and tokenized words in the list
    return list

filename = './debate.txt'                           # filename given
file = open(filename, "r", encoding='UTF-8')        # reads the file
para_list = []                                      # list for the paragraphs intialized
doc = file.readlines()
for line in doc:                                    # for each paragraph splits the empty lists and makes it lower case
    if line.split():
        line.lower()
        para_list.append(tokenize(line))            # uses the tokenize function to tokenize each paragraph

length = len(para_list)                             # intializes the number of documents

# GETIDF FUNCTION
def getidf(word):
    word.lower()
    count = 0
    idf =0
    for line in doc:                                # goes through each word for every paragraph
        if word in line:                            # and counts the number of occurence
            count += 1
        if count != 0:                              # finally calculate the idf = log10(N/doc.freq)
            idf = math.log10(length/count)
        else:                                       # if the word is not in the list. Set idf =1
            idf = 1
    return idf

#GETQVEC FUNCTION
def getqvec(command):
    command.lower()
    word = tokenize(command)                        #tokenize the given string
    sum = 0
    denom = 1

    dic = {}
    vector = {}
    for each in word:                               # for each word creates a dictionary(key,value) = (word, idf)
        dic[each] = getidf(each)

    for value in dic.values():                      # normilizes the given dictionary
        sum += math.pow(value, 2)                   # calculates the square of the sum and thier sqaure root to find the denom
    denom = math.sqrt(sum)

    for each in word:                               # normalizes the dictionary and adds them new vector
        vector[each] = float(getidf(each)/denom)
    return(vector)

