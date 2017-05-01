import lang_processor
import database
import log
import sara
import config

currentMode="default"

def getReply(userInput):
    userInputArray = lang_processor.split_message(userInput)
    userInputWithOnlyQuestionAndKeywords = lang_processor.removeUnwantedWords(userInputArray)
    questions,keywords = lang_processor.seperateQuestionAndKeywords(userInputWithOnlyQuestionAndKeywords)
    
    conn = database.connectToDB()
    response = handle_request(questions, keywords, userInput, conn)

    return response


def handle_request(questions, keywords, userInput, conn):
    count = len(questions)
    if (count == 0):
        response = common_replies(keywords)
    elif (count == 1):
        response = "Hello this is sara handling 1 question"
        if (conn != "error"):
            allResponses = database.getAllResponses(questions[0], conn)
            allResponses = getMatchingKeywords(allResponses, keywords)
            database.storeSentResponse(userInput, response, keywords, questions[0], conn)
            database.getAllPastResponses(questions[0],keywords,conn)
            database.updatePastResponse(1, 'No', conn)
            database.storeNewResponse('Sweeny', keywords, questions[0], conn)
    else:
        response = "Please input proper question format to handle them"

    return response


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
        length = len(response['keywords'].split(','))
        for i in range(0, length):
            currentKeywordList.append(response['keywords'].split(',')[i])
        matchKeywordList = []
        for val1 in currentKeywordList:
            for val2 in keywords:
                if (val2.lower() == val1.lower()):
                    matchKeywordList.append(val2)

        response['numberOfMatchingKeywords'] = len(matchKeywordList)
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
        
            
