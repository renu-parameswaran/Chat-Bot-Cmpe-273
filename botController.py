import lang_processor
import database

def getReply(userInput):
    userInputArray = lang_processor.split_message(userInput)
    userInputWithOnlyQuestionAndKeywords = lang_processor.removeUnwantedWords(userInputArray)
    questions,keywords = lang_processor.seperateQuestionAndKeywords(userInputWithOnlyQuestionAndKeywords)
    #questions,keywords = lang_processor.seperateQuestionAndKeywords(userInputArray)
    conn = database.connectToDB()
    if(conn!="error"):
        database.getAllResponses(questions[0],conn)
    
    response = "This is sara. How can I help?"
    if userInput.startswith("do"):
        response = "Need some intelligence first"

    return response

