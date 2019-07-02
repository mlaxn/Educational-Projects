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
#nltk.download()
from nltk.tokenize import RegexpTokenizer           #for tokenize
from nltk.corpus import stopwords                   #for stopwords downlaod
from nltk.stem.porter import PorterStemmer          #for stemmer


#tokenize function for line and word

def string_token(string):
    return string.split()


# turns the list into lower case
def lowerize(list1):
    for i in range(len(list1)):
        temp = []
        for word in list1[i]:
            temp.append(word.lower())
        list1[i]= temp
        #print("Lower list: ", i, list1[i])
    return list1


#Stop word removal function for the list of words
def swremover(list1):
    stop_list = []
    for words in stopwords.words('english'):                    # converts the downloaded stop words into list of stopwords
        stop_list.append(words)
    # for i in range(len(stop_list)):                           #prints the list of the stopwords
    #     print("Stopword No: ",i+1 , stop_list[i]," >> ")

    for i in range(len(list1)):
        temp = []                                               # store the temporary stopwords removed list
        temp_word = ''                                          # temp list to store the words for comparison
        for word in list1[i]:                                   # iterates through words in the given list
            temp = list1[i]                                     # temp list intilized at the index
            temp_word = word                                    # temp word intilized for comparison
            for j in range(len(stop_list)):
                if (temp_word == stop_list[j]):                 # if the word in the list is same as stopword list,
                    temp.remove(temp_word)                      # then remove from the list
        list1[i] = temp                                         # updates the list no stopwords list = temp

    #print("------------------------------------------------")
    # for i in range(len(list1)):  # prints list with no stop word
    #     print("No Stopword List No: ", i, list1[i], " >> ", len(list1[i]))

    return list1

#Stemming function of the list of words
def stemmize (list1):
    for i in range(len(list1)):
        temp = []                                   # temp list to store the stemmed words
        stemmer = PorterStemmer()
        for word in list1[i]:                       # iterates through words in the given list
            temp.append(stemmer.stem(word))         # appends the stemmed words in the temp list
        list1[i] = temp                             # updates the list with the stemmed words list = temp

    #print("------------------------------------------------")
    # for i in range(len(list1)):                   # prints the stemmed list
    #     print("Stemmed List No: ", i, list1[i], " >> ", len(list1[i]))
    return list1

#stems the sample list
def list_stem(sam_list):
    temp = []

    for word in sam_list:
        stemmer = PorterStemmer()
        temp.append((stemmer.stem(word)))
    sam_list = temp
    return sam_list

#removes the stop words from the single list **still needs to be checked
def list_swremover (list1):

    stop_list = []
    for words in stopwords.words('english'):            # converts the downloaded stop words into list of stopwords
        stop_list.append(words)
    # for i in range(len(stop_list)):                   #prints the list of the stopwords
    #     print("Stopword No: ",i+1 , stop_list[i]," >> ")

    temp = []                                   # store the temporary stopwords removed list
    temp_word = ''                              # temp list to store the words for comparison
    for word in list1:                          # iterates through words in the given list
        temp = list1                            # temp list intilized at the index
        temp_word = word                        # temp word intilized for comparison
        for j in range(len(stop_list)):
            if (temp_word == stop_list[j]):     # if the word in the list is same as stopword list,
                temp.remove(temp_word)          # then remove from the list
                                                # updates the list no stopwords list = temp

    return temp

#dictionary function to creat the dictionary of whole words
def dictionize(list1):
    dic = {}                                    # introduction of the dictionary variable
    for i in range(len(list1)):
        for word in list1[i]:
            dic[word] = dic.get(word, 0) + 1    # idiom: update the counter very time the word is found, else zero
    #print("------------------------------------------------")
    #print("List Dictionary: \n ", dic)  # prints the list of the dictionary

    return dic
#===============================

#sample dictionary of just a single list
def dictionize2(list1):
    dic = {}                                         # introduction of the dictionary variable
    for word in list1:
        dic[word] = dic.get(word, 0) + 1             # idiom: update the counter very time the word is found, else zero
    #print("------------------------------------------------")
    #print("List Dictionary: \n ", dic)              # prints the list of the dictionary

    return dic
#====================================
# Dft_ finder: finds the document frequency of the given word
#===================================
def dft_finder(str):

    idf = 0
    stemmer = PorterStemmer()                       # using stemmer to stem the word
    str = stemmer.stem(str)
    #print("Func. before stemmed: ", str, idf)
    for i in range(len(list1)):                     # for loop to check if the word exist in the list,
        for word in list1[i]:
            if (str == word):                       # if exist then increment the idf counter and break out the document list
                idf = idf + 1
                break
    #print("Func. after stemmed: ", str, idf)

    if idf == 0:                                    # if word not in document, then set defualt idf to 1
        idf = 1
        #print("Func. No Match %.4f= "% idf)
    else:                                           # else calculat the idf with formula
        idf = math.log10(N / idf)                   # idf = log10 (N/idf)
        #print("Func. Idf ::%.4f " %idf)

    return idf
#=========================================
#
def tf_finder(str, strlist):
    tf = 0
    stemmer = PorterStemmer()                       # using stemmer to stem the word
    str = stemmer.stem(str)
    strlist = list_stem(strlist)
    #print(strlist)
    #print("TF Func. before stemmed: ", str, tf)

    for word in strlist:
        if (str == word):
            tf = tf + 1
    #print("TF Func. After stem: ", str, tf)
    tf = math.log10(tf)
    tf = 1 + tf
    return tf


