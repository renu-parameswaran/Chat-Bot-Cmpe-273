import lang_processor
import database
import log

def getReply(userInput):
    userInputArray = lang_processor.split_message(userInput)
    userInputWithOnlyQuestionAndKeywords = lang_processor.removeUnwantedWords(userInputArray)
    questions,keywords = lang_processor.seperateQuestionAndKeywords(userInputWithOnlyQuestionAndKeywords)
	
    conn = database.connectToDB()
    response = handle_request(questions,keywords,conn)

    return response


def handle_request(questions,keywords,conn):
    count = len(questions)
    if (count == 0):
     response =  common_replies(keywords)
    elif(count == 1):
       response = "hello this is from renu's code"
       if(conn!="error"):
            allResponses=database.getAllResponses(questions[0],conn)
            allResponses=getMatchingKeywords(allResponses,keywords)
    else :
     response = "please input proper question format to handle them"

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


#Function to get matching Keywords
def getMatchingKeywords(allResponses,keywords):
    spiltAllResponse = []
    for response in allResponses:
        length = len(response['keywords'].split(','))
        for i in range(0, length):
            spiltAllResponse.append(response['keywords'].split(',')[i])
        matchKeyList = []
        for val1 in spiltAllResponse:
            for val2 in keywords:
                if(val2.lower() == val1.lower()):
                    matchKeyList.append(val2)

        response['numberOfMatchingKeywords'] = len(matchKeyList)
        lengthMKL =len(matchKeyList)
        stra =""
        for i in range(0,lengthMKL):
        	stra = stra + matchKeyList[i] +","

        response['matchingKeyWords'] = stra
        response['matchingKeyWords']= (unicode.encode(response['matchingKeyWords'])).rstrip(',')
        del matchKeyList[:]
        del spiltAllResponse[:]

    log.writetofile("Adding matching keyword")
    log.writetofile(str(allResponses))
    return allResponses
