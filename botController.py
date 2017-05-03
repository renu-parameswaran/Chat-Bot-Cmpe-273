import lang_processor
import database
import log
import config
import operator

currentMode="default"
conn = database.connectToDB()


def getReply(userInput):
    global conn
    userInputArray = lang_processor.split_message(userInput)
    userInputWithOnlyQuestionAndKeywords = lang_processor.removeUnwantedWords(userInputArray)
    questions,keywords = lang_processor.seperateQuestionAndKeywords(userInputWithOnlyQuestionAndKeywords)
    response = handle_request(questions, keywords, userInput,userInputArray, conn)

    return response


def handle_request(questions, keywords, userInput,userInputArray, conn):
    count = len(questions)
    if (count == 0):
        response = common_replies(userInput)
    elif (count == 1):

        if (conn != "error"):
            response = pickBestResponse(keywords,userInput,userInputArray,questions[0],conn)
        else:
            response = config.dbConnectionError

    else:
        response = config.twoQuestionsError

    return response


def pickBestResponse(keywords,userInput,userInputArray,questionPartInUserInput,conn):

    DBResponses = database.getAllResponses(conn)
    DBResponses = getMatchingKeywords(DBResponses, keywords)
    DBResponses.sort(key=operator.itemgetter('numberOfMatchingKeywords'),reverse=True)
    log.writetofile("sorted:" + str(DBResponses))

    for dbResponse in DBResponses:
        #100% match for the entities. Return this response
        if dbResponse['nonMatchingKeyWords']=="" and dbResponse['nonMatchingKeywordsInDB']=="":
            log.writetofile("100% match found")
            return dbResponse['answer']
        #not 100%.
        #perform spell check and find similar words
        else:
            if(dbResponse["numberOfMatchingKeywords"]>=1):
                nonMatchingKeywords = dbResponse['nonMatchingKeyWords'].split(',')
                nonMatchingKeywordsinDB = dbResponse['nonMatchingKeywordsInDB'].split(',')

                for nonMatchingKeyword in nonMatchingKeywords:
                    correctedKeyword = lang_processor.autocorrect(nonMatchingKeyword)
                    if(correctedKeyword != nonMatchingKeyword):
                        log.writetofile("spelling corrected:" + correctedKeyword)
                    synonyms = lang_processor.getSynonyms(correctedKeyword)
                    log.writetofile("synonyms for user input " +correctedKeyword + ":" + str(synonyms))

                    for nonMatchingKeyword in nonMatchingKeywordsinDB:
                        DBsynonyms = lang_processor.getSynonyms(nonMatchingKeyword)
                        log.writetofile("synonyms for DB " +nonMatchingKeyword + ":" + str(DBsynonyms))

                        if(set(DBsynonyms) == set(synonyms)):
                            log.writetofile("matching synonym found.")
                            dbResponse["numberOfMatchingKeywords"] = dbResponse["numberOfMatchingKeywords"]+1;

    log.writetofile("after synonyms : "+str(DBResponses))

    DBResponses.sort(key=operator.itemgetter('numberOfMatchingKeywords'),reverse=True)

    responseNumber = 1
    for dbResponse in DBResponses:
        if dbResponse["numberOfMatchingKeywords"] !=0:
            if responseNumber == 1:
                firstResponseMatchingCount = dbResponse["numberOfMatchingKeywords"]
                response = dbResponse["answer"]
                responseNumber = responseNumber+1
                questionPart = dbResponse["question"]
            else:
                if firstResponseMatchingCount == dbResponse["numberOfMatchingKeywords"]:
                    if questionPart == questionPartInUserInput:
                        return response
                    elif questionPartInUserInput == dbResponse["question"]:
                        response = dbResponse["answer"]
                    else:
                        response = config.ambiguousInput

                return response
        else:
            return config.ambiguousInput
    # pastResponses = database.getPastResponseFromUserInput(userInput,conn)
    return config.noAppropriateResponseFound

def common_replies(user_input):
    for i in user_input:
        if i in ("Hi sara"):
            response = "Hi! Welcome"
        elif i in ("Thanks Sara"):
            response = "Welcome Sara"
        elif i in ("Its a great day"):
            response = "Yes, A Wonderful Day."
        else:
            response = "Sorry! Cannot Handle"
    return response


# Function to get matching Keywords
def getMatchingKeywords(allResponses, keywords):
    currentKeywordList = []


    for response in allResponses:
        length = len(response['DbKeywords'].split(','))

        for i in range(0, length):
            currentKeywordList.append(response['DbKeywords'].split(',')[i])

        matchKeywordList = []
        notMatchingKeywordList = []
        notMatchingKeywordListinDB = []

        for val1 in currentKeywordList:
            for val2 in keywords:
                if (val2.lower() == val1.lower()):
                    matchKeywordList.append(val2.lower())

        for val1 in keywords:
            if val1 not in matchKeywordList:
                notMatchingKeywordList.append(val1.lower())

        for val1 in currentKeywordList:
            if val1 not in matchKeywordList:
                notMatchingKeywordListinDB.append(val1.lower())
                response['nonMatchingKeywordsInDB'] = ','.join(notMatchingKeywordListinDB)


        response['numberOfUserInputKeywords'] = len(keywords)
        response['numberOfMatchingKeywords'] = len(matchKeywordList)

        if  response['numberOfUserInputKeywords'] != response['numberOfMatchingKeywords']:
            response['nonMatchingKeyWords'] = unicode.encode(','.join(notMatchingKeywordList))


        lengthMKL = len(matchKeywordList)
        stra = ""
        for i in range(0, lengthMKL):
            stra = stra + matchKeywordList[i] + ","

        response['matchingKeyWords'] = stra
        try:
            response['matchingKeyWords'] = (unicode.encode(response['matchingKeyWords'])).rstrip(',')
        except:
            response['matchingKeyWords'] = ""

        del matchKeywordList[:]
        del currentKeywordList[:]
        del notMatchingKeywordList[:]
      
    log.writetofile("Adding matching keyword")
    log.writetofile(str(allResponses))
    return allResponses

#Function to get the Current Mode
def currentWorkingMode(userInput):
    global currentMode
    if(currentMode=="default"):
        if(userInput=="1"):
            currentMode="chat"
            response = config.chatResponse
            log.writetofile(response)
        elif (userInput=="2"):
            currentMode="training"
            response = config.trainingResponse
            log.writetofile(response)
        elif (userInput=="3"):
            currentMode="statistics"
            response = config.statisticsResponse
            log.writetofile(response)
        else:
            response="Invalid Input. Please input the number to choose your mode"
            log.writetofile(response)
    elif (currentMode=="chat"):
        response= getReply(userInput)
    elif (currentMode=="training"):
        response = "Call Training Function"
    else:
        response = "Call Statistics Function"
        
    return response
        
            