# ===============================
#1. read the file
# ===============================

filename = './debate.txt'
#filename = './test.txt'
file = open(filename, "r", encoding='UTF-8')

doc = file.readlines()
list1 = []
list2 = []
for line in doc:
    if(len(line.strip())!= 0):          #checks for the empty line
        line = tokenize(line)           #gives the tokenized version of the line
        list1.append(line)              #appends the tokenized paragraph to the list1

# for i in range(len(list1)):           #prints the list of the each paragraph
#     print("List No: ",i, list1[i]," >> " ,len(list1[i]))
# print("------------------------------------------------")
# print("\n>>> No of Paragraph = ", len(list1),">>")
#=================================

list1 = swremover(list1)
# print("------------------------------------------------")
# for i in range(len(list1)):             # prints list with no stop word
#     print("Func. No StopWord List: ", i, list1[i], " >> ", len(list1[i]))

#==================================

#print("------------------------------------------------")

list1 = stemmize(list1)
# for i in range(len(list1)):             # prints the stemmed list
#     print("Func. Stemmed List No: ", i, list1[i], " >> ", len(list1[i]))

#=================================

# for i in range(len(list1)):             #prints the list of the each paragraph
#     print("Sim List No: ",i, list1[i]," >> " ,len(list1[i]))
# print("------------------------------------------------")

list1 = lowerize(list1)                   #lowerises the whole list1

# for i in range(len(list1)):             #prints the list of the each paragraph
#     print("Lower List No: ",i, list1[i]," >> " ,len(list1[i]))
#
# diction = {}                            #presents the dictionary for the whole text file: not useful
# diction = dictionize(list1)
#print("Overall Dictionary: ", diction)
#==============================
for i in range(len(list1)):               #concatnates the individual paragraph into one list for the whole file
    list2 += list1[i]
#print("Whole text: ", list2," >> " ,len(list2))

#variables
N = len(list1)
#print("Number of documents(N) = ", N)

#======================================
#takes the string list and gives the weight vector
def weight_vector_finder (strlist):
    wt_vec = {}
    TF = 0
    IDF = 0

    for word in strlist:
        TF = tf_finder(word,strlist)
        IDF = dft_finder(word)
        value = TF * IDF
        #print(word , value)
        wt_vec[word] = value

    #print("The weight vector dictionary: " ,wt_vec)
    return wt_vec
#====================================
# takes the string and the paragraph and gives the desired weight vector
# not yet working

def getqvec_funct(str, strlist):
    wt_vec = {}
    TF = 0
    IDF = 0
    str = list_stem(str)
    for i in range(len(strlist)):
        for j in range(len(str)):                #needs to be fixed
            if(str[j]==strlist[i] ):
                TF = tf_finder(str[j], strlist[i])
                IDF = dft_finder(str[j])
                value = TF * IDF
                #print(str[j], value)
                wt_vec[str[j]] = value

    #print("Weight vector for slected wordlist: ", wt_vec)
    return wt_vec


#==========================================

while(True):
    command = input('Enter command :: ')

    #for the getidf, preliminary calculation
    if('getidf' in command):

        idf = 0                         #idf variable for the document frequencey
        str = " "                       #temporary string variable to store the command
        strg = " "
        slist = []
        strg = command                  #storing the command in the temp variable = strg

        slist = tokenize(strg)          #storing the command as tokens in the list = slist
        #print(slist)
        str = slist[len(slist)-1]       #Assuming the last token is the word to be evaluated
        str = str.lower()

        #===============
        idf = dft_finder(str)
        if(idf == 1):
            print("No Match: ", idf)
        else:
            print("%.4f " %idf)
#
    if ('getqvec'in command):

        str = " "                       # temporary string variable to store the command
        strg = " "
        slist = []
        strg = command                  # storing the command in the temp variable = strg
        slist = tokenize(strg.lower())  # storing the command as tokens in the list = slist
        #print("Tokenzied QVec list :", slist)

        slist = slist [2:]               #deletes the first two words from the lis
        slist = list_swremover(slist)    #stop word removal
        #print("No SW list:", slist)

        dic_vector = {}                  #intialize the dictionary for Q-vector
        for word in slist:

            idf = 0
            idf = dft_finder(word)       # checks the idf for the sample word
            stemmer = PorterStemmer()
            word = stemmer.stem(word)
            dic_vector[word] = idf       #creates the dictionary for q-vector with idf as value

        print(dic_vector)


    if ('query' in command):

        str = " "                       # temporary string variable to store the command
        strg = " "
        slist = []
        strg = command                  # storing the command in the temp variable = strg
        slist = tokenize(strg.lower())  # storing the command as tokens in the list = slist
        #print("Tokenzied Query list :", slist)
        slist = slist[4:]               # deletes the first two words from the lis
        slist = list_swremover(slist)   # stop word removal
        #print("No SW Query list:", slist)

        dic_doc = {}
        dic_query = {}
        distance_query = 0

        dic_query = weight_vector_finder(slist)
        print("Query: ", dic_query)

        #print("Searching.....")


#==================================================
    if (command == 'quit'):
        print("Exiting the Program....")
        exit()


#=================================
file.close()

