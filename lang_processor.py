#!/usr/bin/python
import log
import nltk
import config
from autocorrect import spell
from nltk.corpus import wordnet
import re
#from PyDictionary import PyDictionary

questionList = config.questionList

def split_message(userInput):

  #log.writetofile("splitting words")
  userInputList = userInput.lower().split(" ")
  userInputListWithAlphaNumeric = []
  for str in userInputList:
      userInputListWithAlphaNumeric.append(re.sub(r'\W+', '', str))
  log.writetofile("UserInput list having only alphanumeric strings" + userInputListWithAlphaNumeric)
  return userInputListWithAlphaNumeric

def seperateQuestionAndKeywords(input):
    questionsInUserInput = []
    keyWordsInUserInput = []

    log.writetofile("seperating the questions and keywords from user input")
    for inp in input:
        if inp in questionList:
            questionsInUserInput.append(inp)
            log.writetofile("Question: " + inp)
        else:
            keyWordsInUserInput.append(inp)
            log.writetofile("keyword: " + inp)

    return questionsInUserInput, keyWordsInUserInput


def removeUnwantedWords(input):
    userInputWithOnlyQuestionAndKeywords = []
    posTagged = nltk.pos_tag(input)
    simplifiedTags = [(word, nltk.map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
    for key,value in simplifiedTags:
        if (key.lower() in config.questionList) or (value not in 'ADP' and value not in 'DET' and value not in 'CONJ' and value not in 'PRT' and key not in 'is'):
            userInputWithOnlyQuestionAndKeywords.append(key)
        else:
            log.writetofile("blacklisted word: " + key)

    return userInputWithOnlyQuestionAndKeywords

def autocorrect(word):

    return spell(word)

def getSynonyms(word):
    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(unicode.encode(l.name()))

    #dictionary = PyDictionary()
    #print (dictionary.synonym(word))

    return synonyms
