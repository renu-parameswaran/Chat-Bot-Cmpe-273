import lang_processor
import database
import log
import config
import operator
import time
#import weather

currentMode = "default"
userInputQuestions = []
userInputKeywords = []
responseID = 0
conn = database.connectToDB()


# Function to get keywords and Questions separately from user input
def userInputQuestionKeyword(userInput):
    userInputArray = lang_processor.split_message(userInput)
    userInputWithOnlyQuestionAndKeywords = lang_processor.removeUnwantedWords(userInputArray)
    questions, keywords = lang_processor.seperateQuestionAndKeywords(userInputWithOnlyQuestionAndKeywords)
    return questions, keywords


def getReply(userInput):
    global conn
    userInputArray = lang_processor.split_message(userInput)
    questions, keywords = userInputQuestionKeyword(userInput)

    response,image_url = handle_request(questions, keywords, userInput,userInputArray, conn)

    return response,image_url


def handle_request(questions, keywords, userInput, userInputArray, conn):
    count = len(questions)
    image_url = "none"
    if (count == 0):
        response = common_replies(userInput)
    elif (count == 1):

        if (conn != "error"):
            response,image_url = pickBestResponse(keywords,userInput,userInputArray,questions[0],conn)
            response = lang_processor.generateResponse(userInputArray, questions[0], response)

        else:
            response = config.dbConnectionError

    else:
        response = config.twoQuestionsError

    return response,image_url


def pickBestResponse(keywords, userInput, userInputArray, questionPartInUserInput, conn):
    image_url = "none"
    pastResponses,isPastResponseExists =  database.getPastResponseFromUserInput(userInput,conn)

    if isPastResponseExists:
        pastResponses.sort(key=operator.itemgetter('CurrentScore'), reverse=True)
        pastResponse = pastResponses[0]
        print pastResponse['CurrentScore']
        if int(pastResponse['CurrentScore'])>0:
            log.writetofile("I am giving a reply from my past experiences")
            response = pastResponse['Answer']
            image_url = pastResponse['Image_Url']
        else:
            log.writetofile("Score for my past experiences does not look good. I am gonna look for new responses in the DB")
            response,image_url = getBestResponseFromDB(keywords, userInput, userInputArray, questionPartInUserInput, conn,True,pastResponse['Answer'])
    else:
        log.writetofile("Getting new response from DB")
        response,image_url = getBestResponseFromDB(keywords, userInput, userInputArray, questionPartInUserInput, conn,False,"none")

    return response,image_url



