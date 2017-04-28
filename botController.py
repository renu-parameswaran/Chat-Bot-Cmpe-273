import lang_processor
import database

def getReply(userInput):
    userInputArray = lang_processor.split_message(userInput)
    userInputWithOnlyQuestionAndKeywords = lang_processor.removeUnwantedWords(userInputArray)
    questions,keywords = lang_processor.seperateQuestionAndKeywords(userInputWithOnlyQuestionAndKeywords)
	
    conn = database.connectToDB()
    if(conn!="error"):
        database.getAllResponses(questions[0],conn)
   
	
    response = handle_request(questions,keywords)
    return response


def handle_request(questions,Keywords):
    count = len(questions)
    if (count == 0):
     response =  common_replies(Keywords)
    elif(count == 1):
       response = "hello this is from renu's code"
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

