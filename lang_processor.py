#!/usr/bin/python
import log
import nltk
import config

questionList = config.questionList

def split_message(cmd):

  #log.writetofile("splitting words")
  str = cmd.lower().split(" ")
  return str

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
        if value not in 'ADP' and value not in 'DET' and value not in 'CONJ' and value not in 'PRT':
            userInputWithOnlyQuestionAndKeywords.append(key)
        else:
            log.writetofile("blacklisted word: " + key)

    return userInputWithOnlyQuestionAndKeywords