def getBestResponseFromDB(keywords,userInput,userInputArray,questionPartInUserInput,conn,isNegativeScore,previousAnswer):
    image_url = "none"
    if isNegativeScore:
        DBResponses = database.getAllResponsesExceptAnswerWithNegativeScore(conn,previousAnswer)
    else:
        DBResponses = database.getAllResponses(conn)
    DBResponses = getMatchingKeywords(DBResponses, keywords)
    DBResponses.sort(key=operator.itemgetter('numberOfMatchingKeywords'), reverse=True)
    log.writetofile("sorted:" + str(DBResponses))

    for dbResponse in DBResponses:
        # 100% match for the keywords in user input with db keywords. Return this response
        #to do: two questions with 100% match?? match question!!
        if dbResponse['nonMatchingKeyWords'] == "" and dbResponse['nonMatchingKeywordsInDB'] == "":
            log.writetofile("100% match found")
            image_url = dbResponse["image_url"]
            database.storeSentResponse(userInput, dbResponse['answer'], keywords, questionPartInUserInput, conn, image_url)
            return dbResponse['answer'],image_url
        #not 100%.
        #perform spell check and find similar words
        else:
            if (dbResponse["numberOfMatchingKeywords"] >= 1):
                nonMatchingKeywords = dbResponse['nonMatchingKeyWords'].split(',')
                nonMatchingKeywordsinDB = dbResponse['nonMatchingKeywordsInDB'].split(',')

                for nonMatchingKeyword in nonMatchingKeywords:
                    correctedKeyword = lang_processor.autocorrect(nonMatchingKeyword)
                    if (correctedKeyword != nonMatchingKeyword):
                        log.writetofile("spelling corrected:" + correctedKeyword)
                    synonyms = lang_processor.getSynonyms(correctedKeyword)
                    #log.writetofile("synonyms for user input " + correctedKeyword + ":" + str(synonyms))

                    for nonMatchingKeyword in nonMatchingKeywordsinDB:
                        DBsynonyms = lang_processor.getSynonyms(nonMatchingKeyword)
                        #log.writetofile("synonyms for DB " + nonMatchingKeyword + ":" + str(DBsynonyms))

                        if (set(DBsynonyms) == set(synonyms)):
                            log.writetofile("matching synonym found.")
                            dbResponse["numberOfMatchingKeywords"] = dbResponse["numberOfMatchingKeywords"] + 1;

    log.writetofile("after synonyms : " + str(DBResponses))

    DBResponses.sort(key=operator.itemgetter('numberOfMatchingKeywords'), reverse=True)

    isAmbiguousReply = False
    responseNumber = 1
    for dbResponse in DBResponses:

            if responseNumber == 1:
                firstResponseMatchingCount = dbResponse["numberOfMatchingKeywords"]
                response = dbResponse["answer"]
                responseNumber = responseNumber+1
                questionPart = dbResponse["question"]
                image_url = dbResponse["image_url"]
            else:
                if(firstResponseMatchingCount != 0):
                    if firstResponseMatchingCount == dbResponse["numberOfMatchingKeywords"]:
                        if questionPart == questionPartInUserInput:
                            log.writetofile("2 responses.picking bases on question")
                        elif questionPartInUserInput == dbResponse["question"]:
                            response = dbResponse["answer"]
                            image_url = dbResponse["image_url"]
                            log.writetofile("2 responses.picking 2nd based on question")
                        else:
                            log.writetofile("2 responses.ambiguos")
                            isAmbiguousReply = True
                            image_url = dbResponse["image_url"]
                            response = config.ambiguousInput
                else:
                    log.writetofile("0 matching keywords")
                    isAmbiguousReply = True
                    image_url = dbResponse["image_url"]
                    response = config.ambiguousInput

                if(isAmbiguousReply):
                    log.writetofile("not storing in sent responses")
                else:
                    database.storeSentResponse(userInput, response, keywords, questionPartInUserInput, conn,image_url)
                    log.writetofile("storing sent response")

                return response,image_url

    # pastResponses = database.getPastResponseFromUserInput(userInput,conn)
    return config.noAppropriateResponseFound


def common_replies(user_input):
    for i in user_input:
        if i in ("hi sara"):
            response = "Hi! Welcome"
        elif i in ("hello sara"):
            response = "Hi..whatsup!?"
        elif i in ("sara, i need some help "):
            resposne = "What help do u need"
        elif i in ("thank you so much for the answers"):
            response = "You are welcome!"
        elif i in ("thanks Sara"):
            response = "Welcome Sara"
        elif i in ("Its a great day"):
            response = "Yes, A Wonderful Day."
        elif i in ("Can you improve your answers?"):
            response = "Yes..sure"
        elif i in ("How are you today?"):
            response = "Im good, thanks! "
        elif i in ("this is an amazing answer!"):
            response = "I know it is! "
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

        if response['numberOfUserInputKeywords'] != response['numberOfMatchingKeywords']:
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


# Function to get the Current Mode
def currentWorkingMode(userInput):
    image_url = "none"
    global currentMode
    if (currentMode == "default"):
        if (userInput == "1"):
            currentMode = "chat"
            response = config.chatResponse
            log.writetofile(response)
        elif (userInput == "2"):
            currentMode = "training"
            response = config.trainingResponse1
            log.writetofile(response)
        elif (userInput == "3"):
            currentMode = "feedback"
            response = config.feedbackResponse1
            log.writetofile(response)
        elif (userInput == "4"):
            currentMode = "statistics"
            response = config.statisticsResponse
            log.writetofile(response)
        elif (userInput == "5"):
            currentMode = "weather"
            response = config.weatherResponse
            log.writetofile(response)
        elif (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            response = "Invalid Input. Please input the number to choose your mode"
            log.writetofile(response)
    elif (currentMode == "chat"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            response,image_url= getReply(userInput)
            log.writetofile("Calling function botController getReply")

    elif (currentMode == "training"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            global userInputQuestions,userInputKeywords
            userInputQuestions,userInputKeywords = userInputQuestionKeyword(userInput)
            #print type(userInputQuestions)
            #print userInputQuestions
            if(len(userInputQuestions)):
                currentMode = "training2"
                response = config.trainingResponse2
    elif (currentMode == "training2"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            global userInputQuestions, userInputKeywords
            unicodeKeywords = []
            conn = database.connectToDB()
            unicodeKeywords = ','.join(userInputKeywords)
            if (database.checkRowExists(userInputQuestions[0], userInput, unicodeKeywords, conn)):
                log.writetofile("row already exist so not inserting")
                currentMode = "training"
            else:
                database.storeNewResponse(userInput, unicodeKeywords, userInputQuestions[0], conn)
                currentMode = "training"
            response = "Thanks for the information. " + config.trainingResponse1


    elif (currentMode == "feedback"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            id = int((unicode.encode(userInput)))
            conn = database.connectToDB()
            if (database.checkIDExists(id, conn)):
                global responseID
                responseID = userInput
                currentMode = "feedback2"
                dblist = database.getPastResponse(id, conn)
                for var1 in dblist:
                    response = "Question is: " + var1['UserQuestion'] + "\n" + config.feedbackResponse2
            else:
                response = "Response ID does not exist"
    elif (currentMode == "feedback2"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            global responseID
            conn = database.connectToDB()
            id = int((unicode.encode(responseID)))
            database.updatePastResponse(id,userInput,conn)
            if(userInput.lower()=="yes".lower() or userInput.lower()=="y"):
                response = config.feedbackResponseYes
                currentMode = "morefeedback"
            if (userInput.lower() == "no".lower() or userInput.lower() == "n"):
                currentMode = "wrongfeedback"
                response = config.feedbackResponseNo
    elif (currentMode == "morefeedback"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        if (userInput.lower() == "yes".lower() or userInput.lower() == "y"):
            currentMode = "feedback"
            response = config.feedbackResponse1
        else:
            response = defaultMode()
    elif (currentMode == "wrongfeedback"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            global responseID
            id = int((unicode.encode(responseID)))
            conn = database.connectToDB()
            dblist = database.getPastResponse(id, conn)

            for var1 in dblist:
                if (database.checkRowExists(var1['QuestionPart'], userInput, var1['MatchingKeywords'], conn)):
                    log.writetofile("row already exist so not inserting")


                else:
                    log.writetofile("new row inserted")
                    database.storeNewResponse(userInput, var1['MatchingKeywords'], var1['QuestionPart'], conn)

            response = config.feedbackResponseYes
            currentMode = "morefeedback"
    elif (currentMode=="weather"):
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            questions,keywords = userInputQuestionKeyword(userInput)
            #response = weather.getWeather(keywords)
            response = "weather mode initiated"

    else:
        if (userInput.lower() == "Exit".lower()):
            response = defaultMode()
        else:
            response = "Call Statistics Function"
        
    return response,image_url


# Function for default mode when userinput==0
def defaultMode():
    global currentMode
    currentMode = "default"
    log.writetofile("Returning to default mode")
    return config.initialDisplayMessage


def getMessage():
    currentTime = int(time.strftime('%H:%M').split(':')[0])
    if currentTime >= 6 and currentTime <= 12:
        response = "Hello!"+" "+ "Good morning!"
    elif currentTime >= 12 and currentTime <= 18:
        response = "Hello" + " " + "Good afternoon!"
    elif currentTime >= 18 and currentTime <= 22:
        response = "Hello" + " " + "Good evening!"
    else:
        response = "Hello" + " " + "Greetings. It's late and you should get some sleep!"
    return response